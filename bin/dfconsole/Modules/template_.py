#!/usr/bin/python
import sys
from support.setting import setting



class create:
    #define info here
    info = '''
This is an info piece.
It will display whenever someone checks the info of this module
Consider it a small README
'''                                                           #what is the 'information' or 'README'
    option_list=["option_a","option_b","option_c"]            #a list of all possible options
   

    #initialize variables here.  All Variables must be initialized, even if the value is ""
    #variables will have a name, value, IsRequired, and Description -- keep descriptions relativelt short, add to README if needed
    #option=setting(str,str,bool,str)    
    
    option_a=setting("option_a","value_a",False,"value for option_a")   
    option_b=setting("option_b","",True,"value for option_b")   
    option_c=setting("option_c","value_c",False,"value for option_c")   

    
    #initialize power_beacon class
    def __init__(self):
        self.name="my_module_name"
    
    def run(self) :             #the actual function
                                #recommend doing all variable checking here
                                #variables won't be checked in dfconsole and will be passed as strings

        print("These are the options I was passed and can use.")
        print(self.option_a.value)
        print(self.option_b.value)
        print(self.option_c.value)






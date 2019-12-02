#!/usr/bin/python

import getopt,sys,socket,time,subprocess,os

def show_help():
    print "Usage: ./client.py -a target_IP -p port -k key"

def main(argv):
    key=''
    ip=''
    port=''
    opts, args = getopt.getopt(argv,"ha:p:k:",["address=","port=","key="])  
   
    for opt, arg in opts:
          if opt == '-h' :
              show_help()
              sys.exit()
          elif opt in ("-a", "--address"):
              ip = arg
          elif opt in ("-p", "--port"):
              port = arg
          elif opt in ("-k", "--key"):
              key = arg



    if ip == '' or port == '' or key=='':
        show_help()
        sys.exit()
    #print ip
    #print port
    #print key
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s.connect((ip,int(port)))
    except:
        print "Unknown Error"
        sys.exit()
    #s.send(key)
    #print "enter the key"
    #key=raw_input()
    print "\n\nConnecting..."
    s.settimeout(300)   
    s.send(key)
    print s.recv(1024)
    while True:
        try:
            x=raw_input()
            if x[:3]=="LCD":
                newdir=x[4:]
                print newdir
                try:
                    os.chdir(newdir)
                    print "Local directory is now "+newdir
                    s.send(" ")
                    print s.recv(1024)    
                    continue
                except:
                    print "Unable to change local directory"
                    s.send(" ")
                    print s.recv(1024)
                    continue
            if x[:4]=="LDIR":
                try:
                    print os.getcwd()
                    subprocess.call(["ls", "-la"])
                    s.send(" ")
                    print s.recv(1024)
                    continue 
                except:
                    "Something bad happened..."
                    s.send(" ")
                    print s.recv(1024)
                    continue 
            s.send(x)
            if x[:4]=="DOWN":
              try:
                x=x.split(' ')
                print s.recv(1024)
                f = open(x[2],'wb')
                l=s.recv(1024)
                #print len(l)
                while len(l)==1024:
                    f.write(l)
                    l = s.recv(1024)
                f.write(l)
                f.close()
                time.sleep(3)
                print "File Collected"
                print s.recv(1024)
                continue
              except:
                print "Error collecting file"
                continue
            if x[:2]=="UP":
                try:
                    x=x.split(' ')
                    print "Preparing to send file...please wait"
                    time.sleep(1)
                    time.sleep(1)
                    f = open(x[1], "rb")
                    l = f.read(1024)
                    while (l):
                        s.send(l)
                        l = f.read(1024)
                        
                    f.close()
                    time.sleep(3)
                    print s.recv(1024)
                    continue
                except Exception as e:
                    print "Unable to send file"
                    print str(e)
                    continue
            time.sleep(1.5)
            l=s.recv(1024)
            data=l
            while len(l)==1024:
                l=s.recv(1024)    
                data=data+l
            print data
            if x== "EXIT":
                sys.exit()
                print s.recv(1024)
                time.sleep(1)
                #s.close()
                sys.exit()
        except Exception as e:
            print "An Unknown error has occured"
            print str(e)
            sys.exit()

if __name__ == "__main__":
    main(sys.argv[1:])



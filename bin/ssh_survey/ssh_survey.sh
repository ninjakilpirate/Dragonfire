#!/bin/bash
#BEGIN COMMENTS
: <<'COMMENTS'



COMMENTS
#END OF COMMENTS


if [  -z "$1"  ]
   then
   echo "Usage: ./ssh_survey [USER] [IP] [CONTROL_FILE] [PORT]"
   exit
   fi
if [  -z "$2"   ]
   then
   echo "Usage: ./ssh_survey [USER] [IP] [CONTROL_FILE] [PORT]"
   exit
   fi
if [  -z "$3"  ]
   then
   echo "Usage: ./ssh_survey [USER] [IP] [CONTROL_FILE] [PORT]"
   exit
   fi

if [  ! -e $3  ]; then
    echo "ControlPath $3 not found...exiting"
    exit
fi


echo -e "\n\n---Timestamps---"
ssh $1@$2 -S $3 date; date -u; date +%s

echo -e "\n\n---Checking/Disabling Auditd---"
ssh $1@$2 -S $3 'if [[ $(service auditd status | grep running | grep -vc grep)  > 0 ]] ; then service auditd stop && echo "Auditd is enabled, Disabling"; else echo "Auditd Not enabled" ; fi'

echo -e "\n\n---Grabbing Networking Configs---"
ssh $1@$2 -S $3 ifconfig -a;route;arp -a

echo -e "\n\n---OS Info---"
ssh $1@$2 -S $3 uname -a 
ssh $1@$2 -S $3 'for i in `ls /etc/*-release`; do cat $i; done'

echo -e "\n\n---CPU Info---"
ssh $1@$2 -S $3 cat /proc/cpuinfo

echo -e "\n\n---Hostname---"
ssh $1@$2 -S $3 hostname

echo -e "\n\n---Logged On Users/Last Log/Uptime"
ssh $1@$2 -S $3 w; last -i; uptime 

echo -e "\n\n---Disk Utilization---"
ssh $1@$2 -S $3 df -hi

echo -e "\n\n---/etc/passwd:shadow---"
ssh $1@$2 -S $3 cat /etc/passwd
ssh $1@$2 -S $3 cat /etc/shadow

echo -e "\n\n---Loaded Modules---"
ssh $1@$2 -S $3 lsmod 

echo -e "\n\n---History Checks---"
ssh $1@$2 -S $3 'for i in `ls /home`; do echo "==========$i history file============" && cat /home/$i/.bash_history; done'

echo -e "\n\n---Scheduled Jobs---"
ssh $1@$2 -S $3 ls -latr /var/spool/cron /var/spool/at
ssh $1@$2 -S $3 cat /etc/crontab
ssh $1@$2 -S $3 ls -latr /var/spool/cron /var/spool/at

echo -e "\n\n---Process List---"
ssh $1@$2 -S $3 ps -ef --sort start_time

echo -e "\n\n---Netstat---"
ssh $1@$2 -S $3 netstat -natup

echo -e "\n\n---Syslog---"
ssh $1@$2 -S $3 'for i in `find /etc | grep log.conf`; do cat $i; done'

echo -e "\n\n---Logging---"
ssh $1@$2 -S $3 ls -latr /var/log

echo -e "\n\n---Directory Listings---"
ssh $1@$2 -S $3 ls -lart /
ssh $1@$2 -S $3 ls -lart /tmp
ssh $1@$2 -S $3 ls -lart /root
ssh $1@$2 -S $3 ls -lart /home
ssh $1@$2 -S $3 ls -lart /root


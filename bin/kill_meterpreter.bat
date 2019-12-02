############EDIT THIS BEFORE USING!!!
############
############
###########EXAMPLE LINE FOR SCHTASK CREATION
###########schtasks /create /ru SYSTEM /sc once /st 23:59 /tn TASK_NAME /tr "c:\windows\kill.bat" 
###########schtasks /run /tn TASK_NAME 

taskkill /PID [PID] /F
ping 127.0.0.1 -n 20 > nul
schtasks /delete /tn TASK_NAME /F 
del c:\windows\temp\meter.exe
DEL "%~f0"

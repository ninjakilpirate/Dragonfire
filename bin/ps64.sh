#!/bin/bash
if [ $# -eq 0 ]
    then 
        echo "Usage:  ps64.sh string_to_convert"
        exit
fi

echo -ne $1 | iconv -f UTF8 -t UTF16LE | base64

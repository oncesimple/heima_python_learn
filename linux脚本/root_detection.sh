#!/bin/bash
#判断当前登录的用户是否为root
user=$(env | grep USER | cut -d "=" -f 2)    
if [ "$user" == "root"  ]
  then
    echo "当前用户是root"
else
    echo "当前用户不是root!"
fi
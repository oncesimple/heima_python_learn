#!/bin/sh
####### 安装hadoop #########
# 
######## 介绍结束 ###############


########## 脚本开始 ############
echo data1 > /etc/hostname 
cat hosts.txt >>/etc/hosts && source /etc/hosts
bash centosinstall.sh
bash java install.sh
bash hadoopinstall.sh
########## 脚本结束 ############
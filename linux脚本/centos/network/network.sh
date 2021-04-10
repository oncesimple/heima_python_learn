#!/bin/sh
####### 配置网络 #########
# 修改配置文件
######## 介绍结束 ###############


########## 脚本开始 ############
cat network.txt > /etc/sysconfig/network-scripts/ifcfg-ens33
service network restart
ping baidu.com
########## 脚本结束 #########
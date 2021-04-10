#!/bin/sh
####### 安装ntp #########
# yum 安装 npt
# 修改配置文件
# 重新加载 ntp
######## 介绍结束 ###############


########## 脚本开始 ############
yum install -y chrony
sed  -i 's/\#allow 192\.168\.0\.0\/16/allow 10\.1\.1\.11\/24/g'  /etc/chrony.conf
systemctl enable chronyd.service
systemctl start chronyd.service 
########## 脚本结束 ############
sed  -i 's/SELINUX=enforcing/SELINUX=disable/g'  /etc/sysconfig/selinux
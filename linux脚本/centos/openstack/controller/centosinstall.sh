#!/bin/sh

####### centos基础安装 #########
# 由于安装最小化系统所以我们要安装 wget 命令
# centos换源
# 安装 ifcofig 
# 安装 vim
# 安装 python3
# 关闭 firewalld
# 修改 selinux
# 关闭 NetworkManager
# 添加所有主机地址
######## 介绍结束 ###############


########## 脚本开始 ############
yum install -y wget
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
yum clean all
yum makecache
yum update -y
yum install -y net-tools 
yum install -y vim
yum install -y python3
systemctl stop firewalld
systemctl disable firewalld
sed  -i 's/SELINUX=enforcing/SELINUX=disable/g'  /etc/sysconfig/selinux
systemctl stop NetworkManager
systemctl stop NetworkManager 
cat hosts.txt >> /etc/hosts
########### 脚本结束 #############
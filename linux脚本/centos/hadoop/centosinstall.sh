#!/bin/sh

####### centos基础安装 #########
# 由于安装最小化系统所以我们要安装 wget 命令
# centos换源
# 安装 ifcofig 
# 安装 vim
######## 介绍结束 ###############


########## 脚本开始 ############
yum install -y wget
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
yum clean all
yum makecache
yum install -y net-tools 
yum install -y vim
########### 脚本结束 #############
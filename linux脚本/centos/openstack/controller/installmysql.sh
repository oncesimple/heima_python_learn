#!/bin/sh
####### 安装 mysql 数据库 #########
# 下载 mysql 官方源
#  安装 mysql 官方源
#  用 yum 安装 mysql
#  安装 glibc.i686 （mysql 依赖库）
#  安装依赖
#  给文件 权限  /var/lib/mysql/
#  启动 mysql
# 安装 python3
# 安装 gcc
######## 介绍结束 ###############


########## 脚本开始 ############
# echo computer > /etc/hostname   # 覆盖里面的所有内容
rpm -qa | grep mysql
yum install mysql -y
yum remove mysql -y
wget http://repo.mysql.com/mysql-community-release-el7-5.noarch.rpm
rpm -ivh mysql-community-release-el7-5.noarch.rpm
sudo yum install mysql-server -y
yum install glibc.i686 -y
yum list libstdc++* -y
chown root /var/lib/mysql/
service mysqld restart
yum install python3 -y
yum install gcc -y
########### 脚本结束 #############
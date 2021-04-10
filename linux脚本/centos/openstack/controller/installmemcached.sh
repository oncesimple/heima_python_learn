#!/bin/sh
####### 安装 memcached #########
# yum 安装软件
# 修改配置文件
# 服务启动并设置自启
######## 介绍结束 ###############


########## 脚本开始 ############
yum install -y memcached python-memcached
vim /etc/sysconfig/memcached 》》OPTIONS="-l 127.0.0.1,::1,controller"
systemctl enable memcached.service && systemctl start memcached.service
########## 脚本结束 ############
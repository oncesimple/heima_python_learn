#!/bin/sh
####### 安装 etcd 服务 #########
# yum 安装
# 修改配置文件  /etc/etcd/etcd.conf
# 设置服务启动并开机自启
######## 介绍结束 ###############


########## 脚本开始 ############
yum -y install etcd
xxxxxxxxxxxx
systemctl enable etcd && systemctl start etcd 
########## 脚本结束 ############
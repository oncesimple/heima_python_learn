#!/bin/sh
####### 安装消息队列 #########
# yum 安装软件
# 服务启动并添加自启
# 添加 openstack 用户
# 为 openstack 用户读写权限
######## 介绍结束 ###############


########## 脚本开始 ############
yum install -y rabbitmq-server
systemctl enable rabbitmq-server.service && systemctl start rabbitmq-server.service
rabbitmqctl add_user openstack f4mtdycd
rabbitmqctl set_permissions openstack ".*" ".*" ".*"
########## 脚本结束 ############
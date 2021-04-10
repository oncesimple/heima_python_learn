#!/bin/sh
#
######## linux基础配置 #########
##
######### 介绍结束 ###############
#
#

########### 脚本开始 ############
sudo yum install -y python3 python3-pip wget git vim net-tools tree
mkdir ~/.pip/
sudo tee ~/.pip/pip.conf <<-'EOF'
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
extra-index = https://pypi.tuna.tsinghua.edu.cn/simple
EOF
sleep 1
########### 脚本结束 #########
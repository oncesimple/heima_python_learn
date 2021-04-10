#!/bin/sh
####### 安装hadoop #########
# 首先你要有一个 /jdk-8u191-linux-x64.tar.gz 到你的 root 用户的家目录
# 创建一个文件
# 解压 jdk 压缩文件到 /usr/local/java/
# 添加 java 环境变量
# 重新加载配置文件
# 添加软连接
# 检查java是否安装完成
######## 介绍结束 ###############

########## 脚本开始 ############
mkdir /usr/local/java/
tar -zxvf ~/jdk-8u191-linux-x64.tar.gz -C /usr/local/java/
cat javaHome.txt >> /etc/profile
source /etc/profile
ln -s /usr/local/java/jdk1.8.0_191 /bin/java /usr/bin/java
java -version
########## 脚本结束 ############
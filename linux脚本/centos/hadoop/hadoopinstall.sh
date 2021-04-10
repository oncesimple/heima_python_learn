#!/bin/sh
####### 安装hadoop #########
# 修改主机名称
# 添加映射主机并且立即生效
# 配置ssh免密登录
# 下载 hadoop 安装包
# 解压 hadoop 安装包
# 剪切并修改 hadoop
# 修改文件 /opt/hadoop/etc/hadoop/hadoop-env.sh
# 修改 core-site.xml
# 修改 hdfs-site.xml
# 修改 mapred-site.xml.template
# 修改 yarn-site.xml
######## 介绍结束 ###############

########## 脚本开始 ############
ssh-keygen -t rsa
ssh-copy-id root@192.168.56.101
ssh-copy-id root@192.168.56.102
echo -e \\n
echo -e \\n
echo "下载hadoop" && sleep 5
echo -e \\n
echo -e \\n
mkdir -p /hadoop/export/data
mkdir -p /hadoop/tmp/dfs/data
mkdir -p /hadoop/tmp/dfs/name
tar -zxvf ~/hadoop-2.9.2.tar.gz -C /opt/hadoop/
mv hadoop-2.9.2 /opt/hadoop/
sed -i "s/export JAVA_HOME=${JAVA_HOME}/export JAVA_HOME=/usr/local/java/jdk1.8.0_191/g" /opt/hadoop/etc/hadoop/hadoop-env.sh
cat core-site.xml > /opt/hadoop/etc/hadoop/core-site.xml
cat hdfs-site.xml > /opt/hadoop/etc/hadoop/hdfs-site.xml
cat mapred-site.xml.template > /opt/hadoop/etc/hadoop/mapred-site.xml.template
cat yarn-site.xml > /opt/hadoop/etc/hadoop/yarn-site.xml
########## 脚本结束 ############
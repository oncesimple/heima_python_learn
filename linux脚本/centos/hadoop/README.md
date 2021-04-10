# hadoop搭建教程

## 所需要的软件以及服务
1. [jdk_1.8](https://pan.baidu.com/s/1NI3auPrbKCmu5NoPAhtncA)
2. [hadoop_2.9.2](https://pan.baidu.com/s/1NUoJR5Z35D99gw0BZJQaKg)
3. [centos7.4](http://isoredirect.centos.org/centos/8/isos/x86_64/CentOS-8-x86_64-1905-dvd1.iso)
4. [VMware Workstation Pro 注：windows软件](https://pan.baidu.com/s/1JCNc7AizOIwAlexfK5EAGA) 
5. [官方安装文档`建议使用chrome浏览器打开网站纯英文`](https://hadoop.apache.org/docs/r2.9.2/hadoop-project-dist/hadoop-common/SingleCluster.html#Fully-Distributed_Operation)
## 开始安装系统
此过程不在赘述

## 开始配置环境
一、 配置网卡信息
```bash
# vim /etc/sysconfig/network-scripts/对应自己的网卡
ONBOOT=yes
IPADDR=IP
PREFIX=子网掩码位数
GATEWAY=网关
DNS=域名解析服务器ip
```
二、主机名称配置和主机名映射
```haml
vim /etc/hostname
# 文件里面输入你想配置的主机名
这里以node-1为例
node-1
# vim /etc/hosts
添加以下内容
10.10.10.11 node-1
10.10.10.12 node-2
10.10.10.13 node-3
10.10.10.14 node-4
```
三、配置ssh免密登录
```haml
ssh-keygen -t rsa
ssh-copy-id 对方主机名
```
四、配置SElinu防火墙
```shell script
 firewall-cmd --state #查看状态
 systemctl stop firewalld.service # 关闭防火墙
 systemctl disable firewalld.service # 永久关闭防火墙
```
五、配置java环境
```shell script
rpm -qa|grep java # 检查已安装java 然后卸载自带的java
rem -e --nodeps # 检查出来的名称
vim /etc/profile
export JAVA_HOME=/hadoop/java/jdk(java路径可用which java 查询)
export PATH=$PATH:$JAVA_HOME/bin
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
source /etc/profile # 立马生效
# 检查java 版本
java -version
```
## Hadoop配置文件的修改

hadoop-env.sh文件的配置
```xml
export JAVA_HOME=/usr/bin/java(java路径可用which java查看)
```
core-site.xml的配置
```html

<configuration>
	<!-- 指定Hadoop所使用的文件系统schema(URI),HDFS的老大
	(NameNode)的地址-->
	<property>
		<name>fs.defaultFS</name>
		<value>hdfs://node-1:9000</value>
	</property>
	
	<!-- 指定Hadoop运行时产生的文件存储目录(默认在/tmp/hadoop-${user.name})-->
	<property>
		<name>hadoop.tmp.dir</name>
		<value>/hadoop/export/data</value>
	</property>
	
</configuration>
```
hdfs-site.xml的配置
```html
<configuration>
	<!-- 指定HDFS副本的数量(默认是3)-->
	<property>
		<name>dfs.replication</name>
		<value>2</value>
	</property>
	
	<!-- 指定secondary在那台机子上-->
	<property>
		<name>dfs.namenode.secondary.http-address</name>
		<value>node-2:50090</value>
	</property>
</configuration>
```
mapred-site.xml的配置(此文件默认是mapred-site.xml.template)
```html

<configuration>
	<!-- 指定YARN的老大(ResourceManager)的地址-->
	<property>
		<name>yarn.resourcemanager.hostname</name>
		<value>node-1</value>
	</property>
	
	<!-- NodeManager上运行的附属服务,需配置成mapreduce_shuffle,才可以运行Mapreduce程序默认值-->
	<property>
		<name>yarn.nodemanager.aux-services</name>
		<value>mapreduce_shuffle</value>
	</property>
</configuration>

```
slaves文件的配置
```bash
vim slaves
将所有节点主机名写入
```
将Hadoop安装位置添加到环境变量
```bash
vim /etc/profile
export HADOOP_HOME=/hadoop/hadoop-2.6.0/
export PATH=$PATH:$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
source /etc/profile  # 立马生效

```
配置好啦单台服务器(将文件分享到其他服务器)
```bash
# -r 代表文件 递归 复制/hadoop/hadoop-2.6.0/所有文件到 node-2主机root用户下的/hadoop/hadoop-2.6.0/下
scp -r /hadoop/hadoop-2.6.0/ root@node-2:/hadoop/hadoop-2.6.0/

```
将环境变量也复制到其他主机
```bash
scp -r /etc/profile root@node-2:/etc/
```
初次启动需要格式化
```bash
hdfs namenode -format
```
在主节点上启动
```bash
stop-all.sh   # 关闭全部
start-all.sh  # 启动全部
jps           # 查看状态
```
#!/bin/sh
#
######## docker 安装 #########
##
######### 介绍结束 ###############
#
#

########### 脚本开始 ############



# 下载docker 并安装
curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh && sleep 1
# 阿里镜像加速
sudo mkdir -p /etc/docker && sleep 1
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://q4a5yqz4.mirror.aliyuncs.com"]
}
EOF
sleep 1
sudo systemctl daemon-reload &&  sudo systemctl restart docker && sudo service docker start && sleep 1
# 下载myslq: 5.7

docker pull mysql:5.7 && sleep 1
# 添加docker开机启动
systemctl enable docker && sleep 1
# 设置启动mysql脚本
sudo tee ~/myslqRun.sh <<-'EOF'
#!/bin/bash

docker start mysql
EOF
sleep 1

sudo tee ~/myslqStop.sh <<-'EOF'
#!/bin/bash

docker stop mysql
EOF
sleep 1
# 添加权限
chmod +x ~/*

########### 脚本结束 #########
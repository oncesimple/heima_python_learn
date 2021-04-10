#!/bin/bash
# 分发文件脚本。
#1获取输入参数个数,如果没有参数,直接退出
pcount=$#
if((pcount==0)); then
echo no args;
exit;
fi

#2获取文件名称
p1=$1
fname=`basename $p1`
echo fname=$fname

#3获取上级目录到绝对路径
pdir=`cd -P $(dirname $p1); pwd`
echo pdir=$pdir

#4获取当前名称

user=`whoami`

#5循环
for((host=1; host<3 ; host++)); do
        echo ---------------- data$host ----------------
        rsync -rvl $pdir/$fname $user@data$host:$pdir
done

#!/usr/bin/python3
import os
import sys


if __name__ == "__main__":
    if os.geteuid() == 0:
        print ("现在是root用户")
    else:
        print(f"现在是 {os.environ['USER']} 用户，不是root用户,本脚本需要root用户权限，请您切换到root用户再进行操作。\n欢迎你再次使用。")
        print("程序退出")
        sys.exit(1)
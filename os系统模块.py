#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'hyh'
__date__ = '2020/4/28 12:47'
import platform
import os
import time


def main():
    OS = platform.platform()
    print(f'系统版本是:  {OS}  ')
    if 'Windows' in OS:
        print('此系统是Windows')
    elif 'Linux' in OS:
        print('此系统是linux')
        print('正在配置vim')
        os.system(
            'git clone https://github.com/gmarik/Vundle.vim.git ~/.vim/bundle/Vundle.vim')
        time.sleep(2)
        os.system(
            'wget https://gitee.com/muaimingjun/python_learn/raw/master/.vimrc')

        os.system('mv .vimrc ~/')


if __name__ == '__main__':
    main()

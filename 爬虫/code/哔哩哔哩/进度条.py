#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'hyh'
__date__ = '2020/9/14 14:55'
# import time
# import  multiprocessing
#
#
#
#
# def prin():
#     print("hello word!")
#     time.sleep(5)
#
# def main():
#     po = multiprocessing.Pool(5)
#     for i in range(10):
#         po.apply_async(prin)
#     po.close()
#     po.join()
#
# if __name__ == '__main__':
#     main()
# encoding: UTF-8
import threading
import time

def showfun(n):
    print ("%s start -- %d"%(time.ctime(),n))
    print ("working")
    time.sleep(2)
    print("%s end -- %d" % (time.ctime(), n))
    semlock.release()

if __name__ == '__main__':
    maxconnections = 5
    semlock = threading.BoundedSemaphore(maxconnections)
    list=[]
    for i in range(50):
        semlock.acquire()
        t=threading.Thread(target=showfun, args=(i,))
        # list.append(t)
        t.start()
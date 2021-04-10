import threading
import time


# 定义一个全局变量
g_num = 0
# 创建一个互斥锁，默认没有上锁
mutex = threading.Lock()


def test1(num):
    global g_num
    # 上锁，如果之前没有上锁，那么此时 上锁成功
    # 如果上锁之前 已经被上锁了，那么此时堵塞这里，直到 这个锁被解开位置
    for i in range(num):
        mutex.acquire()   # TODO 锁子放在里面会有什么效果？？？？？？
        g_num += 1
        mutex.release()

    print("-----in test1 g_num=%d----" % g_num)


def test2(num):
    global g_num
    for i in range(num):
        mutex.acquire()
        g_num += 1
        mutex.release()
    print("-----in test2 g_num=%d----" % g_num)


def main():
    t1 = threading.Thread(target=test1, args=(1000000, ))
    t2 = threading.Thread(target=test2, args=(1000000, ))

    t1.start()
    t2.start()

    # 等待上面的线程执行完毕...
    time.sleep(5)

    print("----in mian Thread g_num = %d" % g_num)


if __name__ == '__main__':
    main()

import threading
import time


# 线程的运行是没有先后顺序的
def test1():
    '''

    :return:
    这是我的第一个线程
    这是我的第二个线程
    '''
    for i in range(5):
        print("-----test1---%d---" % i)
        time.sleep(1)  # 如果创建Thread时执行的函数，运行结果那么意味着 这个子线程结束了....
        # exit()

def test2():
    for i in range(10):
        print("------test2---%d---" % i)
        time.sleep(1)
        # exit()

def main():
    t1 = threading.Thread(target=test1)
    t2 = threading.Thread(target=test2)

    t1.start()
    t2.start()

    while True:
        print(threading.enumerate())
        if len(threading.enumerate()) <= 1:
            break
        time.sleep(1)


if __name__ == '__main__':
    main()

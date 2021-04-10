#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'hyh  联系方式: 2667004988@qq.com'
__date__ = '2020/3/23 19:26'

import threading

import requests
import pandas as pd

'''
智慧树视频下载脚本
脚本显示未登录请修改   1. 第18行 data  2. 30行 Cookie
文档里面 按需求修改的有 1. 第18行 data  2. 30行 Cookie
'''


def page():
    """
    请求页面里所有视频id
    :return: 返回的是一个json
    """
    url = 'https://studyservice.zhihuishu.com/learning/videolist'
    # TODO data根据下载视频要修改
    data = {
        'recruitAndCourseId': '485c5c5f40524158424b595a51',
        'uuid': 'VBRkw8Jl',
        'dateFormate': 1584967219000
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0'
                      '; WOW64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/70.'
                      '0.3538.25 Safari/537.36 Core/1.'
                      '70.3732.400 QQBrowser/10.5.3819.400',
        # TODO Cookie根据需求修改
        'Cookie': 'acw_tc=2f624a1d15850541370174600e5e67d3e86ab6464214532b2df66332b15819; route=8c998338e1fb270d959036dd5e360e38; SESSION=YmM2ZjFkYzgtMGFiZS00ODc1LTk0YTAtODk3MjE2YTgxNjQ2; CASTGC=TGT-2448763-EocmCMg067gWGu5nwdsXxSCoQyfbnhmpbNfAYkAiFMlliNcaPz-passport.zhihuishu.com; CASLOGC=%7B%22myuniRole%22%3A0%2C%22username%22%3A%224c210445d6334553be7510d9680f1eea%22%2C%22mycuRole%22%3A0%2C%22userId%22%3A215575005%2C%22myinstRole%22%3A0%2C%22realName%22%3A%22%E8%B4%BA%E6%AF%85%E6%B5%A9%22%2C%22uuid%22%3A%22VBRkw8Jl%22%2C%22headPic%22%3A%22https%3A%2F%2Fimage.zhihuishu.com%2Fzhs%2Fablecommons%2Fdemo%2F201804%2F87c0fc18a2884d05b3dd671787afda15_s3.jpg%22%7D; exitRecod_VBRkw8Jl=2; SERVERID=b9cc2973d4be8136df436a41a34eed30|1585054651|1585054137'
    }
    r = requests.post(url, headers=headers, data=data)
    # r = requests.get(url, headers=headers, data=data).json()
    print(r.text)
    data = r.json()
    return data


def down_video(name, url):
    """
    下载视频
    :param name: 视频名字
    :param url: 视频下载地址
    :return: None
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0'
                      '; WOW64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/70.'
                      '0.3538.25 Safari/537.36 Core/1.'
                      '70.3732.400 QQBrowser/10.5.3819.400'
    }
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    name1 = name + ".mp4"
    with open(name1, "wb") as f:
        f.write(r.content)


def download(dic):
    """
    多线程下载视频
    :param dic:[课程名称] [课程地址]
    :return:None
    """
    text = len(dic['课程名称'])
    num = 0
    threadpool = []
    while num < text:
        print('正在下载{}'.format(dic['课程名称'][num]))

        th = threading.Thread(target=down_video, args=(dic['课程名称'][num], dic['课程地址'][num]))
        # 将线程加入线程池
        threadpool.append(th)
        num += 1
    for th in threadpool:
        th.start()
    # 等待所有线程运行完毕
    for th in threadpool:
        th.join()


def reque(url):
    """
    下载视频的json
    :param url: 视频json的url
    :return: 返回一个字典
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0'
                      '; WOW64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/70.'
                      '0.3538.25 Safari/537.36 Core/1.'
                      '70.3732.400 QQBrowser/10.5.3819.400'
    }
    url1 = requests.get(url, headers=headers).json()['result']['lines'][0]
    print(url1)
    return url1


# def openw():
#     '''
#     打开json文件
#     :return: {‘课程名称’:[],
#                     '课程地址':[]
#                     }
#     '''
#     # TODO 根据需求修改小程序.json
#     f = open(r"小程序.json", encoding="utf-8")
#     data1 = f.read()
#     f.close()
#     data2 = json.loads(data1)['data']['videoChapterDtos']
#     id = []
#     name = []
#
#     for i in data2:
#         for i in i['videoLessons']:
#             if i['videoId'] != 0:
#                 # time.sleep(10)
#
#                 id.append(i['videoId'])
#                 name.append(i['name'])
#     return {
#         '课程名称': name,
#         '课程地址': [reque('https://newbase.zhihuishu.com/video/initVideo?videoID={}'.format(i))['lineUrl'] for i in id],
#     }


def urls(data1):
    """
    传入整个视频的所有的信息
    :param data1: json文档
    :return:{‘课程名称’:[],
                    '课程地址':[]
                    }
    """
    print(data1)
    data2 = data1['data']['videoChapterDtos']
    name, video_id = [], []

    for i in data2:
        for name5 in i['videoLessons']:
            if name5['videoId'] != 0:
                # time.sleep(10)
                video_id.append(name5['videoId'])
                name.append(name5['name'])
    return {
        '课程名称': name,
        '课程地址': [reque('https://newbase.zhihuishu.com/video/initVideo?videoID={}'.format(i))['lineUrl'] for i in video_id],
    }


# def url1(helo):
#     '''
#     多线程请求
#     :param helo: list
#     :return: list
#     '''
#     id = []
#     threadpool = []
#     for i in helo:
#         th = threading.Thread(target=reque, args=())
#         # 将线程加入线程池
#         threadpool.append(th)
#         # TODO 多线程返回值不会用
#         id.append(reque('https://newbase.zhihuishu.com/video/initVideo?videoID={}'.format(i))['lineUrl'])
#     for th in threadpool:
#         th.start()
#     # 等待所有线程运行完毕
#     for th in threadpool:
#         th.join()
#     return id
def thread_it(func, *args):
    """将函数打包进线程"""
    # 创建
    t = threading.Thread(target=func, args=args)
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()


def main():
    # dic = openw()
    data = page()

    dic = urls(data)
    df = pd.DataFrame(dic)
    # TODO 按需求修改 小程序开发
    df.to_excel('小程序开发.xls')
    # 多线程下载
    # thread_it(download, dic)
    download(dic)


if __name__ == '__main__':
    main()

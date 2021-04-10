#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'hyh'
__date__ = '2020/9/12 17:08'
# !/usr/bin/python
# -*- coding:utf-8 -*-

import requests, time, hashlib, urllib.request, re, json
from multiprocessing import Pool
import os, sys, threading
from tkinter import *
from tqdm import tqdm

maxconnections = 6
semlock = threading.BoundedSemaphore(maxconnections)

# 弹出保存视频路径
if (sys.platform.startswith('win')):
    # 如果是windows系统弹出
    import easygui

    path = easygui.diropenbox('视频保存路径')
else:
    path = input('请输入保存路径')

# 清屏函数
def Clear():
    Hide()
    print('\033[2J', end='')

# 隐藏光标
def Hide():
    print('\033[?25l', end='')

# 访问API地址
def get_play_list(start_url, cid, quality):
    """


    """
    entropy = 'rbMCKn@KuamXWlPMoJGsKcbiJKUfkPF_8dABscJntvqhRSETg'
    appkey, sec = ''.join([chr(ord(i) + 2) for i in entropy[::-1]]).split(':')
    params = 'appkey=%s&cid=%s&otype=json&qn=%s&quality=%s&type=' % (appkey, cid, quality, quality)
    chksum = hashlib.md5(bytes(params + sec, 'utf8')).hexdigest()
    url_api = 'https://interface.bilibili.com/v2/playurl?%s&sign=%s' % (params, chksum)
    # print(url_api)
    headers = {
        'Referer': start_url,  # 注意加上referer
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
                      'Safari/537.36 '
    }
    # print(url_api)
    html = requests.get(url_api, headers=headers).json()
    # print(json.dumps(html))
    video_list = []
    for i in html['durl']:
        video_list.append(i['url'])
    # print(video_list)
    return video_list
# 下载视频
'''
 urllib.urlretrieve 的回调函数：
def callbackfunc(blocknum, blocksize, totalsize):
    @blocknum:  已经下载的数据块
    @blocksize: 数据块的大小
    @totalsize: 远程文件的大小
'''
#  下载视频
def down_video(video_list, title, start_url, page,wenjianjia):
    num = 1
    # print('[正在下载P{}段视频,请稍等...]:'.format(page) + title)
    currentVideoPath = os.path.join(path, wenjianjia)  # 当前目录作为下载目录
    for i in video_list:
        vid_headers = {
            'Origin': 'https://www.bilibili.com',
            'Referer': start_url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        }
        resp = requests.get(i,headers=vid_headers, stream=True)
        # 创建文件夹存放下载的视频
        if not os.path.exists(currentVideoPath):
            os.makedirs(currentVideoPath)
        # 开始下载
        if len(video_list) > 1:

            chunk_size = 1024  # 每次块大小为1024
            content_size = int(resp.headers['content-length'])  # 返回的response的headers中获取文件大小信息
            print(content_size)
            time.sleep(50)
            print("文件大小：" + str(round(float(content_size / chunk_size / 1024), 4)) + "[MB]")
            with open(currentVideoPath+r'/{}-{}.mp4'.format(title, num), "wb") as f:
                print("安装包整个大小是：", content_size, 'k，开始下载...')
                for data in tqdm(iterable=resp.iter_content(1024), total=content_size, unit='k', desc=r'{}-{}.mp4'.format(title, num)):
                    # 调用iter_content，一块一块的遍历要下载的内容，搭配stream=True，此时才开始真正的下载
                    # iterable：可迭代的进度条 total：总的迭代次数 desc：进度条的前缀
                    f.write(data)
                print(currentVideoPath+r'/{}-{}.mp4'.format(title, num) + "已经下载完毕！")
        else:
            content_size = int(resp.headers['content-length'])  # 返回的response的headers中获取文件大小信息
            with open(currentVideoPath + r'/{}.mp4'.format(title), "wb") as f:
                print("安装包整个大小是：", content_size, 'k，开始下载...')
                for data in tqdm(iterable=resp.iter_content(1024), total=content_size, unit='k',
                                 desc= r'{}.mp4'.format(title)):
                    # 调用iter_content，一块一块的遍历要下载的内容，搭配stream=True，此时才开始真正的下载
                    # iterable：可迭代的进度条 total：总的迭代次数 desc：进度条的前缀
                    f.write(data)
                print(currentVideoPath + r'/{}.mp4'.format(title) + "已经下载完毕！")
        num += 1
        # semlock.release()

def do_prepare(inputStart, inputQuality=80):
    """"
    inputStart: url/BV号
    inputQuality:视频质量
    """
    # 用户输入BV号或者视频链接地址
    # 设置进程池

    start = inputStart
    if start.isdigit() == True:  # 如果输入的是BV号
        # 获取cid的api, 传入aid即可
        start_url = 'https://api.bilibili.com/x/web-interface/view?bvid=' + start

    else:
        # https://www.bilibili.com/video/BV46958874/?spm_id_from=333.334.b_63686965665f7265636f6d6d656e64.16
        start_url = 'https://api.bilibili.com/x/web-interface/view?bvid=' + re.search(r'BV([0-9a-zA-Z]*)', start).group(
            1)
    # print(start_url)
    # 视频质量
    # <accept_format><![CDATA[flv,flv720,flv480,flv360]]></accept_format>
    # <accept_description><![CDATA[高清 1080P,高清 720P,清晰 480P,流畅 360P]]></accept_description>
    # <accept_quality><![CDATA[80,64,32,16]]></accept_quality>
    quality = inputQuality
    # 获取视频的cid,title
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    # print("视频json:"+start_url)
    html = requests.get(start_url, headers=headers).json()
    data = html['data']
    cid_list = []
    if '?p=' in start:
        # 单独下载分P视频中的一集
        p = re.search(r'\?p=(\d+)', start).group(1)
        cid_list.append(data['pages'][int(p) - 1])
    else:
        # 如果p不存在就是全集下载
        cid_list = data['pages']
    # print(cid_list)
    # 创建线程池
    threadpool = []
    title_list = []
    # Po = Pool(10)
    for item in cid_list:
        semlock.acquire()
        cid = str(item['cid'])
        title = item['part']
        title = re.sub(r'[\/\\:*?"<>|]', '', title)  # 替换为空的
        # print("正在加载：>>>>   " + title)
        # print('[下载视频的cid]:' + cid)
        # print('[下载视频的标题]:' + title)
        title_list.append(title)
        page = str(item['page'])
        start_url = start_url + "/?p=" + page
        print(start_url)
        video_list = get_play_list(start_url, cid, quality)
        # 下载视频
        Clear()
        down_video(video_list, title, start_url, page, data['title'])
        # t1 = threading.Thread(target=down_video, args=(video_list, title, start_url, page, data['title']))
        # threadpool.append(t1)
        # t1.start()
        # Po.apply_async(down_video,(video_list, title, start_url, page, data['title']))
    # for i in threadpool:
    #     # i.start()
    #     print(i)
    # for i in threadpool:
    #     i.join()
    # Po.close()
    # Po.join()
    # 如果是windows系统，下载完成后打开下载目录
    # currentVideoPath = os.path.join(sys.path[0], 'bilibili_video')  # 当前目录作为下载目录
    if sys.platform.startswith('win'):
        os.startfile(path)


def main():
    # t1 = threading.Thread(target=do_prepare, args=['BV1CE411L7qq'])
    # t1.start()
    # keyTrans = dict()
    # keyTrans['1080P+'] = '112'
    # keyTrans['1080P'] = '80'
    # keyTrans['720p'] = '64'
    # keyTrans['480p'] = '32'
    # keyTrans['360p'] = '16'
    # 初始值为720p
    # BV1CK411A7DY
    url = input('请输入视频地址或者视频BV/AV号:')
    do_prepare(url)


if __name__ == '__main__':
    main()

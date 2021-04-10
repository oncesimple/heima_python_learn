#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'hyh'
__date__ = '2020/9/22 8:14'

import requests, time, hashlib, urllib.request, re, json
from multiprocessing import Pool
import os, sys, threading
from tkinter import *
from tqdm import tqdm

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
def get_play_list(start_url, cid, quality, page, title):
    entropy = 'rbMCKn@KuamXWlPMoJGsKcbiJKUfkPF_8dABscJntvqhRSETg'
    appkey, sec = ''.join([chr(ord(i) + 2) for i in entropy[::-1]]).split(':')
    params = 'appkey=%s&cid=%s&otype=json&qn=%s&quality=%s&type=' % (appkey, cid, quality, quality)
    chksum = hashlib.md5(bytes(params + sec, 'utf8')).hexdigest()
    url_api = 'https://interface.bilibili.com/v2/playurl?%s&sign=%s' % (params, chksum)
    headers = {
        'Referer': start_url,  # 注意加上referer
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
                      'Safari/537.36 '
    }
    # print("视频地址的api地址:"+url_api)
    html = requests.get(url_api, headers=headers).json()
    video_list = []
    for i in html['durl']:
        video_list.append(i['url'])
    pages = {
        "cid": cid,
        'page': page,
        "title": title,
        "start_url": start_url,
        'video_list': video_list
    }
    return pages


#  下载视频
def down_video(video_list, title, start_url, wenjianjia, page):
    """
    下载视频函数
    """
    global file_path2
    num = 1
    print('[正在下载P{}段视频,请稍等...]:'.format(page) + title)
    currentVideoPath = os.path.join(path, wenjianjia)  # 当前目录作为下载目录
    for i in video_list:
        headers = {
            'Origin': 'https://www.bilibili.com',
            'Referer': start_url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        }
        # print(currentVideoPath)
        # 创建文件夹存放下载的视频
        if not os.path.exists(currentVideoPath):
            os.makedirs(currentVideoPath)
        rep = requests.get(i, headers=headers, stream=True)
        # 开始下载
        file_path1 = currentVideoPath + r'/{}-{}.mp4'.format(page + "-" + title, num)
        file_path2 = currentVideoPath + r'/{}.mp4'.format(page + "-" + title)
        content_size = int(rep.headers['content-length'])  # 返回的response的headers中获取文件大小信息
        # 断点续传
        if os.path.exists(file_path1):
            first_size = os.path.getsize(file_path1)
        elif os.path.exists(file_path2):
            first_size = os.path.getsize(file_path2)
        else:
            first_size = 0
        if first_size >= content_size:
            return content_size
        headers = {
            'Origin': 'https://www.bilibili.com',
            'Referer': start_url,
            'Range': f'bytes={first_size}-{content_size}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        }
        rep = requests.get(i, headers=headers, stream=True)
        if len(video_list) > 1:
            chunk_size = 1024  # 每次块大小为1024
            # print("文件大小：" + str(round(float(content_size / chunk_size / 1024), 4)) + "[MB]")
            with open(file_path1, "wb") as f:
                # print("安装包整个大小是：", content_size, 'k，开始下载...')
                for data in tqdm(iterable=rep.iter_content(1024), total=content_size, unit='k',
                                 desc=r'{}-{}.mp4'.format(title, num)):
                    # 调用iter_content，一块一块的遍历要下载的内容，搭配stream=True，此时才开始真正的下载
                    # iterable：可迭代的进度条 total：总的迭代次数 desc：进度条的前缀
                    f.write(data)
                print(currentVideoPath + r'/{}-{}.mp4'.format(title, num) + "已经下载完毕！")
        else:
            content_size = int(rep.headers['content-length'])  # 返回的response的headers中获取文件大小信息
            with open(file_path2, "wb") as f:
                # print("安装包整个大小是：", content_size, 'k，开始下载...')
                for data in tqdm(iterable=rep.iter_content(1024), total=content_size, unit='k',
                                 desc=r'{}.mp4'.format(title)):
                    # 调用iter_content，一块一块的遍历要下载的内容，搭配stream=True，此时才开始真正的下载
                    # iterable：可迭代的进度条 total：总的迭代次数 desc：进度条的前缀
                    f.write(data)
                print(currentVideoPath + r'/{}.mp4'.format(title) + "已经下载完毕！")
        num += 1


def do_prepare(inputStart, inputQuality=80):
    """"
    inputStart: url/BV号
    inputQuality:视频质量
    """
    # 用户输入BV号或者视频链接地址
    start = inputStart
    if start.isdigit() == True:  # 如果输入的是BV号
        # 获取cid的api, 传入aid即可
        start_url = 'https://api.bilibili.com/x/web-interface/view?bvid=' + start
    else:
        # https://www.bilibili.com/video/BV46958874/?spm_id_from=333.334.b_63686965665f7265636f6d6d656e64.16
        start_url = 'https://api.bilibili.com/x/web-interface/view?bvid=' + re.search(r'BV([0-9a-zA-Z]*)', start).group(
            1)
    # print("BV号的视频api地址:"+start_url)
    # 视频质量
    # <accept_format><![CDATA[flv,flv720,flv480,flv360]]></accept_format>
    # <accept_description><![CDATA[高清 1080P,高清 720P,清晰 480P,流畅 360P]]></accept_description>
    # <accept_quality><![CDATA[80,64,32,16]]></accept_quality>
    quality = inputQuality
    # 获取视频的cid,title
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    html = requests.get(start_url, headers=headers).json()
    data = html['data']
    currentVideoPath = os.path.join(path, data['title'])  # 当前目录作为下载目录
    if not os.path.exists(currentVideoPath):
        os.makedirs(currentVideoPath)
        cid_list = []
        if '?p=' in start:
            # 单独下载分P视频中的一集
            p = re.search(r'\?p=(\d+)', start).group(1)
            cid_list.append(data['pages'][int(p) - 1])
        else:
            # 如果p不存在就是全集下载
            cid_list = data['pages']
        videoss = []
        print(f"即将要下载《{data['title']}》此视频总共有（{data['videos']}）页")
        time.sleep(3)
        for item in cid_list:
            cid = str(item['cid'])
            title = item['part']
            title = re.sub(r'[\/\\:*?"<>|]', '', title)  # 替换为空的
            page = str(item['page'])
            start_url = start_url + "/?p=" + page
            video_list = get_play_list(start_url, cid, quality, page, title)
            videoss.append(video_list)
            print(f"正在添加第{page}页。")
        json_data = {
            "BVid": data['bvid'],
            "videos": data['videos'],
            "title": data['title'],
            "pages": videoss
        }

        with open(currentVideoPath + data["title"] + ".json", 'w') as f:
            f.write(json.dumps(json_data))
    with open(currentVideoPath + data["title"] + ".json", 'r') as fl:
        videoss = json.loads(fl.read())
    for data in videoss['pages']:
        # TODO 下载视频
        # semlock.acquire()
        # tl = threading.Thread(target=down_video,args=(data['video_list'], data['title'], data['start_url'], videoss['title'],data['page']))
        down_video(data['video_list'], data['title'], data['start_url'], videoss['title'], data['page'])
        # tl.start()


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
    # BV1Wv411C7Ca
    url = input('请输入视频地址或者视频BV/AV号:')
    do_prepare(url)


if __name__ == '__main__':
    main()

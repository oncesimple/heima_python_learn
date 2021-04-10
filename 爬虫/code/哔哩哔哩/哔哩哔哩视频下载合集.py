#!/usr/bin/python3
# -*- coding:utf-8 -*-
# 脚本仅供学习（禁止商用）
"""
评论模块已经写好未想好怎么部署
# TODO 脚本仅供学习（禁止商用）
"""
__author__ = 'hyh'
__date__ = '2020/4/16 10:17'

import re
import requests
import pandas as pd
import time
import math
import hashlib, urllib.request
from moviepy.editor import *
import os, sys, threading
import signal

# 线程信号量, 限制并发数
S = threading.Semaphore(5)

# 正在下载的视频
currentPage = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/79.0.3945.130 Safari/537.36 '
}

# 测试BV号 BV1ex411x7Em
work_information_url = 'https://api.bilibili.com/x/web-interface/view?bvid='
url = 'https://www.bilibili.com/video/{}?p=2'.format('BV号')
urlq = 'https://api.bilibili.com/x/web-interface/dynamic/region?ps=10&rid='


def reque_json(url):
    """
    请求json
    :param url: 请求api
    :return: 数据字典
    """
    data = requests.get(url).json()['data']
    return data


# 计算评论到底有多少页返回页数
def math11(data):
    """
    计算评论页数
    :param data: 数据字典
    :return: 页数
    """
    num = data['page']['count'] / data['page']['size']
    if type(num) == int:
        return num + 1
    else:
        return int(num) + 2


def replys(aid):
    """
    评论提取
    :param aid: oid
    :return: 数据列表
    """
    dic_list = []
    urls = f'https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn=1&type=1&oid={aid}'
    for i in range(1, math11(reque_json(urls))):
        # 拼接url
        url = f'https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn={i}&type=1&oid={aid}'
        data = reque_json(url)  # 请求url
        dic = pres(data)  # 数据的提取
        dic_list.append(pres(data))  # 数据整合成df然后放到列表里
    return dic_list


def pres(data):
    """
    评论提取
    :param data: 数据字典
    :return: 数据字典
    """
    data_list = data['replies']
    try:
        return {
            '用户id': [i['member']['mid'] for i in data_list],
            '用户昵称': [i['member']['uname'] for i in data_list],
            '性别': [i['member']['sex'] for i in data_list],
            '个性签名': [i['member']['sign'] for i in data_list],
            '评论': [i['content']['message'] for i in data_list],

        }
    except:
        return None


# 清屏函数
def Clear():
    Hide()
    print('\033[2J', end='')


# 显示光标
def Show():
    print('\033[?25h', end='')


# 隐藏光标
def Hide():
    print('\033[?25l', end='')


# 移动到位置,且清除这一行
def POS(x=0, y=0):
    print('\033[{};{}H\033[K'.format(y, x), end='')


def signal_handler(signal, frame):
    Show()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


# 访问API地址
def get_play_list(start_url, cid, quality):
    entropy = 'rbMCKn@KuamXWlPMoJGsKcbiJKUfkPF_8dABscJntvqhRSETg'
    appkey, sec = ''.join([chr(ord(i) + 2) for i in entropy[::-1]]).split(':')
    params = 'appkey=%s&cid=%s&otype=json&qn=%s&quality=%s&type=' % (appkey, cid, quality, quality)
    chksum = hashlib.md5(bytes(params + sec, 'utf8')).hexdigest()
    url_api = 'https://interface.bilibili.com/v2/playurl?%s&sign=%s' % (params, chksum)
    headers = {
        'Referer': start_url,  # 注意加上referer
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
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


def Schedule_cmd(title, page):
    """

    :param title:
    :param page:
    :return:
    """
    start_time = time.time()

    def Schedule(blocknum, blocksize, totalsize):
        # 进度条打印在第几行
        lineNum = currentPage.index(page) + 1
        POS(0, lineNum)
        speed = (blocknum * blocksize) / (time.time() - start_time)
        # speed_str = " Speed: %.2f" % speed
        speed_str = " Speed: %s" % format_size(speed)
        recv_size = blocknum * blocksize

        # 设置下载进度条
        percent = recv_size / totalsize
        percent_str = "%.2f%%" % (percent * 100)
        n = round(percent * 50)
        s = ('#' * n).ljust(50, '-')
        print('P{}:'.format(page) + '[' + s + ']  ' + percent_str.ljust(6, ' ') + speed_str)

    return Schedule


# 字节bytes转化K\M\G
def format_size(bytes):
    """

    :param bytes:
    :return:
    """
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"
    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%.3fG" % (G)
        else:
            return "%.3fM" % (M)
    else:
        return "%.3fK" % (kb)


#  下载视频
def down_video(video_list, pas, title, start_url, page):
    """

    :param video_list: 视频下载地址
    :param title: 作品名称
    :param start_url: 视频地址
    :param page: 数量
    :return:
    """
    S.acquire()
    num = 1
    currentVideoPath = os.path.join(sys.path[0], 'bilibili_video', pas)  # 当前目录作为下载目录
    if not os.path.exists(currentVideoPath):
        os.makedirs(currentVideoPath)
    for i in video_list:
        opener = urllib.request.build_opener()
        # 请求头
        opener.addheaders = [
            # ('Host', 'upos-hz-mirrorks3.acgvideo.com'),  #注意修改host,不用也行
            ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0'),
            ('Accept', '*/*'),
            ('Accept-Language', 'en-US,en;q=0.5'),
            ('Accept-Encoding', 'gzip, deflate, br'),
            ('Range', 'bytes=0-'),  # Range 的值要为 bytes=0- 才能下载完整视频
            ('Referer', start_url),  # 注意修改referer,必须要加的!
            ('Origin', 'https://www.bilibili.com'),
            ('Connection', 'keep-alive'),
        ]
        urllib.request.install_opener(opener)
        # 创建文件夹存放下载的视频
        if not os.path.exists(currentVideoPath):
            os.makedirs(currentVideoPath)
        # 开始下载
        reporthook = Schedule_cmd(title, page)
        currentPage.append(page)
        if len(video_list) > 1:
            urllib.request.urlretrieve(url=i, filename=os.path.join(currentVideoPath, r'{}-{}.mp4'.format(title, num)),
                                       reporthook=reporthook)  # 写成mp4也行  title + '-' + num + '.flv'
        else:
            urllib.request.urlretrieve(url=i, filename=os.path.join(currentVideoPath, r'{}.mp4'.format(title)),
                                       reporthook=reporthook)  # 写成mp4也行  title + '-' + num + '.flv'
        currentPage.remove(page)
        num += 1
    S.release()


# 合并视频
def combine_video(pas, title_list):
    """
    合并视频
    :param pas: 下载作品，名称
    :param title_list:
    :return:
    """
    video_path = os.path.join(sys.path[0], 'bilibili_video', pas)  # 下载目录
    for title in title_list:
        current_video_path = os.path.join(video_path, title)
        if len(os.listdir(current_video_path)) >= 2:
            # 视频大于一段才要合并
            print('[下载完成,正在合并视频...]:' + title)
            # 定义一个数组
            L = []
            # 遍历所有文件
            for file in sorted(os.listdir(current_video_path), key=lambda x: int(x[x.rindex("-") + 1:x.rindex(".")])):
                # 如果后缀名为 .mp4/.flv
                if os.path.splitext(file)[1] == '.flv':
                    # 拼接成完整路径
                    filePath = os.path.join(current_video_path, file)
                    # 载入视频
                    video = VideoFileClip(filePath)
                    # 添加到数组
                    L.append(video)
            # 拼接视频
            final_clip = concatenate_videoclips(L)
            # 生成目标视频文件
            final_clip.to_videofile(os.path.join(current_video_path, r'{}.mp4'.format(title)), fps=24,
                                    remove_temp=False)
            print('[视频合并完成]' + title)
        else:
            # 视频只有一段则直接打印下载完成
            print('[视频合并完成]:' + title)


def download(start, quality='112'):
    """
    视频下载
    :param start: 您要下载的B站BV号或者视频链接地址
    :param quality: 您要下载视频的清晰度(1080p+:112;1080p:80;720p:64;480p:32;360p:16)(填写112或80或64或32或16)
    :return:
    """
    start_time = time.time()

    start_url = 'https://api.bilibili.com/x/web-interface/view?bvid=' + re.findall(r'(BV[0-9a-zA-Z]*)|av\d*', start)[0]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
                      'Safari/537.36 '
    }
    html = requests.get(start_url, headers=headers)
    data = html.json()['data']
    File_name = data['title']
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
    Hide()
    for i, item in enumerate(cid_list):
        cid = str(item['cid'])
        title = item['part']
        title = re.sub(r'[\/\\:*?"<>|]', '', title)  # 替换为空的
        # s是进度条
        s = ('#' * round(i / len(cid_list) * 50)).ljust(50, '-')
        print('加载视频cid:[{}] {}/{}\r'.format(s, i, len(cid_list)), end='')
        title_list.append(title)
        page = str(item['page'])
        start_url = start_url + "/?p=" + page
        video_list = get_play_list(start_url, cid, quality)
        # down_video(video_list, title, start_url, page)
        # 定义线程
        th = threading.Thread(target=down_video, args=(video_list, File_name, title, start_url, page))
        # 将线程加入线程池
        threadpool.append(th)
    Clear()
    # 开始线程
    for th in threadpool:
        time.sleep(2)
        th.start()
    # 等待所有线程运行完毕
    for th in threadpool:
        time.sleep(2)
        th.join()
    Show()
    # 最后合并视频
    # combine_video(File_name, title_list)

    end_time = time.time()  # 结束时间
    print('下载总耗时%.2f秒,约%.2f分钟' % (end_time - start_time, int(end_time - start_time) / 60))
    # 如果是windows系统，下载完成后打开下载目录
    currentVideoPath = os.path.join(sys.path[0], 'bilibili_video')  # 当前目录作为下载目录
    if (sys.platform.startswith('win')):
        os.startfile(currentVideoPath)


def BV_id(url):
    """
    BV号提取
    :param url: https://api.bilibili.com/x/web-interface/dynamic/region?ps=10&rid= 序号
    :return: BV号列表
    """
    r = requests.get(url, headers=headers)
    return re.findall(r'(BV[0-9a-zA-Z]*)', r.text)


def work_information(start):
    start_url = work_information_url + re.search(r'BV([0-9a-zA-Z]*)', start).group(1)
    html = requests.get(start_url, headers=headers).json()
    try:
        data = html['data']

        dic = {
            '作品BV': data['bvid'],
            '发布时间': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data['ctime'])),
            '作品数': data['videos'],
            '作品名字': data['title'],
            '作者名字': data['owner']['name'],
            '作者id': data['owner']['mid'],
            '播放量': data['stat']['view'],
            '弹幕数': data['stat']['danmaku'],
            '硬币': data['stat']['reply'],
            '收藏': data['stat']['favorite'],
            '转发': data['stat']['share'],
            '评论数': data['stat']['reply'],
            'aid': data['aid'],  # 视频评论 "https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn=1&type=1&oid="+aid
            '作品简介': data['desc'],
        }
        # TODO 评论在这里
        # replys(data, data['aid'])
        return (dic,)
    except:
        print(html)


def Input(url):
    r = requests.get(url, headers=headers).json()['data']['page']['count']
    num = r / 30
    return math.ceil(num)


def Input1(url):
    return requests.get(url, headers=headers).json()['data']['numPages']


def UP_homepage():
    """
    UP主主页搜索
    :return:
    """
    BV = []
    ID = input('请输入作者mid:')
    url = 'https://api.bilibili.com/x/space/arc/search?mid=' + ID + '&ps=30&tid=0&pn=1&keyword=&order=pubdate&jsonp=jsonp'
    num = Input(url)
    print('总共 %s 页' % num)
    q = int(input('请输入你要开始的页数:'))
    r = int(input('请输入你要结束的页数:'))
    for i in range(q, r + 1):
        print('正在下载第{}页'.format(i))
        for nu in BV_id('https://api.bilibili.com/x/space/arc/search?mid=' + ID + '&ps=30&tid=0&pn=' + str(
                i) + '&keyword=&order=pubdate&jsonp=jsonp'):
            BV.append(nu)
    print('总共 %s 个作品' % len(BV))
    data = []
    number = 1
    for i in BV:
        print('正在爬取第{}个作品'.format(number))
        data_com = work_information(i)
        data.append(data_com[0])
        number += 1
    res = list(filter(None, data))
    time.sleep(3)
    print("正在写入DataFrame。")
    df = pd.DataFrame(res)
    print('正在去重数据')
    df.drop_duplicates('作品BV', 'first', inplace=True)
    w = input('您要下载的数据保存成csv吗? (输入： yes 或者 no):')
    if w == 'yes':
        print('正在写入数据')
        df.to_csv('{}_bilibi作品全部信息.csv'.format(df['作者名字'][1]), encoding='utf-8', index=False)
    elif w == 'no':
        print('数据没有保存。。')
    else:
        print('输入错误。程序退出。')
        exit()
    user_input_if(df)


def homepage():
    """
    主页搜索
    :return:
    """
    BV = []
    ID = input('请输入你想要搜索的内容:')
    url = 'https://api.bilibili.com/x/web-interface/search/type?context=&page=1&order=&keyword=' + ID + '&duration=&tids_1=&tids_2=&__refresh__=true&search_type=video&highlight=1&single_column=0&jsonp=jsonp'
    num = int(Input1(url))
    print('总共 %s 页' % num)
    q = int(input('请输入你要开始的页数:'))
    r = int(input('请输入你要结束的页数:'))
    for i in range(q, r + 1):
        print('正在下载第{}页'.format(i))
        for nu in BV_id('https://api.bilibili.com/x/web-interface/search/all/v2?context=&page=' + str(
                i) + '&order=&keyword=' + ID):
            BV.append(nu)
    print('总共 %s 个作品' % len(BV))
    data = []
    number = 1
    for i in BV:
        print('正在爬取第{}个作品'.format(number))
        data_com = work_information(i)
        try:
            data.append(data_com[0])
        except:
            print("啥也没有")
        number += 1
    res = list(filter(None, data))
    time.sleep(3)
    df = pd.DataFrame(res)
    print('正在去重数据')
    df.drop_duplicates('作品BV', 'first', inplace=True)
    w = input('您要下载的数据保存成csv吗? (输入： yes 或者 no):')
    if w == 'yes':
        print('正在写入数据')
        df.to_csv('{}_bilibi作品搜索信息.csv'.format(ID), encoding='utf-8', index=False)
    elif w == 'no':
        print('数据没有保存。。')
    else:
        print('输入错误。程序退出。')
        exit()
    user_input_if(df)


def user_input_if(df):
    """
    用户输入判断
    :param df: DataFrame
    :return:
    """
    # TODO 评论判断
    # reply = input('您要下载评论吗? (输入： yes 或者 no):')
    # reply = 'no'
    # if reply == 'yes':
    #     print('马上下载评论。')
    #     data = []
    #     for i in list(df['aid']):
    #         data + replys(i)
    #     ef = pd.DataFrame(data)
    #     ef.to_csv('hello.csv',index=False)
    # elif reply == 'no':
    #     print('数据没有保存。。程序退出。。')
    #     exit()
    # else:
    #     print('输入错误。程序退出。')
    #     exit()

    m = input('您要下载视频吗? (输入： yes 或者 no):')
    if m == 'yes':
        print('马上下载视频。')
        time.sleep(3)
        for BV in list(df['作品BV']):
            download(BV)
    elif m == 'no':
        print('数据没有保存。。程序退出。。')
        exit()
    else:
        print('输入错误。程序退出。')
        exit()


def main():
    print('==============' * 8)
    print('|  <<<<<<<bilibili（哔哩哔哩*干杯*）视频下载>>>>>>>    <<<<<视频下载脚本,视频详细信息下载>>>>>        <<<<<开始啦>>>>>>>  |')
    print('--------------' * 8)
    print('|  0: 退出;         |         1: 主页搜索;         |           2: UP主_主页;         |         3: BV号下载视频:     |')
    print('==============' * 8)
    num = input('请输入:')
    if num == '0':
        exit()
    elif num == '1':
        homepage()
    elif num == '2':
        UP_homepage()
    elif num == '3':
        BV = input("您要下载的B站BV号或者视频链接地址:")
        time.sleep(3)
        download(BV)
    else:
        print("您输入有误。程序退出。。")


if __name__ == '__main__':
    main()

import requests
import json
import time
import os
import re
"""

TODO 声明
脚本仅仅提供学习使用，拿来盗别人视频，或者商业用途，后果自负作者不会承担任何责任。。

"""


profile_url = "https://live.kuaishou.com/profile/"
data_url = "https://live.kuaishou.com/m_graphql"
work_url = "https://live.kuaishou.com/u/"
param_did = "?did=web_0897bf2eb33014d08a0a7064fd41c899"

headers = {
    'accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Host': 'live.kuaishou.com',
    'Origin': 'https://live.kuaishou.com',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',

    # User-Agent/Cookie 根据自己的电脑修改
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-N9100 Build/LRX21V) > AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 > Chrome/37.0.0.0 Mobile Safari/537.36 > MicroMessenger/6.0.2.56_r958800.520 NetType/WIFI',
    'Cookie': 'clientid=3; did=web_0897bf2eb33014d08a0a7064fd41c899; client_key=65890b29; kpn=GAME_ZONE; userId=74099798; didv=1607403433433; userId=74099798; kuaishou.live.bfb1s=477cb0011daca84b36b3a4676857e5a1; kuaishou.live.web_st=ChRrdWFpc2hvdS5saXZlLndlYi5zdBKgAbo-45F5Fz5bh9gGjb4R3IiGqwMucDTlDtr_-CmFc4lChRdDvLZNxl846jFROCsiTckWw4Lh9AO79DROtbh63stUyQFVc7e5je2MlTPNT6alPLXohJOF0ipo7BbdvWurtIulhOTbVDhCveDXFSjmrYwwnLPlCbT1W3M34_gI9ubAXtWWotWf2XbT5SZKSMca9tOEM__JAc_PO3B70oQUnQMaEsa__TMaP0jJgfAfW0kccZcKPyIg8T8U2KZcRUHrrw-pp8lsd3jZRnvPlK8DdyItxGURSSMoBTAB; kuaishou.live.web_ph=b4cc4bcea27e75415672acbd977ca022edf7'
}


def crawl_user(uid):
    global headers
    payload = {"operationName": "privateFeedsQuery",
               "variables": {"principalId": uid, "pcursor": "", "count": 99999},
               "query": "query privateFeedsQuery($principalId: String, $pcursor: String, $count: Int) {\n  privateFeeds(principalId: $principalId, pcursor: $pcursor, count: $count) {\n    pcursor\n    list {\n      id\n      thumbnailUrl\n      poster\n      workType\n      type\n      useVideoPlayer\n      imgUrls\n      imgSizes\n      magicFace\n      musicName\n      caption\n      location\n      liked\n      onlyFollowerCanComment\n      relativeHeight\n      timestamp\n      width\n      height\n      counts {\n        displayView\n        displayLike\n        displayComment\n        __typename\n      }\n      user {\n        id\n        eid\n        name\n        avatar\n        __typename\n      }\n      expTag\n      __typename\n    }\n    __typename\n  }\n}\n"}
    res = requests.post(data_url, headers=headers, json=payload)
    # 查看抓取的数据
    print(res.text)
    works = json.loads(res.content.decode(encoding='utf-8', errors='strict'))['data']['privateFeeds']['list']
    # print(works)
    if not os.path.exists("data"):
        os.makedirs("data")

    # 这两行代码将response写入json供分析
    # with open("data/" + uid + ".json", "w") as fp:
    #     fp.write(json.dumps(works, indent=2))

    # 防止该用户在直播，第一个作品默认为直播，导致获取信息为NoneType
    if works[0]['id'] is None:
        works.pop(0)
    name = works[0]['user']['name']
    #
    dir = "data/" + "(" + uid + ")/"
    print(len(works))
    if not os.path.exists(dir):
        os.makedirs(dir)
    print("开始爬取用户 " + name + "，保存在目录 " + dir)
    print(" 共有" + str(len(works)) + "个作品")

    for j in range(len(works)):
        print(j + 1)
        crawl_work(uid, dir, works[j], j + 1)
        time.sleep(1)
    print("用户 " + name + "爬取完成!")
    print()
    time.sleep(1)


'''
快手分为五种类型的作品，在作品里面表现为workType属性
 * 其中两种图集: `vertical`和`multiple`，意味着拼接长图和多图，所有图片的链接在imgUrls里
 * 一种单张图片: `single` 图片链接也在imgUrls里
 * K歌: `ksong` 图片链接一样，不考虑爬取音频...
 * 视频: `video` 需要解析html获得视频链接
'''


def get(url: str) -> dict:
    """
    title、imgs、videos
    """
    data = {}
    failed = {'msg': 'failed...'}
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25",
        "Cookie": "did=web_68e0268146694843a92700d2de49a0a6;"
    }
    # rewrite desktop url 这个url请求不出来想要的数据
    # temp = re.findall(r'live\.kuaishou\.com/u/\w+/(\w+)', url)
    # if temp:
    #     url = 'https://c.kuaishou.com/fw/photo/{}'.format(temp[0])
    # url  = https://live.kuaishou.com/u/jinyue521/3xxbcy9k9c4f3hw?did=web_0897bf2eb33014d08a0a7064fd41c899   uid
    # url = https://live.kuaishou.com/u/3xwi8eeif9kgjcu/3xxbcy9k9c4f3hw?did=web_0897bf2eb33014d08a0a7064fd41c899  eid
    rep = requests.get(url, headers=headers, timeout=10)
    if rep.status_code != 200:
        return failed

    page_data = re.findall(r'<script type="text/javascript">window\.pageData= (\{.*?\})</script>', rep.text)
    if not page_data:
        return failed

    try:
        page_data = json.loads(page_data[0])
    except Exception:
        print('kuaishou loads json failed')
        return failed

    video_info = page_data['video']
    data['title'] = video_info['caption']
    # 获取视频
    try:  # 如果出错，则可能是长图视频
        data['videos'] = [video_info['srcNoMark']]
    except Exception:
        pass
    else:
        data['videoName'] = data['title']
        data['msg'] = '如果快手视频下载出错请尝试更换网络'
    # 获取图片
    try:  # 如果出错，则可能是普通视频；
        images = video_info['images']
        imageCDN: str = video_info['imageCDN']
        # 如果是长图视频，则这几项一定存在
        assert images is not None
        assert imageCDN is not None
    except Exception:
        pass
    else:
        if not imageCDN.startswith('http'):
            imageCDN = 'http://' + imageCDN
        data['imgs'] = [imageCDN + i['path'] for i in images]
    return data


def crawl_work(uid, dir, work, wdx):
    w_caption = re.sub(r"\s+", " ", work['caption'])
    w_name = re.sub(r'[\\/:*?"<>|\r\n]+', "", w_caption)[0:24]
    w_time = time.strftime('%Y-%m-%d', time.localtime(work['timestamp'] / 1000))
    if len(work['imgUrls']) > 0:
        w_urls = work['imgUrls']
        l = len(w_urls)
        print("  " + str(wdx) + ")图集作品：" + w_caption + "，" + "共有" + str(l) + "张图片")
        for i in range(l):
            p_name = w_time + "_" + w_name + "_" + str(i + 1) + ".jpg"
            pic = dir + p_name
            if not os.path.exists(pic):
                r = requests.get(w_urls[i])
                r.raise_for_status()
                with open(pic, "wb") as f:
                    f.write(r.content)
                print("    " + str(i + 1) + "/" + str(l) + " 图片 " + p_name + " 下载成功 √")
            else:
                print("    " + str(i + 1) + "/" + str(l) + " 图片 " + p_name + " 已存在 √")
    elif len(work['imgUrls']) == 0:
        w_url = work_url + uid + "/" + work['id'] + param_did
        # print(''+w_url)
        print("  " + str(wdx) + ")视频作品：" + w_caption)
        v_name = w_time + "_" + w_name + ".mp4"
        video = dir + v_name

        if not os.path.exists(video):
            r = requests.get(get(w_url)['videos'][0])
            r.raise_for_status()

            with open(video, "wb") as f:
                f.write(r.content)
            print("    视频 " + v_name + " 下载成功 √")
        else:
            print("    视频 " + v_name + " 已存在 √")
    else:
        print("错误的类型")


def switch_id(uid):
    payload = {"operationName": "SearchOverviewQuery",
               "variables": {"keyword": uid, "ussid": None},
               "query": "query SearchOverviewQuery($keyword: String, $ussid: String) {\n  pcSearchOverview(keyword: $keyword, ussid: $ussid) {\n    list {\n      ... on SearchCategoryList {\n        type\n        list {\n          categoryId\n          categoryAbbr\n          title\n          src\n          __typename\n        }\n        __typename\n      }\n      ... on SearchUserList {\n        type\n        ussid\n        list {\n          id\n          name\n          living\n          avatar\n          sex\n          description\n          counts {\n            fan\n            follow\n            photo\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      ... on SearchLivestreamList {\n        type\n        lssid\n        list {\n          user {\n            id\n            avatar\n            name\n            __typename\n          }\n          poster\n          coverUrl\n          caption\n          id\n          playUrls {\n            quality\n            url\n            __typename\n          }\n          quality\n          gameInfo {\n            category\n            name\n            pubgSurvival\n            type\n            kingHero\n            __typename\n          }\n          hasRedPack\n          liveGuess\n          expTag\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
    res = requests.post(data_url, headers=headers, json=payload)
    dt = json.loads(res.content.decode(encoding='utf-8', errors='strict'))['data']
    return dt['pcSearchOverview']['list'][1]['list'][0]['id']


def crawl():
    # ['Aiby258377','3xwi8eeif9kgjcu']
    # uid = ['3xwi8eeif9kgjcu']
    uid = ['3xwi8eeif9kgjcu']

    for uid in uid:
        print(uid.isdigit())
        if uid.isdigit():
            crawl_user(switch_id(uid))
            print(crawl_user(switch_id(uid)))
        else:
            crawl_user(uid)


if __name__ == "__main__":
    crawl()

import re
import requests, json
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Cookie': 'clientid=3; did=web_0897bf2eb33014d08a0a7064fd41c899; client_key=65890b29; userId=74099798; didv=1583230324425; userId=74099798; kuaishou.live.bfb1s=ac5f27b3b62895859c4c1622f49856a4; kuaishou.live.web_st=ChRrdWFpc2hvdS5saXZlLndlYi5zdBKgAYB0XR4U9RZ15eHSPx8Bia7pxcYTntrGYYToVZo_aF5btZIHgU7ZYe68i5zbHsszgq9jV_JlUiDkmo6DDWRvIsMo2NTNFvdQ0_iFzbv5Xu1roeUgUzwUCL8XOzOUQ8--Tyqx1-yYI1Ic9edvi4aklgPcv0Lmxsq1uNbHssWUrzJEh53q7zvHTOdiT7Ix1wx-NslAZKawKVx70RfzLK3SrtIaEqtYXSf19kp4pfaTtPC7dufEBiIgQHWYKkLmGm1FM2IpGOpTmYanvzCZgi70At6oGq8U4rcoBTAB; kuaishou.live.web_ph=6acd1ef384ecd83e3c9282dbdb0dd5ebad97'
}
first_url = 'https://live.kuaishou.com/m_graphql'


def workType(url):
    # 请求视频地址
    res = requests.get(url, headers=headers)
    html = res.text
    soup = BeautifulSoup(html, "html.parser")

    pattern = re.compile(r"playUrl", re.MULTILINE | re.DOTALL)
    script = soup.find("script", text=pattern)
    s = pattern.search(script.text).string
    # time.sleep(2)
    return s.split('playUrl":"')[1].split('.mp4')[0].encode('utf-8').decode('unicode-escape') + '.mp4'


def data(uid):
    # 访问快手界面
    payload = {"operationName": "privateFeedsQuery",
               "variables": {"principalId": uid, "pcursor": "", "count": 99999},
               "query": "query privateFeedsQuery($principalId: String, $pcursor: String, $count: Int) {\n  privateFeeds(principalId: $principalId, pcursor: $pcursor, count: $count) {\n    pcursor\n    list {\n      id\n      thumbnailUrl\n      poster\n      workType\n      type\n      useVideoPlayer\n      imgUrls\n      imgSizes\n      magicFace\n      musicName\n      caption\n      location\n      liked\n      onlyFollowerCanComment\n      relativeHeight\n      timestamp\n      width\n      height\n      counts {\n        displayView\n        displayLike\n        displayComment\n        __typename\n      }\n      user {\n        id\n        eid\n        name\n        avatar\n        __typename\n      }\n      expTag\n      __typename\n    }\n    __typename\n  }\n}\n"
               }
    res = requests.post(first_url, headers=headers, json=payload)
    work = json.loads(res.content.decode(encoding='utf-8', errors='strict'))['data']['privateFeeds']['list']

    print(len(work))
    zhuye = [
        'https://live.kuaishou.com/u/' + i['user']['id'] + '/' + i['id'] + '?did=web_0897bf2eb33014d08a0a7064fd41c899'
        for i in work]
    shipin = []
    w = 1
    for i in zhuye:
        print('正在爬取第{}个作品'.format(w))
        w += 1
        url = workType(i)
        shipin.append(url)

    time.sleep(100)

    dic = {
        '作者id': [i['user']['id'] for i in work],
        '作者昵称': [i['user']['name'] for i in work],
        '作品标题': [i['caption'] for i in work],
        '作品主页': zhuye,
        '作品播放量': [i['counts']['displayView'] for i in work],
        '作品喜欢量': [i['counts']['displayLike'] for i in work],
        '作品评论量': [i['counts']['displayComment'] for i in work],
        '作品类型': [i['workType'] for i in work],
        '作品地址': shipin,
    }
    return dic


def main():
    # 这里写作者id
    uid = ['3xwi8eeif9kgjcu',]
    for i in uid:
        print('正在爬取{}的主页作品。。。'.format(i))
        dic = data(i)
        df = pd.DataFrame(dic)
        df.to_excel(dic['作者昵称'][1] + ".xls")
    print("======================完成=========================")


if __name__ == '__main__':
    main()

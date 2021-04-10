import requests, json, re

profile_url = "https://live.kuaishou.com/profile/"
data_url = "https://live.kuaishou.com/m_graphql"
work_url = "https://live.kuaishou.com/u/"
param_did = "?did=web_0897bf2eb33014d08a0a7064fd41c899"
zhuye = "https://live.kuaishou.com/profile/"

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
               "query": "query privateFeedsQuery($principalId: String, $pcursor: String, $count: Int) {\n  privateFeeds(principalId: $principalId, pcursor: $pcursor, count: $count) {\n    pcursor\n    list {\n      id\n      thumbnailUrl\n      poster\n      workType\n      type\n      useVideoPlayer\n      imgUrls\n      imgSizes\n      magicFace\n      musicName\n      caption\n      location\n      liked\n      onlyFollowerCanComment\n      relativeHeight\n      timestamp\n      width\n      height\n      counts {\n        displayView\n        displayLike\n        displayComment\n        __typename\n      }\n      user {\n        id\n        eid\n        name\n        avatar\n        __typename\n      }\n      expTag\n      __typename\n    }\n    __typename\n  }\n}\n"
               }
    res = requests.post(data_url, headers=headers, json=payload)
    print(len(json.loads(res.content.decode())['data']['privateFeeds']['list']))


def requ(uid):
    res = requests.get(zhuye + uid, headers=headers, allow_redirects=False).text
    page_data = re.findall(r'<script>window\.__APOLLO_STATE__=(\{.*?\})</script>', res)
    if not page_data:
        return 0

    try:
        page_data = json.loads(page_data[0])
        print(page_data)
    except Exception:
        print('kuaishou loads json failed')
        return 0


def main():
    uids = ['yih7777777', ]
    l = 'wudadala'
    for i in uids:
        # crawl_user(i)
        requ(i)


if __name__ == '__main__':
    main()

import requests
import json
import time


def requs_data(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0'
                          '; WOW64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/70.'
                          '0.3538.25 Safari/537.36 Core/1.'
                          '70.3732.400 QQBrowser/10.5.3819.400'
        }
        respons = requests.get(url=url, headers=headers)
        if respons.status_code == 200:
            return respons.json()
    except RecursionError:
        print('请求失败')


def json_dispose(json_url):
    data = json.loads(requs_data(json_url))  # 格式化json文件
    number = data['data']['page']['count'] // data['data']['page']['size']  # 提取属性值
    for i in range(1, number + 2):
        url = json_url.format(i)
        data1 = json.loads(requs_data(url))
        data2 = data1['data']['replies']  # 提取data里面的属性值
        for u in data2:
            unames = []
            messages = []
            uname = u['member']['uname']
            message = u['content']['message']
            unames.append(uname)
            messages.append(message)
            ass = dict(zip(unames, messages))  # 将两个列表拼接成一个字典
            if u['replies'] == None:
                continue
        print("第{}页爬取完成".format(i))
        return ass




def main():
    url = 'https://api.bilibili.com/x/v2/reply?pn={}&type=1&oid=68434586&sort=2&_=1575370605527'
    urlq = url.format(1)
    data = requs_data(urlq)
    number = data['data']['page']['count'] // data['data']['page']['size']  # 提取属性值
    for i in range(1, number + 2):
        urlu = url.format(i)
        data1 = requs_data(urlu)
        data2 = data1['data']['replies']  # 提取data里面的属性值
        for u in data2:
            unames = []
            messages = []
            uname = u['member']['uname']
            message = u['content']['message']
            unames.append(uname)
            messages.append(message)
            if u['replies'] == None:
                continue
            for w in u['replies']:
                message = w['content']['message']
                uname = w['member']['uname']
        print("第{}页爬取完成".format(i))


if __name__ == '__main__':
    main()
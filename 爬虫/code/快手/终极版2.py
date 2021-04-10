import json
import requests

#设置请求
ID = "3xrptqgjk98rism"
photoID = "3xw28sc864d8p2e"
# URL = 'https://live.kuaishou.com/u/'+ID+'/'+photoID


headers = {
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
}
URL = 'https://live.kuaishou.com/profile/wudadala'
#获取某个ID用户的作品photoID
# res = requests.get(URL, headers=headers)
# print(res.text)
#PyQuery解析
# html = pq(res.text)

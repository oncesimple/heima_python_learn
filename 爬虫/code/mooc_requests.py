import requests
import json
import time
import re
import random

def get_title_reply(uid, fi, http):
    url = 'https://www.icourse163.org/dwr/call/plaincall/PostBean.getPaginationReplys.dwr'
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-length': '249',
        'content-type': 'text/plain',
        'cookie': '',
        'origin': 'https://www.icourse163.org',
        'referer': 'https://www.icourse163.org/learn/WHUT-1002576003?tid=1206076258',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    }
    data = {
        'httpSessionId': '611437146dd0453d8a7093bfe8f44f17',
        'scriptSessionId': '${scriptSessionId}190',
        'c0-scriptName': 'PostBean',
        'c0-methodName': 'getPaginationReplys',
        'c0-id': 0,
        'callCount': 1,
        # 根据主题楼主的 id 检索回复内容
        'c0-param0': 'number:' + str(uid),
        'c0-param1': 'string:2',
        'c0-param2': 'number:1',
        'batchId': round(time.time() * 1000),
    }
    res = requests.post(url, data=data, headers=headers, proxies=http)
    # js 代码末尾给出回复总数，当前页码等信息。
    totle_count = int(re.findall("totalCount:(.*?)}", res.text)[0])
    try:
        if totle_count:
            begin_reply = int(re.findall("dataList:(.*?),", res.text)[0][1:]) + 1
            for i in range(begin_reply, begin_reply + totle_count):
                content_re ='s{}.content="(.*?)";'.format(i)
                content = re.findall(content_re, res.text)[0]
                # print(content.encode().decode('unicode-escape'))
                fi.write('\t' + content.encode().decode('unicode-escape') + '\n')
                # time.sleep(1)
    except Exception:
        print('回复内容写入错误！')



def get_response(course_name, url, page_index):

    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-length': '333',
        'content-type': 'text/plain',
        'cookie': '',
        'origin': 'https://www.icourse163.org',
        'referer': 'https://www.icourse163.org/learn/WHUT-1002576003?tid=1206076258',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',

    }
    data = {
        'httpSessionId': '611437146dd0453d8a7093bfe8f44f17',
        'scriptSessionId': '${scriptSessionId}190',
        'c0-scriptName': 'PostBean',
        'c0-methodName': 'getAllPostsPagination',
        'c0-id': 0,
        'callCount': 1,
        # 课程 id
        'c0-param0': 'number:1206076258',
        'c0-param1': 'string:',
        'c0-param2': 'number:1',
        # 当前页码
        'c0-param3': 'string:' + str(page_index),
        # 页码内容量
        'c0-param4': 'number:20',
        'c0-param5': 'boolean:false',
        'c0-param6': 'null:null',
        # 毫秒级时间戳
        'batchId': round(time.time() * 1000),
    }
    # 代理 IP
    proxy = [
        {
            'http': 'http://119.179.132.94:8060',
            'https': 'https://221.178.232.130:8080',
        },
        {
            'http': 'http://111.29.3.220:8080',
            'https': 'https://47.110.130.152:8080',
        },
        {
            'http': 'http://111.29.3.185:8080',
            'https': 'https://47.110.130.152:8080',
        },
        {
            'http': 'http://111.29.3.193:8080',
            'https': 'https://47.110.130.152:8080',
        },
        {
            'http': 'http://39.137.69.10:8080',
            'https': 'https://47.110.130.152:8080',
        },
    ]
    http = random.choice(proxy)
    is_end = False
    try:
        res = requests.post(url, data=data, headers=headers, proxies=http)
        # 评论从 S** 开始，js 代码末尾信息分析
        response_result = re.findall("results:(.*?)}", res.text)[0]
    except Exception:
        print('开头就错，干啥！')
    if response_result == 'null':
        is_end = True
    else:
        try:
            begin_title = int(response_result[1:]) + 1
            with open(course_name+'.txt', 'a', encoding='utf-8') as fi:
                for i in range(begin_title, begin_title + 21):
                    user_id_re = 's{}.id=([0-9]*?);'.format(str(i))
                    title_re = 's{}.title="(.*?)";'.format(str(i))
                    title_introduction_re = 's{}.shortIntroduction="(.*?)"'.format(str(i))
                    title = re.findall(title_re, res.text)
                    if len(title):
                        user_id = re.findall(user_id_re, res.text)
                        title_introduction = re.findall(title_introduction_re, res.text)
                        # print(f'user_id={user_id[0]},title={(title[0]).encode().decode("unicode-escape")}')
                        fi.write((title[0]).encode().decode("unicode-escape") + '\n')
                        # 主题可能未进行描述
                        if len(title_introduction):
                            # print(title_introduction[0].encode().decode("unicode-escape"))
                            fi.write('\t' + (title_introduction[0]).encode().decode("unicode-escape") + '\n')
                            get_title_reply(user_id[0], fi, random.choice(proxy))
        except Exception:
            print('主题写入错误！')
    return is_end

def get_pages_comments():
    url = 'https://www.icourse163.org/dwr/call/plaincall/PostBean.getAllPostsPagination.dwr'
    page_index = 1
    course_name = "lisanjiegou"
    while(True):
        # time.sleep(1)
        is_end = get_response(course_name, url, page_index)
        if is_end:
            break
        else:
            print('第{}页写入完成!'.format(page_index))
            page_index += 1

if __name__ == '__main__':
    start_time = time.time()
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time)))
    get_pages_comments()
    end_time = time.time()
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time)))
    print('用时{}秒!'.format(end_time - start_time))

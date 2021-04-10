import pandas as pd
import requests
from pyecharts.charts import Bar
from pyecharts import options as opts
# 内置主题类型可查看 pyecharts.globals.ThemeType
from pyecharts.globals import ThemeType
from pyecharts.faker import Faker
from pyecharts.commons.utils import JsCode
import time
import random


def request(url):
    cookies = {
        'historystock': 'HK0667^%^7C*^%^7CHK0270',
        'v': 'Aj5yzI7z7LDIMziUF_2zQZ6bj1-DfwIMlEK29ehHqHx9WdDJUA9SCWTTBu-7',
    }

    headers = {
        'Connection': 'keep-alive',
        'Accept': 'text/html, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'hexin-v': 'Aj5yzI7z7LDIMziUF_2zQZ6bj1-DfwIMlEK29ehHqHx9WdDJUA9SCWTTBu-7',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'Referer': 'http://data.10jqka.com.cn/hgt/ggtb/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7,en-CN;q=0.6',
    }

    response = requests.get(url, headers=headers, cookies=cookies, verify=False)
    return response.text


def text_echars1(merchant, list, file):
    ba = Bar()
    ba.add_xaxis([i for i in list[0]])
    ba.add_yaxis('昨收', [i for i in list[1]], category_gap="60%")
    ba.set_series_opts(itemstyle_opts={
        "normal": {
            "color": JsCode("""new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                offset: 0,
                color: 'rgba(0, 244, 255, 1)'
            }, {
                offset: 1,
                color: 'rgba(0, 77, 167, 1)'
            }], false)"""),
            "barBorderRadius": [30, 30, 30, 30],
            "shadowColor": 'rgb(0, 160, 221)',
        }})
    ba.set_global_opts(
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
        title_opts=opts.TitleOpts(title=merchant),
    )
    ba.render(file)


def text_echars(merchant, list, file):
    bar = Bar()
    bar.add_xaxis(list[0])
    bar.add_yaxis("商家A", list[1])
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title=merchant),
        datazoom_opts=opts.DataZoomOpts(),
    )
    bar.render(file)


def requests_pandas(url):
    data = pd.read_html(request(url))
    l = [i[0] for i in [list(i) for i in data[:1][0]]]

    df = pd.DataFrame(data[0])
    df.columns = l
    return df


def main():
    urls = ['http://data.10jqka.com.cn/hgt/ggtb/field/zdf/order/desc/page/{}/ajax/1/'.format(i) for i in range(1, 5)]
    dataFrames = []
    for i in urls:
        time.sleep(2)
        print('正在请求：' + i)
        dataFrames.append(requests_pandas(i))
        time.sleep(random.randint(5, 10))
    dataFrame = pd.concat(dataFrames)
    df = pd.DataFrame(dataFrame)
    df.to_excel('hello.xls', index=False)
    print(dataFrame)
    print('Done!')


if __name__ == '__main__':
    main()

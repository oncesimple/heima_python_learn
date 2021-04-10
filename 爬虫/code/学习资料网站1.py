import requests
from lxml import etree


def reque(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10'
                      '.0; Win64; x64) AppleWebKi'
                      't/537.36 (KHTML, like Gec'
                      'ko) Chrome/78.0.3904.70 S'
                      'afari/537.36'
    }
    rewew = requests.get(url, headers=headers)
    print(rewew.status_code)
    if rewew.status_code == 200:
        print("网页请求成功，马上爬取网页")
    else:
        print("网页请求异常")
    html = etree.HTML(rewew.text)
    print(html.xpath("//a[@href]/text()"))
    print(html.xpath("//a/@href"))
    
    return 0


def main():
    url = "http://www.xuexi111.org/"

    print(reque(url))


if __name__ == '__main__':
    main( )

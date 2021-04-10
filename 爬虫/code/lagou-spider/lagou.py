import requests
import math
import pandas as pd
import time


def get_json(url):
    headers={
        "User-Agent":"Mozilla/5.0"
                     " (Windows NT 10.0; W"
                     "in64; x64) AppleWebKit/"
                     "537.36 (KHTML, like Ge"
                     "cko) Chrome/78.0.3904."
                     "70 Safari/537.36"
    }
    res = requests.get(url,headers)
    print(res.text())

if __name__ == '__main__':
    get_json("https://www.douban.com")
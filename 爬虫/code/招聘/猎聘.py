#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'hyh'
__date__ = '2020/3/27 16:07'
import request as rq
import analysis as aa


def urls():
    return ['https://www.liepin.com/zhaopin/?init=-1&headckid=2df011695d29c20d&fromSearchBtn=2&ckid=2df011695d29c20d&degradeFlag=0&sfrom=click-pc_homepage-centre_searchbox-search_new&key=python&siTag=I-7rQ0e90mv8a37po7dV3Q%7EfA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_fp&d_ckId=7471caaf93f86da682c325e0c484faec&d_curPage=2&d_pageSize=40&d_headId=7471caaf93f86da682c325e0c484faec&curPage='+str(i) for i in range(10)]


def main():
    url = 'https://www.liepin.com/zhaopin/?init=-1&headckid=2df011695d29c20d&fromSearchBtn=2&ckid=2df011695d29c20d&degradeFlag=0&sfrom=click-pc_homepage-centre_searchbox-search_new&key=python&siTag=I-7rQ0e90mv8a37po7dV3Q%7EfA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_fp&d_ckId=7471caaf93f86da682c325e0c484faec&d_curPage=2&d_pageSize=40&d_headId=7471caaf93f86da682c325e0c484faec&curPage=0'
    response2 = rq.reuquests_text(url)
    print(response2)
    # 获取所有的url
    all_url = aa.lxml_xpath(response2,'//div[@class="job-info"]/h3/a/@href')
    # 获取职位名称
    job = aa.lxml_xpath(response2, '//*//div[@class="title-info"]/h1/@title')
    print(all_url,job)


if __name__ == '__main__':
    main()

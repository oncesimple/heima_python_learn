#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'hyh'
__date__ = '2020/3/22 14:41'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



job_list = [
    '机器学习 实习',
]
driver = webdriver.Chrome()
base_url = 'https://www.zhipin.com/job_detail/?query={}&scity=101020100&industry=&position='
positions = []

def login():
    driver.get('https://passport.csdn.net/login?code=public')
    print('页面加载完成，请手动验证后输入任意字符')
    input()

def run():
    login()
    for job in job_list:
        url = base_url.format(job)
        items = []
        first_page = True
        while True:
            driver.get(url)
            try:
                # 用于等待下一页的按钮出现后再进行点击
                WebDriverWait(driver=driver, timeout=5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@class="page"]/a[last()]')))
            except:
                # 有可能不存在下一页按钮
                pass
            # 页面加载完毕后 解析页面
            items.extend(parse_list_page(driver, first_page))
            first_page = False
            try:
                next_bt = driver.find_element_by_xpath('//div[@class="page"]/a[last()]')
                # 判断是否到了最后一页
                if "disabled" in next_bt.get_attribute('class'):
                    break
                else:
                    url = next_bt.get_attribute('href')
            except:
                # 有可能不存在下一页按钮
                break
        for item in items:
            request_detail_page(item.link)




def parse_list_page(driver, first_page):
    if first_page:
        links: ElementList = WebDriverWait(driver=driver, timeout=10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@id="main"]/div/div[3]/ul/li')))
    else:
        links: ElementList = WebDriverWait(driver=driver, timeout=10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@id="main"]/div/div[2]/ul/li')))
    items = []
    for temp in links:
        link = temp.find_element_by_xpath('./div/div[1]/h3/a')
        job = link.find_element_by_class_name('job-title').text
        company = temp.find_element_by_class_name('company-text').text
        href = link.get_attribute('href')
        btn = temp.find_element_by_xpath('./div/a')
        if '继续沟通' in btn.get_attribute('innerHTML'):
            print('已投递过', company)
        else:
            item = LagouItem(href, company, job)
            print(item)
            items.append(item)
    return items


def request_detail_page(url):
    # 用新窗口打开页面
    url = url
    driver.get(url)
    # 等待页面加载完成
    WebDriverWait(driver, timeout=10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div[1]/div/div/div[3]/div[1]/a')))
    btn = driver.find_element_by_xpath('//*[@id="main"]/div[1]/div/div/div[3]/div[1]/a')
    if btn.text == '立即沟通':
        print('发现目标，点击投递')
        btn.click()
    elif btn.text == '继续沟通':
        print('已投递过', url)


def main():
    run()


if __name__ == '__main__':
    main()

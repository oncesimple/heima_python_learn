#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'hyh'
__date__ = '2020/3/22 13:03'

from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options


class Boss_spider(object):
    driver_path = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'

    def __init__(self):
        # options是为了防爬虫做的设置
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.driver = webdriver.Chrome(executable_path=self.driver_path, options=self.options)
        self.url = 'https://www.zhipin.com/'

    def run(self, search):
        self.driver.get(self.url)
        inputTag = self.driver.find_element_by_class_name('ipt-search')
        inputTag.send_keys(search)
        inputTag.send_keys(Keys.RETURN)  # 用按钮用不了,用回车替代
        time.sleep(0.5)
        self.driver.find_element_by_link_text('杭州').click()  # 切换城市

        while True:
            self.parser_list_page()
            # 是否还有下一页的判断
            if self.driver.page_source.find('next disabled') != -1:
                break
            else:
                self.driver.find_element_by_class_name('next').click()
                time.sleep(1)

    # 解析得到每个职位的url
    def parser_list_page(self):
        source = BeautifulSoup(self.driver.page_source, 'html.parser')
        urls = source.find_all('div', class_='job-primary')
        for url in urls:
            pager_url = 'https://www.zhipin.com' + str(url.find('h3', class_='name').a['href'])
            time.sleep(0.5)
            self.request_detail_page(pager_url)

    # 解析具体每个职位的详细信息
    def request_detail_page(self, url):
        # 新建一个网页打开具体每个职位的url
        self.driver.execute_script("window.open('%s')" % url)
        self.driver.switch_to.window(self.driver.window_handles[1])

        source = BeautifulSoup(self.driver.page_source, 'html.parser')
        position_info = source.find('div', class_='info-primary')

        position_name = position_info.find('div', class_='name').find('h1').string  # 职位名称
        position_salary = position_info.find('span', class_='salary').string  # 职位薪水
        position_city = position_info.find('p').get_text()  # 工作城市
        position_work_years = position_info.find_all('em', class_='dolt')[0].get_text()  # 工作经验
        position_education = position_info.find_all('em', class_='dolt')[1].get_text()  # 学历
        print(position_name, position_salary, position_city, position_work_years, position_education)
        # 输出工作福利等信息
        welfare = position_info.find('div', class_='job-tags').find_all('span')
        for welfare_info in welfare:
            print(welfare_info.string, end=' ')
        print('\n', '*' * 50)

        # 关闭职位信息的网页，回到列表页
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(1)

def selenium(url):
    # chrome_options = Options()
    # chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    # chrome_options.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
    # chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    # chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    # chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    # chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    # # chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"  # 手动指定本机电脑使用的浏览器位置
    #
    # # 创建一个driver,进行后面的请求页面等操作，executable_path指定本机中chromedriver.exe的位置
    # driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe" )
    driver = webdriver.Chrome(
        executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")  # executable_path为chromedriver.exe的解压安装目录，需要与chrome浏览器同一文件夹下
    # driver = webdriver.Chrome(executable_path=r"D:\chromedriver.exe")  # executable_path为chromedriver.exe的解压安装目录，需要与chrome浏览器同一文件夹下

    # 举例1：使用driver去请求页面
    driver.get(url)

    # 举例2：driver去填写用户名和密码进行模拟登陆
    # driver.find_element_by_id("loginform-username").send_keys("dongyuqin")
    driver.find_element_by_name("phone").send_keys('17609209703')
    driver.find_element_by_xpath('//*[@id="wrap"]/div[3]/div/div[1]/form/div/div[2]/a').click()
    button = driver.find_element_by_xpath('//*[@id="nc_7_n1z"]')  # 找到“蓝色滑块”
    action = ActionChains(driver)  # 实例化一个action对象
    action.click_and_hold(button).perform()  # perform()用来执行ActionChains中存储的行为
    action.reset_actions()
    action.move_by_offset(180, 0).perform()  # 移动滑块
    yanzhengma = input('请输入你的验证码:')
    driver.find_element_by_name('phoneCode').send_keys(yanzhengma)
    driver.find_element_by_xpath('//*[@id="wrap"]/div[3]/div/div[1]/form/div/button').click()
    # driver.find_element_by_id("loginform-password").send_keys("dongyuqin")
    # driver自动点击登陆按钮
    # driver.find_element_by_xpath("//div[@class='form-group']").click()

    # 举例3: driver自动获取cookie信息，这里可以将cookies添加到cookie池中去循环使用
    cookies = driver.close()
    # 打印获取的cookies信息
    print(cookies)

    # 最后记得关闭driver
    close = driver.close()


def main():
    # selenium('https://www.zhipin.com/')
    Spider = Boss_spider()
    Spider.run('阿里巴巴')

if __name__ == '__main__':
    main()

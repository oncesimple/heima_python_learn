import time
from selenium import webdriver
from lxml import etree
from bs4 import BeautifulSoup

# driver = webdriver.PhantomJS(
#     executable_path=r"E:\ruanjian\phantomjs-2.1.1-windows\bin\phantomjs.exe")  # executable_path为chromedriver.exe的解压安装目录，需要与chrome浏览器同一文件夹下
driver = webdriver.Chrome(executable_path=r"E:\谷歌下载\chromedriver_win32\chromedriver.exe")  # executable_path为chromedriver.exe的解压安装目录，需要与chrome浏览器同一文件夹下
# driver = webdriver.Chrome(executable_path=r"D:\chromedriver.exe")  # executable_path为chromedriver.exe的解压安装目录，需要与chrome浏览器同一文件夹下
driver.get(r'http://wenshu.court.gov.cn/website/wenshu/181217BMTKHNT2W0/index.html?pageId=fceff0d4cef17171ebcebd8c496cb1d8&s8=02')  # 爬取Python语言程序设计
cont = driver.page_source  # 获得初始页面代码，接下来进行简单的解析
# soup = BeautifulSoup(cont, 'html.parser')
# ele = driver.find_element_by_id("review-tag-button")  # 模仿浏览器就行点击查看课程评价的功能
# ele.click()  # 上边的id，下边的classname都可以在源码中看到（首选火狐，谷歌）
# xyy = driver.find_element_by_class_name("ux-pager_btn__next")  # 翻页功能，类名不能有空格，有空格可取后边的部分
# connt = driver.page_source
# acontent = []  # n页的总评论
# # print(len(acontent))
# for i in range(3):  # 翻页 286-0+1次，也就是287次，第一页打开就是，上边读完第一页了
#     xyy.click()  # 调用翻页
#     connt = driver.page_source  # 获取网页
#     html = etree.HTML(connt)  # 创建解析对象
#     time.sleep(5)
#     input()
#     content = html.xpath(
#         r'//div[@class="ux-mooc-comment-course-comment_comment-list_item_body_content"]/span/text()')  # 解析html
#     l = acontent + content  # 列表拼接
# with open(r'pinglun.txt','w',encoding='utf-8')as f:
#     f.write(str(l))
# print(l)
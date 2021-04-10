import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from lxml import etree
from bs4 import BeautifulSoup


def loin():
    option = webdriver.ChromeOptions()
    option.add_argument("start-maximized")
    # option.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', True)
    driver = webdriver.Chrome(options=option)
    driver.execute_script('Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});')
    driver.implicitly_wait(10)
    # driver.maximize_window()
    # input('hhhhhh')

    # 访问登录页面
    driver.get("https://passport.csdn.net/account/login?ref=toolbar")
    # 保存登录页面截图
    driver.save_screenshot("csdn1.png")
    zhanghaodenglu = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div[5]/ul/li[3]')
    zhanghaodenglu = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div[5]/ul/li[2]')
    action = ActionChains(driver)
    action.move_to_element(zhanghaodenglu).click()
    action.perform()
    zhanghao = driver.find_element_by_xpath('//div[@class="col-xs-7 col-sm-7 control-col-pos col-pr-no form-control-phone"]/input[1]')
    # 获取登录 用户输入框、密码输入框
    action.move_to_element(zhanghao).click(zhanghao)
    zhanghao.send_keys('1')
    zhanghao.send_keys('17609209703')
    dianjiyanzhen = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[2]/div[5]/div/div[4]/div/button')
    action.move_to_element(dianjiyanzhen).click(dianjiyanzhen)
    u_name = driver.find_element_by_name('all').send_keys('17609209703')
    yanzhengma = input('请输入验证码：')
    action.perform()
    p_word = driver.find_element_by_id("password-number").send_keys("hyh17609209703")
    # input('jj')
    # 模拟点击登录
    login_btn = driver.find_element_by_class_name('btn btn-primary')
    action.perform( )
    login_btn.click( )
    # 保存登录后的截图
    # driver.save_screenshot("csdn2.png")
    # 保存数据
    # with open("csdn.html", "w") as f:
        # f.write(driver.page_source.encode("utf-8"))

    # 退出浏览器
    driver.quit( )


def main():
    loin()


if __name__ == '__main__':
    main()
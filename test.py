from selenium import webdriver
from selenium.webdriver.common.by import By

def find(path):
    global driver
    return driver.find_element(by=By.XPATH, value=path).text

url = 'https://www.lottery.gov.cn/jc/zqgdjj/?m=060248'
# 构建驱动
driver = webdriver.Chrome()
# 前往网站
driver.get(url)

print(find('//*[@id="rs_tb"]/tr[1]/td[1]/strong'))
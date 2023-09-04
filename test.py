from selenium import webdriver
from selenium.webdriver.common.by import By

def find(path):
    global driver
    return driver.find_element(by=By.XPATH, value=path).text

url = 'https://www.lottery.gov.cn/jc/zqgdjj/?m=60001'
# 构建驱动
driver = webdriver.Chrome()
# 前往网站
driver.get('https://www.lottery.gov.cn/jc/zqgdjj/?m=60001')

print(len(driver.find_elements(by=By.XPATH, value='//*[@id="hafu_tb"]/tr')))
import pandas as pd
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from exts import db
from models import *
from datetime import datetime
from app import app
from data_collect import find, find_game, find_rang, find_half, find_simple, find_goals

option = webdriver.ChromeOptions()
option.headless = True
# 构建驱动
driver = webdriver.Chrome(options=option)
# 前往网站
driver.get('https://www.lottery.gov.cn/jc/zqgdjj/?m=100487')
# 等待页面渲染
sleep(3)

# 读取数据
df = pd.read_excel('output.xlsx')
try:
    l = len(df)
    for i in range(l):
        url = df['url'].get(i)

        # 新开窗口
        driver.execute_script("window.open('', '_blank');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(url)

        # 切换回初始窗口
        driver.switch_to.window(driver.window_handles[0])
        # 关闭原始窗口
        driver.close()
        sleep(5)
        # 重新定位窗口
        driver.switch_to.window(driver.window_handles[0])

        # 爬取历史奖金信息
        with app.app_context():
            find_game()
            find_simple()
            find_rang()
            find_goals()
            find_half()

        df = df.drop(i)
except:
    df.to_excel('result.xlsx')
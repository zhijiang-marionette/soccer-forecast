from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

# def find(path):
#     global driver
#     return driver.find_element(by=By.XPATH, value=path).text
#
# url = 'https://www.lottery.gov.cn/jc/zqgdjj/?m=100487'
# # 构建驱动
# driver = webdriver.Chrome()
# # 前往网站
# driver.get(url)
#

from models import *
from app import app
import pandas as pd

with app.app_context():
    games = Game.query.with_entities(Game.url).all()
    df = pd.DataFrame(games)
    df.to_excel('output.xlsx', index=False)
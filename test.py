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

import pandas as pd
import numpy as np
from models import *
from app import app

with app.app_context():
    simple_finals = Simple_final.query.with_entities(Simple_final.win_price, Simple_final.draw_price, Simple_final.lose_price).all()
    arr_nx3 = np.array(simple_finals)

import numpy as np

# 创建1x3和3x3的numpy数组
array_1x3 = np.array([1.96, 3.42, 2.97])

# 使用广播计算差值
diff = arr_nx3 - array_1x3.reshape(1, -1)

# 计算每个元素的平方
squared_diff = diff**2

# 沿着第一个轴（axis=1）求和
sum_squared_diff = np.sum(squared_diff, axis=1)

# 对结果开根号，得到欧几里得距离
euclidean_distance = np.sqrt(sum_squared_diff)

# 找到这些元素的索引, 取得是每一个奖金差距在0.04以内
indices_below_threshold = np.where(euclidean_distance < 0.0692)[0] + 1

# 根据索引在数据库中检索
with app.app_context():
    games = Game.query.filter(Game.id.in_(indices_below_threshold)).all()

# 得到比赛结果列表
simples = [game.simple for game in games]

# 计算三种结果比例
total_matches = len(simples)
win_count = simples.count('胜')
draw_count = simples.count('平')
loss_count = simples.count('负')

win_percentage = (win_count / total_matches) * 100
draw_percentage = (draw_count / total_matches) * 100
loss_percentage = (loss_count / total_matches) * 100

print(f'胜利比例：{win_percentage:.2f}%')
print(f'平局比例：{draw_percentage:.2f}%')
print(f'失败比例：{loss_percentage:.2f}%')
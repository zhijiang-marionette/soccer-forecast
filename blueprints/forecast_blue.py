from flask import Blueprint, render_template, request
from exts import db
from models import *
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie, Line
from random import randrange
from calculate import *
import requests
import json

# 创建蓝图模版
forecast_blue = Blueprint('name', __name__)

# 比赛ID
matchId = 0
# 存储爬取奖金返回信息
dict_data = {}
# 奖金信息和盘口变化相似的比赛，运用集合进行存储，避免重复项
similar_games = set()
# 奖金信息和盘口变化相似比赛的结果概率情况，分胜平负和让球两个概率
simple_result = [0, 0, 0]
rang_result = [0, 0, 0]

# 定义视图函数，配置蓝图路由
@forecast_blue.route('/<Id>')
def home(Id):
    global matchId, dict_data
    matchId = Id
    # 发送请求获取网页内容
    url = 'https://webapi.sporttery.cn/gateway/jc/football/getFixedBonusV1.qry?clientCode=3001&matchId=' + str(matchId)
    response = requests.get(url)
    html = response.content

    # 解析返回内容，转换为字典格式
    dict_data = json.loads(html)
    return render_template('forecast.html')

@forecast_blue.route("/simplePie", methods=['GET'])
def get_simple_pie():
    global similar_games
    # 提取奖金信息
    win_price = float(dict_data['value']['oddsHistory']['hadList'][-1]['h'])
    draw_price = float(dict_data['value']['oddsHistory']['hadList'][-1]['d'])
    lose_price = float(dict_data['value']['oddsHistory']['hadList'][-1]['a'])

    data, games = probability_of_simple(win_price, draw_price, lose_price)

    for i in range(len(data)):
        simple_result[0] += data[0][1] * 0.4

    similar_games.update(games)

    p = (
        Pie()
        .add('', data,
             )
    )
    return p.dump_options_with_quotes()


@forecast_blue.route("/rangPie", methods=['GET'])
def get_rang_pie():
    global similar_games
    # 提取奖金信息
    rang_win_price = float(dict_data['value']['oddsHistory']['hhadList'][-1]['h'])
    rang_draw_price = float(dict_data['value']['oddsHistory']['hhadList'][-1]['d'])
    rang_lose_price = float(dict_data['value']['oddsHistory']['hhadList'][-1]['a'])

    data, games = probability_of_rang(rang_win_price, rang_draw_price, rang_lose_price)

    for i in range(len(data)):
        rang_result[0] += data[0][1] * 0.4

    similar_games.update(games)

    p = (
        Pie()
        .add('', data,
             )
    )
    return p.dump_options_with_quotes()


@forecast_blue.route("/simpleChangePie", methods=['GET'])
def get_simple_change_pie():
    global similar_games
    # 提取奖金信息
    win_price = float(dict_data['value']['oddsHistory']['hadList'][-1]['h']) - float(
        dict_data['value']['oddsHistory']['hadList'][0]['h'])
    draw_price = float(dict_data['value']['oddsHistory']['hadList'][-1]['d']) - float(
        dict_data['value']['oddsHistory']['hadList'][0]['d'])
    lose_price = float(dict_data['value']['oddsHistory']['hadList'][-1]['a']) - float(
        dict_data['value']['oddsHistory']['hadList'][0]['a'])

    data, games = probability_of_simpleChange(win_price, draw_price, lose_price)

    for i in range(len(data)):
        simple_result[0] += data[0][1] * 0.6

    similar_games.update(games)

    p = (
        Pie()
        .add('', data,
             )
    )

    return p.dump_options_with_quotes()

@forecast_blue.route("/rangChangePie", methods=['GET'])
def get_rang_change_pie():
    global similar_games
    # 提取奖金信息
    rang_win_price = float(dict_data['value']['oddsHistory']['hhadList'][-1]['h']) - float(
        dict_data['value']['oddsHistory']['hhadList'][0]['h'])
    rang_draw_price = float(dict_data['value']['oddsHistory']['hhadList'][-1]['d']) - float(
        dict_data['value']['oddsHistory']['hhadList'][0]['d'])
    rang_lose_price = float(dict_data['value']['oddsHistory']['hhadList'][-1]['a']) - float(
        dict_data['value']['oddsHistory']['hhadList'][0]['a'])

    data, games = probability_of_rangChange(rang_win_price, rang_draw_price, rang_lose_price)

    for i in range(len(data)):
        rang_result[0] += data[0][1] * 0.6

    similar_games.update(games)

    p = (
        Pie()
        .add('', data,
             )
    )

    return p.dump_options_with_quotes()

@forecast_blue.route("/simpleLine", methods=['GET'])
def get_simple_line():
    temp = dict(x=[], win=[], draw=[], lose=[])

    for i, dic in enumerate(dict_data['value']['oddsHistory']['hadList']):
        temp['x'].append(dic['updateDate'][5::] + ' ' + dic['updateTime'][0:5])
        temp['win'].append(float(dic['h']))
        temp['draw'].append(float(dic['d']))
        temp['lose'].append(float(dic['a']))

    line = (
        Line()
        .add_xaxis(xaxis_data=temp['x'])
        .add_yaxis(series_name='胜', y_axis=temp['win'], symbol='arrow', is_symbol_show=True)
        .add_yaxis(series_name='平', y_axis=temp['draw'], symbol='rect', is_symbol_show=True)
        .add_yaxis(series_name='负', y_axis=temp['lose'])
        .set_global_opts(title_opts=opts.TitleOpts(title='胜平负数据变化图'))
    )

    return line.dump_options_with_quotes()

@forecast_blue.route("/rangLine", methods=['GET'])
def get_rang_line():
    temp = dict(x=[], win=[], draw=[], lose=[])

    for i, dic in enumerate(dict_data['value']['oddsHistory']['hhadList']):
        temp['x'].append(dic['updateDate'][5::] + ' ' + dic['updateTime'][0:5])
        temp['win'].append(float(dic['h']))
        temp['draw'].append(float(dic['d']))
        temp['lose'].append(float(dic['a']))

    line = (
        Line()
        .add_xaxis(xaxis_data=temp['x'])
        .add_yaxis(series_name='胜', y_axis=temp['win'], symbol='arrow', is_symbol_show=True)
        .add_yaxis(series_name='平', y_axis=temp['draw'], symbol='rect', is_symbol_show=True)
        .add_yaxis(series_name='负', y_axis=temp['lose'])
        .set_global_opts(title_opts=opts.TitleOpts(title='让球数据变化图'))
    )

    return line.dump_options_with_quotes()
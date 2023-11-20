from flask import Blueprint, render_template, request
from exts import db
from models import *
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie
from random import randrange
from calculate import *
import requests
import json

# 创建蓝图模版
forecast_blue = Blueprint('name', __name__)


# 定义视图函数，配置蓝图路由
@forecast_blue.route('/')
def home():
    return render_template('forecast.html')


def bar_base() -> Bar:
    c = (
        Bar()
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [randrange(0, 100) for _ in range(6)])
        .add_yaxis("商家B", [randrange(0, 100) for _ in range(6)])
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    return c


def simple_pie(data: list) -> Pie:
    p = (
        Pie()
        .add('', data,
             )
        # .set_global_opts(title_opts=opts.TitleOpts(title="胜平负比例图"))
        # .set_global_opts(legend_opts=opts.LegendOpts(is_show=False))  # 不显示图示
    )

    return p


def rang_pie(data: list) -> Pie:
    p = (
        Pie()
        .add('', data,
             )
        # .set_global_opts(title_opts=opts.TitleOpts(title="让胜平负比例图"))
        # .set_global_opts(legend_opts=opts.LegendOpts(is_show=False))  # 不显示图示
    )

    return p


@forecast_blue.route("/barChart")
def get_bar_chart():
    c = bar_base()
    return c.dump_options_with_quotes()


@forecast_blue.route("/simplePie", methods=['GET'])
def get_simple_pie():
    # 获取参数
    matchId = request.args.get('matchId')
    # 发送请求获取网页内容
    url = 'https://webapi.sporttery.cn/gateway/jc/football/getFixedBonusV1.qry?clientCode=3001&matchId=' + str(matchId)
    response = requests.get(url)
    html = response.content

    # 解析返回内容，转换为字典格式
    dict_data = json.loads(html)

    # 提取奖金信息
    win_price = float(dict_data['value']['oddsHistory']['hadList'][-1]['h'])
    draw_price = float(dict_data['value']['oddsHistory']['hadList'][-1]['d'])
    lose_price = float(dict_data['value']['oddsHistory']['hadList'][-1]['a'])

    data = probability_of_simple(win_price, draw_price, lose_price)

    p = simple_pie(data)
    return p.dump_options_with_quotes()


@forecast_blue.route("/rangPie", methods=['GET'])
def get_rang_pie():
    # 获取参数
    matchId = request.args.get('matchId')
    # 发送请求获取网页内容
    url = 'https://webapi.sporttery.cn/gateway/jc/football/getFixedBonusV1.qry?clientCode=3001&matchId=' + str(matchId)
    response = requests.get(url)
    html = response.content

    # 解析返回内容，转换为字典格式
    dict_data = json.loads(html)

    # 提取奖金信息
    rang_win_price = float(dict_data['value']['oddsHistory']['hhadList'][-1]['h'])
    rang_draw_price = float(dict_data['value']['oddsHistory']['hhadList'][-1]['d'])
    rang_lose_price = float(dict_data['value']['oddsHistory']['hhadList'][-1]['a'])

    data = probability_of_rang(rang_win_price, rang_draw_price, rang_lose_price)

    p = rang_pie(data)
    return p.dump_options_with_quotes()


@forecast_blue.route("/simpleChangePie", methods=['GET'])
def get_simple_change_pie():
    # 获取参数
    matchId = request.args.get('matchId')
    # 发送请求获取网页内容
    url = 'https://webapi.sporttery.cn/gateway/jc/football/getFixedBonusV1.qry?clientCode=3001&matchId=' + str(matchId)
    response = requests.get(url)
    html = response.content

    # 解析返回内容，转换为字典格式
    dict_data = json.loads(html)

    # 提取奖金信息
    win_price = float(dict_data['value']['oddsHistory']['hadList'][-1]['h']) - float(
        dict_data['value']['oddsHistory']['hadList'][0]['h'])
    draw_price = float(dict_data['value']['oddsHistory']['hadList'][-1]['d']) - float(
        dict_data['value']['oddsHistory']['hadList'][0]['d'])
    lose_price = float(dict_data['value']['oddsHistory']['hadList'][-1]['a']) - float(
        dict_data['value']['oddsHistory']['hadList'][0]['a'])

    data = probability_of_simpleChange(win_price, draw_price, lose_price)

    p = simple_pie(data)
    return p.dump_options_with_quotes()

@forecast_blue.route("/rangChangePie", methods=['GET'])
def get_rang_change_pie():
    # 获取参数
    matchId = request.args.get('matchId')
    # 发送请求获取网页内容
    url = 'https://webapi.sporttery.cn/gateway/jc/football/getFixedBonusV1.qry?clientCode=3001&matchId=' + str(matchId)
    response = requests.get(url)
    html = response.content

    # 解析返回内容，转换为字典格式
    dict_data = json.loads(html)

    # 提取奖金信息
    rang_win_price = float(dict_data['value']['oddsHistory']['hhadList'][-1]['h']) - float(
        dict_data['value']['oddsHistory']['hhadList'][0]['h'])
    rang_draw_price = float(dict_data['value']['oddsHistory']['hhadList'][-1]['d']) - float(
        dict_data['value']['oddsHistory']['hhadList'][0]['d'])
    rang_lose_price = float(dict_data['value']['oddsHistory']['hhadList'][-1]['a']) - float(
        dict_data['value']['oddsHistory']['hhadList'][0]['a'])

    data = probability_of_rangChange(rang_win_price, rang_draw_price, rang_lose_price)

    p = rang_pie(data)
    return p.dump_options_with_quotes()
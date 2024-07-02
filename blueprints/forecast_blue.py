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

# 定义视图函数，配置蓝图路由
@forecast_blue.route('/<Id>', methods=['GET'])
def home(Id):
    global matchId, dict_data
    # 奖金信息和盘口变化相似的比赛
    similar_games = []
    # 奖金信息和盘口变化相似比赛的结果概率情况，分胜平负和让球两个概率
    simple_result = [0, 0, 0]
    rang_result = [0, 0, 0]
    matchId = Id

    # 发送请求获取网页内容
    url = 'https://webapi.sporttery.cn/gateway/jc/football/getFixedBonusV1.qry?clientCode=3001&matchId=' + str(matchId)
    response = requests.get(url)
    html = response.content

    # 解析返回内容，转换为字典格式
    dict_data = json.loads(html)

    # -----------------------------------------胜平负奖金相似（实时）比赛-----------------------------------------
    # 提取奖金信息
    win_price, draw_price, lose_price = 0, 0, 0
    if dict_data['value']['oddsHistory']['hadList']:
        win_price = float(dict_data['value']['oddsHistory']['hadList'][-1]['h'])
        draw_price = float(dict_data['value']['oddsHistory']['hadList'][-1]['d'])
        lose_price = float(dict_data['value']['oddsHistory']['hadList'][-1]['a'])

    data, games = probability_of_simple(win_price, draw_price, lose_price, False)

    sorted_games = sorted(games, key = lambda game: game.game_time, reverse=True)

    if len(sorted_games) > 10:
        sorted_games = sorted_games[0:10]

    for i in range(len(data)):
        simple_result[i] += data[i][1]

    similar_games.extend(sorted_games)

    slp = (
        Pie()
        .add('', data,
             )
    ).dump_options_with_quotes()

    # -----------------------------------------胜平负奖金相似（初盘）比赛-----------------------------------------
    # 提取奖金信息
    win_price, draw_price, lose_price = 0, 0, 0
    if dict_data['value']['oddsHistory']['hadList']:
        win_price = float(dict_data['value']['oddsHistory']['hadList'][0]['h'])
        draw_price = float(dict_data['value']['oddsHistory']['hadList'][0]['d'])
        lose_price = float(dict_data['value']['oddsHistory']['hadList'][0]['a'])

    data, games = probability_of_simple(win_price, draw_price, lose_price, True)

    sorted_games = sorted(games, key = lambda game: game.game_time, reverse=True)

    if len(sorted_games) > 10:
        sorted_games = sorted_games[0:10]

    for i in range(len(data)):
        simple_result[i] += data[i][1]

    similar_games.extend(sorted_games)

    sfp = (
        Pie()
        .add('', data,
             )
    ).dump_options_with_quotes()

    # ---------------------------------------让球胜平负奖金相似（实时）比赛---------------------------------------
    # 提取奖金信息
    rang_win_price = float(dict_data['value']['oddsHistory']['hhadList'][-1]['h'])
    rang_draw_price = float(dict_data['value']['oddsHistory']['hhadList'][-1]['d'])
    rang_lose_price = float(dict_data['value']['oddsHistory']['hhadList'][-1]['a'])

    data, games = probability_of_rang(rang_win_price, rang_draw_price, rang_lose_price, False, int(dict_data['value']['oddsHistory']['hhadList'][-1]['goalLine']))

    sorted_games = sorted(games, key=lambda game: game.game_time, reverse=True)

    if len(sorted_games) > 10:
        sorted_games = sorted_games[0:10]

    for i in range(len(data)):
        rang_result[i] += data[i][1]

    similar_games.extend(sorted_games)

    rlp = (
        Pie()
        .add('', data,
             )
    ).dump_options_with_quotes()

    # ---------------------------------------让球胜平负奖金相似（初盘）比赛---------------------------------------
    # 提取奖金信息
    rang_win_price = float(dict_data['value']['oddsHistory']['hhadList'][0]['h'])
    rang_draw_price = float(dict_data['value']['oddsHistory']['hhadList'][0]['d'])
    rang_lose_price = float(dict_data['value']['oddsHistory']['hhadList'][0]['a'])

    data, games = probability_of_rang(rang_win_price, rang_draw_price, rang_lose_price, True, int(dict_data['value']['oddsHistory']['hhadList'][-1]['goalLine']))

    sorted_games = sorted(games, key=lambda game: game.game_time, reverse=True)

    if len(sorted_games) > 10:
        sorted_games = sorted_games[0:10]

    for i in range(len(data)):
        rang_result[i] += data[i][1]

    similar_games.extend(sorted_games)

    rfp = (
        Pie()
        .add('', data,
             )
    ).dump_options_with_quotes()

    # # ---------------------------------------胜平负奖金变化相似比赛---------------------------------------
    # # 提取奖金信息
    # win_price = float(dict_data['value']['oddsHistory']['hadList'][-1]['h']) - float(
    #     dict_data['value']['oddsHistory']['hadList'][0]['h'])
    # draw_price = float(dict_data['value']['oddsHistory']['hadList'][-1]['d']) - float(
    #     dict_data['value']['oddsHistory']['hadList'][0]['d'])
    # lose_price = float(dict_data['value']['oddsHistory']['hadList'][-1]['a']) - float(
    #     dict_data['value']['oddsHistory']['hadList'][0]['a'])
    #
    # data, games = probability_of_simpleChange(win_price, draw_price, lose_price)
    #
    # # sorted_games = sorted(games, key = lambda game: game.game_time, reverse=True)
    # #
    # # if len(sorted_games) > 20:
    # #     sorted_games = sorted_games[0:20]
    #
    # for i in range(len(data)):
    #     simple_result[i] += data[i][1] * 0.6
    #
    # # similar_games.update(sorted_games)
    #
    # scp = (
    #     Pie()
    #     .add('', data,
    #          )
    # ).dump_options_with_quotes()
    #
    # # -------------------------------------让球胜平负奖金变化相似比赛-------------------------------------
    # # 提取奖金信息
    # rang_win_price = float(dict_data['value']['oddsHistory']['hhadList'][-1]['h']) - float(
    #     dict_data['value']['oddsHistory']['hhadList'][0]['h'])
    # rang_draw_price = float(dict_data['value']['oddsHistory']['hhadList'][-1]['d']) - float(
    #     dict_data['value']['oddsHistory']['hhadList'][0]['d'])
    # rang_lose_price = float(dict_data['value']['oddsHistory']['hhadList'][-1]['a']) - float(
    #     dict_data['value']['oddsHistory']['hhadList'][0]['a'])
    #
    # data, games = probability_of_rangChange(rang_win_price, rang_draw_price, rang_lose_price)
    #
    # # sorted_games = sorted(games, key = lambda game: game.game_time, reverse=True)
    # #
    # # if len(sorted_games) > 20:
    # #     sorted_games = sorted_games[0:20]
    #
    # for i in range(len(data)):
    #     rang_result[i] += data[i][1] * 0.6
    #
    # # similar_games.update(sorted_games)
    #
    # rcp = (
    #     Pie()
    #     .add('', data,
    #          )
    # ).dump_options_with_quotes()

    # -------------------------------------胜平负奖金变化趋势-------------------------------------
    temp = dict(x=[], win=[], draw=[], lose=[])

    for i, dic in enumerate(dict_data['value']['oddsHistory']['hadList']):
        temp['x'].append(dic['updateDate'][5::] + ' ' + dic['updateTime'][0:5])
        temp['win'].append(float(dic['h']))
        temp['draw'].append(float(dic['d']))
        temp['lose'].append(float(dic['a']))

    sl = (
        Line()
        .add_xaxis(xaxis_data=temp['x'])
        .add_yaxis(series_name='胜', y_axis=temp['win'], symbol='arrow', is_symbol_show=True)
        .add_yaxis(series_name='平', y_axis=temp['draw'], symbol='rect', is_symbol_show=True)
        .add_yaxis(series_name='负', y_axis=temp['lose'])
        .set_global_opts(title_opts=opts.TitleOpts(title='胜平负数据变化图'))
    ).dump_options_with_quotes()

    # -------------------------------------让球奖金变化趋势-------------------------------------
    temp = dict(x=[], win=[], draw=[], lose=[])

    for i, dic in enumerate(dict_data['value']['oddsHistory']['hhadList']):
        temp['x'].append(dic['updateDate'][5::] + ' ' + dic['updateTime'][0:5])
        temp['win'].append(float(dic['h']))
        temp['draw'].append(float(dic['d']))
        temp['lose'].append(float(dic['a']))

    rl = (
        Line()
        .add_xaxis(xaxis_data=temp['x'])
        .add_yaxis(series_name='胜', y_axis=temp['win'], symbol='arrow', is_symbol_show=True)
        .add_yaxis(series_name='平', y_axis=temp['draw'], symbol='rect', is_symbol_show=True)
        .add_yaxis(series_name='负', y_axis=temp['lose'])
        .set_global_opts(title_opts=opts.TitleOpts(title='让球数据变化图'))
    ).dump_options_with_quotes()

    # ---------------------------------------------------------------------------------------
    similarGames = json.dumps([{
        'id':game.id,
        'dan':game.dan,
        'host':Team.query.filter_by(id=game.host_id).first().name,
        'guest':Team.query.filter_by(id=game.guest_id).first().name,
        'game_time':game.game_time.strftime('%Y-%m-%d %H:%M:%S'),
        'session':game.session,
        'simple':game.simple,
        'rang':game.rang,
        'score':game.score,
        'goals':game.goals,
        'half':game.half,
        'url':game.url
    } for game in similar_games])

    return render_template('forecast.html', simpleFirstPie = sfp, rangFirstPie = rfp, simpleLastPie = slp, rangLastPie = rlp, simpleLine = sl, rangLine = rl, similarGames=similarGames)
    # return render_template('forecast.html', simplePie = sp, rangPie = rp, simpleChangePie = scp, rangChangePie = rcp, simpleLine = sl, rangLine = rl)
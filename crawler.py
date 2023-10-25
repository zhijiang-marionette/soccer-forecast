import requests
import json
from models import *
from datetime import datetime
from app import app

# 爬取竞彩网开的赛事，并汇总成列表
def get_game_list() -> list:
    # 发送请求获取网页内容
    url = 'https://webapi.sporttery.cn/gateway/jc/football/getMatchListV1.qry?clientCode=3001'
    response = requests.get(url)
    html = response.content

    # 解析返回内容，转换为字典格式
    dict_data = json.loads(html)

    res = []

    for item in dict_data['value']['matchInfoList']:
        for dic in item['subMatchList']:
            game = dict(matchNum=dic['matchNum'], league=dic['leagueAllName'],
                        team=dic['homeTeamAllName'] + 'vs' + dic['awayTeamAllName'],
                        time=dic['matchDate'] + dic['matchTime'], game_id=dic['matchId'])
            res.append(game)

    return res

def get_results(matchId: int):
    # 发送请求获取网页内容
    url = 'https://webapi.sporttery.cn/gateway/jc/football/getFixedBonusV1.qry?clientCode=3001&matchId=' + str(matchId)
    response = requests.get(url)
    html = response.content

    # 解析返回内容，转换为字典格式
    dict_data = json.loads(html)

    # 判断是否为有效网址
    if not dict_data['value']['matchResultList']:
        return

    # 获取基本信息
    base_data = json.loads(requests.get('https://i.sporttery.cn/api/fb_match_info/get_match_info?mid=' + str(matchId)).content)
    game_time = datetime.strptime(base_data['result']['date_cn'] + ' ' + base_data['result']['time_cn'], '%Y-%m-%d %H:%M:%S')
    session = base_data['result']['date_cn'] + ' ' + base_data['result']['s_num'] + ' ' + base_data['result']['l_cn']

    # 主队
    host = dict_data['value']['oddsHistory']['homeTeamAllName']
    # 客队
    guest = dict_data['value']['oddsHistory']['homeTeamAllName']
    # 单关
    dan = False
    for item in dict_data['value']['oddsHistory']['singleList']:
        if item['poolCode'] == 'HAD':
            dan = False if item['single'] == 0 else True

    # 获取队伍id
    host_team = Team.query.filter_by(name=host).all()
    guest_team = Team.query.filter_by(name=guest).all()
    # 需考虑队伍没有入库的情况
    if len(host_team) == 0:
        # 1.创建ORM对象
        team = Team(name=host)
        # 2.将ORM对象添加到db.session中
        db.session.add(team)
        # 3.将db.session中的改变同步到数据库中
        db.session.commit()
        # 4.获取id
        host_id = Team.query.filter_by(name=host).all()[0].id
    else:
        host_id = Team.query.filter_by(name=host).all()[0].id
    if len(guest_team) == 0:
        # 1.创建ORM对象
        team = Team(name=guest)
        # 2.将ORM对象添加到db.session中
        db.session.add(team)
        # 3.将db.session中的改变同步到数据库中
        db.session.commit()
        # 4.获取id
        guest_id = Team.query.filter_by(name=guest).all()[0].id
    else:
        guest_id = Team.query.filter_by(name=guest).all()[0].id

    # 比赛结果
    simple = ''
    rang = ''
    score = ''
    goals = 0
    half = ''

    for dic in dict_data['value']['matchResultList']:
        if dic['code'] == 'HHAD':
            rang = dic['combinationDesc']
        elif dic['code'] == 'HAFU':
            half = dic['combinationDesc']
        elif dic['code'] == 'HAD':
            simple = dic['combinationDesc']
        elif dic['code'] == 'CRS':
            score = dic['combinationDesc']
        elif dic['code'] == 'TTG':
            goals = int(dic['combinationDesc']) if dic['combinationDesc'] != '7+' else 7

    if simple == '':
        simple = '--'

    # 创建ORM对象，url有bug
    game = Game(dan=dan, host_id=host_id, guest_id=guest_id, game_time=game_time, session=session, simple=simple, rang=rang, score=score, goals=goals, half=half, url='https://www.lottery.gov.cn/jc/zqgdjj/?m=' + str(matchId))
    # 将ORM对象添加到db.session中
    db.session.add(game)
    # 将db.session中的改变同步到数据库中
    db.session.commit()

    # 返回比赛id
    game_id = Game.query.filter_by(session=session).all()[0].id

# -----------------------------返回历史奖金信息------------------------------------
    # 胜平负奖金
    if simple != '--':
        for i, dic in enumerate(dict_data['value']['oddsHistory']['hadList']):
            if i == 0:
                win_price = float(dic['h'])
                draw_price = float(dic['d'])
                lose_price = float(dic['a'])

                # 1.创建ORM对象
                simple_first = Simple_first(game_id=game_id, win_price=win_price, draw_price=draw_price,
                                            lose_price=lose_price)
                # 2.将ORM对象添加到db.session中
                db.session.add(simple_first)
                # 3.将db.session中的改变同步到数据库中
                db.session.commit()

            if i == len(dict_data['value']['oddsHistory']['hadList']) - 1:
                win_price = float(dic['h'])
                draw_price = float(dic['d'])
                lose_price = float(dic['a'])

                # 1.创建ORM对象
                simple_final = Simple_final(game_id=game_id, win_price=win_price, draw_price=draw_price,
                                            lose_price=lose_price)
                # 2.将ORM对象添加到db.session中
                db.session.add(simple_final)
                # 3.将db.session中的改变同步到数据库中
                db.session.commit()

            date_time = datetime.strptime(dic['updateDate'] + ' ' + dic['updateTime'], '%Y-%m-%d %H:%M:%S')
            win_price = float(dic['h'])
            draw_price = float(dic['d'])
            lose_price = float(dic['a'])

            # 1.创建ORM对象
            simple = Simple(game_id=game_id, date_time=date_time, win_price=win_price, draw_price=draw_price,
                            lose_price=lose_price)
            # 2.将ORM对象添加到db.session中
            db.session.add(simple)
            # 3.将db.session中的改变同步到数据库中
            db.session.commit()

    # 让球胜平负奖金
    for i, dic in enumerate(dict_data['value']['oddsHistory']['hhadList']):
        if i == 0:
            rang_win_price = float(dic['h'])
            rang_draw_price = float(dic['d'])
            rang_lose_price = float(dic['a'])

            # 1.创建ORM对象
            rang_first = Rang_first(game_id=game_id, rang_win_price=rang_win_price,
                        rang_draw_price=rang_draw_price, rang_lose_price=rang_lose_price)
            # 2.将ORM对象添加到db.session中
            db.session.add(rang_first)
            # 3.将db.session中的改变同步到数据库中
            db.session.commit()

        if i == len(dict_data['value']['oddsHistory']['hhadList']) - 1:
            rangfou = dic['goalLine']
            rang_win_price = float(dic['h'])
            rang_draw_price = float(dic['d'])
            rang_lose_price = float(dic['a'])

            # 1.创建ORM对象
            rang_final = Rang_final(rangfou=rangfou, game_id=game_id, rang_win_price=rang_win_price,
                        rang_draw_price=rang_draw_price, rang_lose_price=rang_lose_price)
            # 2.将ORM对象添加到db.session中
            db.session.add(rang_final)
            # 3.将db.session中的改变同步到数据库中
            db.session.commit()

        date_time = datetime.strptime(dic['updateDate'] + ' ' + dic['updateTime'], '%Y-%m-%d %H:%M:%S')
        rangfou = dic['goalLine']
        rang_win_price = float(dic['h'])
        rang_draw_price = float(dic['d'])
        rang_lose_price = float(dic['a'])

        # 1.创建ORM对象
        rang = Rang(rangfou=rangfou, game_id=game_id, date_time=date_time, rang_win_price=rang_win_price,
                    rang_draw_price=rang_draw_price, rang_lose_price=rang_lose_price)
        # 2.将ORM对象添加到db.session中
        db.session.add(rang)
        # 3.将db.session中的改变同步到数据库中
        db.session.commit()

    # 半全场奖金，使用enumerate()函数是预防后期可能会有处理半全场数据变化的需求
    for i, dic in enumerate(dict_data['value']['oddsHistory']['hafuList']):
        date_time = datetime.strptime(dic['updateDate'] + ' ' + dic['updateTime'], '%Y-%m-%d %H:%M:%S')
        win_win = float(dic['hh'])
        draw_win = float(dic['hd'])
        lose_win = float(dic['ha'])
        win_draw = float(dic['dh'])
        draw_draw = float(dic['dd'])
        lose_draw = float(dic['da'])
        win_lose = float(dic['ah'])
        draw_lose = float(dic['ad'])
        lose_lose = float(dic['aa'])

        # 1.创建ORM对象
        half = Half(game_id=game_id, date_time=date_time, win_win=win_win, draw_win=draw_win, lose_win=lose_win,
                    win_draw=win_draw, draw_draw=draw_draw, lose_draw=lose_draw, win_lose=win_lose,
                    draw_lose=draw_lose, lose_lose=lose_lose)
        # 2.将ORM对象添加到db.session中
        db.session.add(half)
        # 3.将db.session中的改变同步到数据库中
        db.session.commit()

    # 进球数奖金，使用enumerate()函数是预防后期可能会有处理进球数数据变化的需求
    for i, dic in enumerate(dict_data['value']['oddsHistory']['ttgList']):
        date_time = datetime.strptime(dic['updateDate'] + ' ' + dic['updateTime'], '%Y-%m-%d %H:%M:%S')
        zero_price = float(dic['s0'])
        one_price = float(dic['s1'])
        two_price = float(dic['s2'])
        there_price = float(dic['s3'])
        four_price = float(dic['s4'])
        five_price = float(dic['s5'])
        six_price = float(dic['s6'])
        seven_price = float(dic['s7'])

        # 1.创建ORM对象
        goals = Goals(game_id=game_id, date_time=date_time, zero_price=zero_price, one_price=one_price,
                      two_price=two_price, there_price=there_price, four_price=four_price, five_price=five_price,
                      six_price=six_price, seven_price=seven_price)
        # 2.将ORM对象添加到db.session中
        db.session.add(goals)
        # 3.将db.session中的改变同步到数据库中
        db.session.commit()

# -----------------------------返回历史奖金信息------------------------------------End

# 处理胜平负奖金以及让球胜平负奖金的变化数据
def data_change():
    # 胜平负奖金
    # 获取所有的记录
    simple_first_entries = Simple_first.query.all()
    simple_final_entries = Simple_final.query.all()

    # 将Simple_final的数据以字典形式存储，以便后续匹配
    simple_final_data = {entry.game_id: entry for entry in simple_final_entries}

    i = 1

    for entry1 in simple_first_entries:
        game_id = entry1.game_id
        if game_id in simple_final_data:
            entry2 = simple_final_data[game_id]

            result_field1 = entry2.win_price - entry1.win_price
            result_field2 = entry2.draw_price - entry1.draw_price
            result_field3 = entry2.lose_price - entry1.lose_price

            result_entry = Simple_change(
                game_id=game_id,
                win_price=result_field1,
                draw_price=result_field2,
                lose_price=result_field3
            )

            db.session.add(result_entry)
            db.session.commit()

        i += 1
        if i % 1000 == 0:
            print('胜平负奖金处理已完成', i)

    # 让球胜平负奖金
    # 获取所有的记录
    rang_first_entries = Rang_first.query.all()
    rang_final_entries = Rang_final.query.all()

    # 将Rang_final的数据以字典形式存储，以便后续匹配
    rang_first_data = {entry.game_id: entry for entry in rang_first_entries}

    i = 1

    for entry1 in rang_final_entries:
        game_id = entry1.game_id
        if game_id in rang_first_data:
            entry2 = rang_first_data[game_id]

            result_field1 = entry1.rang_win_price - entry2.rang_win_price
            result_field2 = entry1.rang_draw_price - entry2.rang_draw_price
            result_field3 = entry1.rang_lose_price - entry2.rang_lose_price

            result_entry = Rang_change(
                game_id=game_id,
                rang_win_price=result_field1,
                rang_draw_price=result_field2,
                rang_lose_price=result_field3
            )

            db.session.add(result_entry)
            db.session.commit()

        i += 1
        if i % 1000 == 0:
            print('已完成', i)

with app.app_context():
    # for matchId in range(1021405, 1021410):
    #     get_results(matchId)
    #     if matchId % 100 == 0:
    #         print(matchId, '已完成')
    data_change()
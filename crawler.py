import requests
import json
from models import *
from datetime import datetime
# from app import app

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
                        time=dic['matchDate'] + ' ' + dic['matchTime'], game_id=dic['matchId'])
            res.append(game)

    # 查询数据表的最后一条记录
    last_record = Game.query.order_by(Game.id.desc()).first().url[-7:]
    for matchId in range(int(last_record) + 1, res[0]['game_id']):
        get_results(matchId)
        print(matchId, "爬取成功")
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
    guest = dict_data['value']['oddsHistory']['awayTeamAllName']
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
                win_begin_price = float(dic['h'])
                draw_begin_price = float(dic['d'])
                lose_begin_price = float(dic['a'])

            if i == len(dict_data['value']['oddsHistory']['hadList']) - 1:
                win_end_price = float(dic['h'])
                draw_end_price = float(dic['d'])
                lose_end_price = float(dic['a'])

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

        if win_end_price - win_begin_price != 0 or draw_end_price - draw_begin_price != 0 or lose_end_price - lose_begin_price != 0:
            # 1.创建ORM对象
            simple_change = Simple_change(game_id=game_id, win_price=win_end_price - win_begin_price, draw_price=draw_end_price - draw_begin_price,
                                          lose_price=lose_end_price - lose_begin_price)
            # 2.将ORM对象添加到db.session中
            db.session.add(simple_change)
            # 3.将db.session中的改变同步到数据库中
            db.session.commit()

    # 让球胜平负奖金
    for i, dic in enumerate(dict_data['value']['oddsHistory']['hhadList']):
        if i == 0:
            rang_win_begin_price = float(dic['h'])
            rang_draw_begin_price = float(dic['d'])
            rang_lose_begin_price = float(dic['a'])

        if i == len(dict_data['value']['oddsHistory']['hhadList']) - 1:
            rang_win_end_price = float(dic['h'])
            rang_draw_end_price = float(dic['d'])
            rang_lose_end_price = float(dic['a'])

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
    if rang_win_end_price - rang_win_begin_price != 0 or rang_draw_end_price - rang_draw_begin_price != 0 or rang_lose_end_price - rang_lose_begin_price != 0:
        # 1.创建ORM对象
        rang_change = Rang_change(game_id=game_id, rang_win_price=rang_win_end_price - rang_win_begin_price,
                                      rang_draw_price=rang_draw_end_price - rang_draw_begin_price,
                                      rang_lose_price=rang_lose_end_price - rang_lose_begin_price)
        # 2.将ORM对象添加到db.session中
        db.session.add(rang_change)
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

# with app.app_context():
#     # for matchId in range(1000267, 1024576):
#     for matchId in range(1017317, 1024576):
#         get_results(matchId)
#         if matchId % 100 == 0:
#             print(matchId, '已完成', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # print(get_game_list())

# 删除错误比赛记录
# with app.app_context():
#     for i in range(36391, 50000):
#         record = db.session.query(Game).filter(Game.id == i)
#         if record is not None:
#             record.delete()
#             db.session.query(Goals).filter(Goals.game_id == i).delete()
#             db.session.query(Half).filter(Half.game_id == i).delete()
#             db.session.query(Rang).filter(Rang.game_id == i).delete()
#             db.session.query(Rang_change).filter(Rang_change.game_id == i).delete()
#             db.session.query(Rang_final).filter(Rang_final.game_id == i).delete()
#             db.session.query(Rang_first).filter(Rang_first.game_id == i).delete()
#             db.session.query(Simple).filter(Simple.game_id == i).delete()
#             db.session.query(Simple_change).filter(Simple_change.game_id == i).delete()
#             db.session.query(Simple_final).filter(Simple_final.game_id == i).delete()
#             db.session.query(Simple_first).filter(Simple_first.game_id == i).delete()
#             db.session.commit()
#         else:
#             break
# 测试获取数据变化列
# with app.app_context():
#     from sqlalchemy import func, desc
#     from sqlalchemy.orm import aliased
#
#     # 窗口函数，给每个分组的行编号
#     from sqlalchemy import over
#
#     row_number = func.row_number().over(partition_by=Simple.game_id, order_by=desc(Simple.date_time)).label('row_number')
#
#     # 子查询，包含窗口函数的编号
#     subquery = db.session.query(
#         Simple,
#         row_number
#     ).subquery()
#
#     # 创建一个别名以便于查询
#     alias_subquery = aliased(Simple, subquery)
#
#     # 主查询，过滤出编号为1的行
#     query = db.session.query(alias_subquery).filter(subquery.c.row_number == 1)
#
#     # 执行查询并获取结果
#     simple_finals = query.all()
#     simple_final_similar_games = []
#     for simple_final in simple_finals:
#         if (simple_final.win_price - 2.31) ** 2 + (simple_final.draw_price - 3.73) ** 2 + (simple_final.lose_price - 2.41) ** 2 < 0.0075:
#             simple_final_similar_games.append(simple_final.game_id)
#             print(simple_final.win_price, simple_final.draw_price, simple_final.lose_price)
#     # 根据索引在数据库中检索
#     games = Game.query.filter(Game.id.in_(simple_final_similar_games)).all()
#
#     # 得到比赛结果列表
#     simples = [game.simple for game in games]
#
#     # 计算三种结果比例
#     total_matches = len(simples)
#     win_count = simples.count('胜')
#     draw_count = simples.count('平')
#     loss_count = simples.count('负')
#
#     win_percentage = (win_count / total_matches) * 100
#     draw_percentage = (draw_count / total_matches) * 100
#     lose_percentage = (loss_count / total_matches) * 100
#
#     print(f'胜利比率为{win_percentage}, 平局比率为{draw_percentage}, 失败比率为{lose_percentage}')
#

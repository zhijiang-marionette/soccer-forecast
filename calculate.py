import numpy as np
from models import *
from sqlalchemy import func, desc
from sqlalchemy.orm import aliased

def probability_of_simple(win: float, draw: float, lose: float, first: bool):
    # 窗口函数，给每个分组的行编号
    if first == True:
        row_number = func.row_number().over(partition_by=Simple.game_id, order_by=desc(Simple.date_time)).label(
            'row_number')
    else:
        row_number = func.row_number().over(partition_by=Simple.game_id, order_by=Simple.date_time).label(
            'row_number')

    # 子查询，包含窗口函数的编号
    subquery = db.session.query(
        Simple,
        row_number
    ).subquery()

    # 创建一个别名以便于查询
    alias_subquery = aliased(Simple, subquery)

    # 主查询，过滤出编号为1的行
    query = db.session.query(alias_subquery).filter(subquery.c.row_number == 1)

    # 执行查询并获取结果
    simple_finals = query.all()
    simple_final_similar_games = []
    for simple_final in simple_finals:
        if (simple_final.win_price - win) ** 2 + (simple_final.draw_price - draw) ** 2 + (
                simple_final.lose_price - lose) ** 2 < 0.0075:
            simple_final_similar_games.append(simple_final.game_id)
    # 根据索引在数据库中检索
    games = Game.query.filter(Game.id.in_(simple_final_similar_games)).all()

    # 得到比赛结果列表
    simples = [game.simple for game in games]

    # 计算三种结果比例
    total_matches = len(simples) + 0.000001
    win_count = simples.count('胜')
    draw_count = simples.count('平')
    loss_count = simples.count('负')

    win_percentage = (win_count / total_matches) * 100
    draw_percentage = (draw_count / total_matches) * 100
    lose_percentage = (loss_count / total_matches) * 100

    return [['胜利', win_percentage],
            ['平局', draw_percentage],
            ['失败', lose_percentage]], games

def probability_of_rang(rang_win: float, rang_draw: float, rang_lose: float, first: bool, rangfou: int):
    # 窗口函数，给每个分组的行编号
    if first == True:
        row_number = func.row_number().over(partition_by=Rang.game_id, order_by=desc(Rang.date_time)).label(
            'row_number')
    else:
        row_number = func.row_number().over(partition_by=Rang.game_id, order_by=Rang.date_time).label(
            'row_number')

    # 子查询，包含窗口函数的编号
    subquery = db.session.query(
        Rang,
        row_number
    ).subquery()

    # 创建一个别名以便于查询
    alias_subquery = aliased(Rang, subquery)

    # 主查询，过滤出编号为1的行
    query = db.session.query(alias_subquery).filter(subquery.c.row_number == 1)

    # 执行查询并获取结果
    rang_finals = query.all()
    rang_final_similar_games = []
    for rang_final in rang_finals:
        if rangfou == rang_final.rangfou and (rang_final.rang_win_price - rang_win) ** 2 + (rang_final.rang_draw_price - rang_draw) ** 2 + (
                rang_final.rang_lose_price - rang_lose) ** 2 < 0.0075:
            rang_final_similar_games.append(rang_final.game_id)
    # 根据索引在数据库中检索
    games = Game.query.filter(Game.id.in_(rang_final_similar_games)).all()

    # 得到比赛结果列表
    rangs = [game.rang for game in games]

    # 存放结果
    result = []

    # 简单处理
    for i in range(len(rangs)):
        if rangs[i][-1] == '胜':
            result.append('让胜')
        elif rangs[i][-1] == '平':
            result.append('让平')
        else:
            result.append('让负')

    # 计算三种结果比例
    total_matches = len(result) + 0.000001
    rang_win_count = result.count('让胜')
    rang_draw_count = result.count('让平')
    rang_loss_count = result.count('让负')

    rang_win_percentage = (rang_win_count / total_matches) * 100
    rang_draw_percentage = (rang_draw_count / total_matches) * 100
    rang_lose_percentage = (rang_loss_count / total_matches) * 100

    return [['让胜', rang_win_percentage],
            ['让平', rang_draw_percentage],
            ['让负', rang_lose_percentage]], games

def probability_of_simpleChange(win: float, draw: float, lose: float):
    simple_changes = Simple_change.query.with_entities(Simple_change.win_price, Simple_change.draw_price,
                                                     Simple_change.lose_price).all()
    arr_nx3 = np.array(simple_changes)

    # 创建1x3和3x3的numpy数组
    array_1x3 = np.array([win, draw, lose])

    # 使用广播计算差值
    diff = arr_nx3 - array_1x3.reshape(1, -1)

    # 计算每个元素的平方
    squared_diff = diff ** 2

    # 沿着第一个轴（axis=1）求和
    sum_squared_diff = np.sum(squared_diff, axis=1)

    # 对结果开根号，得到欧几里得距离
    euclidean_distance = np.sqrt(sum_squared_diff)

    # 找到这些元素的索引, 取得是每一个奖金差距在0.04以内
    indices_below_threshold = np.where(euclidean_distance < 0.0692)[0] + 1

    # 根据索引在数据库中检索
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
    lose_percentage = (loss_count / total_matches) * 100

    return [['胜利', win_percentage],
            ['平局', draw_percentage],
            ['失败', lose_percentage]], games

def probability_of_rangChange(rang_win: float, rang_draw: float, rang_lose: float):
    # 导出数据库中所有截止时间的赔率
    rang_finals = Rang_change.query.with_entities(Rang_change.rang_win_price, Rang_change.rang_draw_price,
                                                     Rang_change.rang_lose_price).all()
    arr_nx3 = np.array(rang_finals)

    # 创建1x3和3x3的numpy数组
    array_1x3 = np.array([rang_win, rang_draw, rang_lose])

    # rangs = ['(' + rang + ')' + ' ' + '胜', '(' + rang + ')' + ' ' + '平', '(' + rang + ')' + ' ' + '负']
    # 使用广播计算差值
    diff = arr_nx3 - array_1x3.reshape(1, -1)

    # 计算每个元素的平方
    squared_diff = diff ** 2

    # 沿着第一个轴（axis=1）求和
    sum_squared_diff = np.sum(squared_diff, axis=1)

    # 对结果开根号，得到欧几里得距离
    euclidean_distance = np.sqrt(sum_squared_diff)

    # 找到这些元素的索引, 取得是每一个奖金差距在0.04以内
    indices_below_threshold = np.where(euclidean_distance < 0.0692)[0] + 1

    # 根据索引在数据库中检索
    games = Game.query.filter(Game.id.in_(indices_below_threshold)).all()

    # 得到比赛结果列表
    rangs = [game.rang for game in games]

    # 存放结果
    result = []

    # 简单处理
    for i in range(len(rangs)):
        if rangs[i][-1] == '胜':
            result.append('让胜')
        elif rangs[i][-1] == '平':
            result.append('让平')
        else:
            result.append('让负')

    # 计算三种结果比例
    total_matches = len(result)
    rang_win_count = result.count('让胜')
    rang_draw_count = result.count('让平')
    rang_loss_count = result.count('让负')

    rang_win_percentage = (rang_win_count / total_matches) * 100
    rang_draw_percentage = (rang_draw_count / total_matches) * 100
    rang_lose_percentage = (rang_loss_count / total_matches) * 100

    return [['让胜', rang_win_percentage],
            ['让平', rang_draw_percentage],
            ['让负', rang_lose_percentage]], games
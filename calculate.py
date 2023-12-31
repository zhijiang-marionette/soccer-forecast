import numpy as np
from models import *

def probability_of_simple(win: float, draw: float, lose: float):
    simple_finals = Simple_final.query.with_entities(Simple_final.win_price, Simple_final.draw_price,
                                                     Simple_final.lose_price).all()
    arr_nx3 = np.array(simple_finals)

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

def probability_of_rang(rang_win: float, rang_draw: float, rang_lose: float):
    # 导出数据库中所有截止时间的赔率
    rang_finals = Rang_final.query.with_entities(Rang_final.rang_win_price, Rang_final.rang_draw_price,
                                                     Rang_final.rang_lose_price).all()
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
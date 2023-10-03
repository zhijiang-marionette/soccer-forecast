from flask import Blueprint
from exts import db
from models import *
import numpy as np

# 创建蓝图模版
forecast_blue = Blueprint('name', __name__)

# 定义视图函数，配置蓝图路由
@forecast_blue.route('/')
def home():
    return 1

# 根据欧几里得距离计算，计算出截止时间的赔率相似比赛，得出三种结果可能性
@forecast_blue.route('/simple-final', methods=['POST'])
def simple_final():
    # 导出数据库中所有截止时间的赔率
    simple_finals = Simple_final.query.with_entities(Simple_final.win_price, Simple_final.draw_price,
                                                     Simple_final.lose_price).all()
    arr_nx3 = np.array(simple_finals)

    # 创建1x3和3x3的numpy数组
    array_1x3 = np.array([1.96, 3.42, 2.97])

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
    loss_percentage = (loss_count / total_matches) * 100

    print(f'胜利比例：{win_percentage:.2f}%')
    print(f'平局比例：{draw_percentage:.2f}%')
    print(f'失败比例：{loss_percentage:.2f}%')

# 根据欧几里得距离计算，计算出截止时间的赔率相似比赛，得出三种结果可能性（让球）
@forecast_blue.route('/rang-final', methods=['POST'])
def rang_final():
    # 导出数据库中所有截止时间的赔率
    rang_finals = Rang_final.query.with_entities(Rang_final.rang_win_price, Rang_final.rang_draw_price,
                                                     Rang_final.rang_lose_price).all()
    arr_nx3 = np.array(rang_finals)

    # 创建1x3和3x3的numpy数组
    array_1x3 = np.array([1.96, 3.42, 2.97])

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

    # 简单处理
    for i in range(len(rangs)):
        if rangs[i][-1] == '胜':
            rangs[i][-1] = '让胜'
        elif rangs[i][-1] == '平':
            rangs[i][-1] = '让平'
        else:
            rangs[i][-1] = '让负'

    # 计算三种结果比例
    total_matches = len(rangs)
    rang_win_count = rangs.count('让胜')
    rang_draw_count = rangs.count('让平')
    rang_loss_count = rangs.count('让负')

    rang_win_percentage = (rang_win_count / total_matches) * 100
    rang_draw_percentage = (rang_draw_count / total_matches) * 100
    rang_loss_percentage = (rang_loss_count / total_matches) * 100

    print(f'让胜比例：{rang_win_percentage:.2f}%')
    print(f'让平比例：{rang_draw_percentage:.2f}%')
    print(f'让负比例：{rang_loss_percentage:.2f}%')
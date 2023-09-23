from flask import Blueprint
from exts import db
from models import *

# 创建蓝图模版
forecast_blue = Blueprint('name', __name__)

# 定义视图函数，配置蓝图路由
@forecast_blue.route('/')
def home():
    return 1

# 根据最基础的距离计算，计算出截止时间的赔率相似比赛，得出三种结果可能性
@forecast_blue.route('/simple')
def simple():
    simples = Simple.query.filter_by(game_id=1).all()
    print(simples)
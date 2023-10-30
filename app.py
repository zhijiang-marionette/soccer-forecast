from flask import Flask, render_template
from models import *
# from blueprints.decision_manage import bp as dm_bp
import config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from blueprints.forecast_blue import forecast_blue
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie
from random import randrange
from calculate import probability_of_simple
from crawler import get_game_list
import json

app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)

# 注册蓝图
app.register_blueprint(forecast_blue)

# 先创建后绑定
db.init_app(app)

# app.register_blueprint(dm_bp)

migrate = Migrate(app, db)

# 第一次创建表
# with app.app_context():
#     db.create_all()

def bar_base() -> Bar:
    c = (
        Bar()
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [randrange(0, 100) for _ in range(6)])
        .add_yaxis("商家B", [randrange(0, 100) for _ in range(6)])
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    return c

def pie_base(data: list) -> Pie:
    p = (
        Pie()
        .add('', data,
             )
        .set_global_opts(title_opts=opts.TitleOpts(title="胜平负比例图"))
        .set_global_opts(legend_opts=opts.LegendOpts(is_show=False))  # 不显示图示
    )

    return p

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route("/barChart")
def get_bar_chart():
    c = bar_base()
    return c.dump_options_with_quotes()

@app.route("/pieChart")
def get_pie_chart():
    data = probability_of_simple(1.25, 4.50, 8.50)

    p = pie_base(data)
    return p.dump_options_with_quotes()

@app.route('/get-game-list')
def game_list():
    return json.dumps(get_game_list())

if __name__ == '__main__':
    app.run(debug=True)
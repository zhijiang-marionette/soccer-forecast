from flask import Flask, render_template
from models import *
# from blueprints.decision_manage import bp as dm_bp
import config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from blueprints.forecast_blue import forecast_blue
from pyecharts import options as opts
from pyecharts.charts import Bar
from random import randrange

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

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route("/barChart")
def get_bar_chart():
    c = bar_base()
    return c.dump_options_with_quotes()

@app.route('/add')
def add():
    # 1.创建ORM对象
    team = Team(name='曼城')
    # 2.将ORM对象添加到db.session中
    db.session.add(team)
    # 3.将db.session中的改变同步到数据库中
    db.session.commit()

    return "对象添加成功"

if __name__ == '__main__':
    app.run(debug=True)
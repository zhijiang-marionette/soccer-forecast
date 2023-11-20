from flask import Flask, render_template
from models import *
# from blueprints.decision_manage import bp as dm_bp
import config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from blueprints.forecast_blue import forecast_blue
from crawler import get_game_list
import json

app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)

# 注册蓝图
app.register_blueprint(forecast_blue, url_prefix='/forecast')

# 先创建后绑定
db.init_app(app)

# app.register_blueprint(dm_bp)

migrate = Migrate(app, db)

# 第一次创建表
# with app.app_context():
#     db.create_all()

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/get-game-list')
def game_list():
    return json.dumps(get_game_list())

if __name__ == '__main__':
    app.run(debug=True)
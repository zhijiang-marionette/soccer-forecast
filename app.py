from flask import Flask
from models import *
# from blueprints.decision_manage import bp as dm_bp
import config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)

# 先创建后绑定
db.init_app(app)

# app.register_blueprint(dm_bp)

migrate = Migrate(app, db)

# 第一次创建表
# with app.app_context():
#     db.create_all()

@app.route('/')
def hello_world():
    return 'Hello 中国!'

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
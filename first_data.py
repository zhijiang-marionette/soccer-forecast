import time

from models import *
from app import app

with app.app_context():
    # 取出id和胜平负结果
    data = Game.query.with_entities(Game.id, Game.simple, Game.url).all()
    for i in range(len(data)):
        # 根据比赛id找到让球初始奖金数据
        rang_first = Rang.query.filter_by(game_id=data[i][0]).all()[0]

        # 存储初始奖金数据
        # 1.创建ORM对象，将ORM对象添加到db.session中
        db.session.add(
            Rang_first(game_id=data[i][0], rang_win_price=rang_first.rang_win_price, rang_draw_price=rang_first.rang_draw_price,
                         rang_lose_price=rang_first.rang_lose_price))
        # 2.将db.session中的改变同步到数据库中
        db.session.commit()

        if data[i][1] == '--':
            continue
        # 根据比赛id找到胜平负初始奖金数据
        simple_first = Simple.query.filter_by(game_id=data[i][0]).all()[0]

        # 存储初始奖金数据
        # 1.创建ORM对象，将ORM对象添加到db.session中
        db.session.add(Simple_first(game_id=data[i][0], win_price=simple_first.win_price, draw_price=simple_first.draw_price,
                                    lose_price=simple_first.lose_price))
        # 2.将db.session中的改变同步到数据库中
        db.session.commit()

        if i % 1000 == 0:
            print('已完成', i)
from exts import db

# 队伍信息
class Team(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, index=True) # 队伍名称

# 比赛基本信息
class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dan = db.Column(db.Boolean, default=False) # 是否为单关
    host_id = db.Column(db.Integer, nullable=False) # 主队编号
    guest_id = db.Column(db.Integer, nullable=False) # 客队编号
    game_time = db.Column(db.DateTime, nullable=False) # 比赛时间
    session = db.Column(db.String(255), nullable=False) # 比赛场次

    # 结果
    simple = db.Column(db.String(255), nullable=False)
    rang = db.Column(db.String(255), nullable=False)
    score = db.Column(db.String(255), nullable=False)
    goals = db.Column(db.Integer, nullable=False)
    half = db.Column(db.String(255), nullable=False)

    # 链接
    url = db.Column(db.String(255), nullable=False)

# 胜平负奖金信息
class Simple(db.Model):
    __tablename__ = 'simple'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_id = db.Column(db.Integer, nullable=False)  # 关联比赛id
    date_time = db.Column(db.DateTime, nullable=False)  # 发布时间
    win_price = db.Column(db.Integer, nullable=False)
    draw_price = db.Column(db.Integer, nullable=False)
    lose_price = db.Column(db.Integer, nullable=False)

# 让球胜平负信息
class Rang(db.Model):
    __tablename__ = 'rang'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rangfou = db.Column(db.Integer, nullable=False) # 让球还是受让
    game_id = db.Column(db.Integer, nullable=False)  # 关联比赛id
    date_time = db.Column(db.DateTime, nullable=False)  # 发布时间
    rang_win_price = db.Column(db.Integer, nullable=False)
    rang_draw_price = db.Column(db.Integer, nullable=False)
    rang_lose_price = db.Column(db.Integer, nullable=False)

# 进球数奖金信息
class Goals(db.Model):
    __tablename__ = 'goals'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_id = db.Column(db.Integer, nullable=False)  # 关联比赛id
    date_time = db.Column(db.DateTime, nullable=False)  # 发布时间
    zero_price = db.Column(db.Integer, nullable=False)
    one_price = db.Column(db.Integer, nullable=False)
    two_price = db.Column(db.Integer, nullable=False)
    there_price = db.Column(db.Integer, nullable=False)
    four_price = db.Column(db.Integer, nullable=False)
    five_price = db.Column(db.Integer, nullable=False)
    six_price = db.Column(db.Integer, nullable=False)
    seven_price = db.Column(db.Integer, nullable=False)

# 半全场奖金信息
class Half(db.Model):
    __tablename__ = 'half'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_id = db.Column(db.Integer, nullable=False)  # 关联比赛id
    date_time = db.Column(db.DateTime, nullable=False)  # 发布时间
    win_win = db.Column(db.Integer, nullable=False)
    draw_win = db.Column(db.Integer, nullable=False)
    lose_win = db.Column(db.Integer, nullable=False)
    win_draw = db.Column(db.Integer, nullable=False)
    draw_draw = db.Column(db.Integer, nullable=False)
    lose_draw = db.Column(db.Integer, nullable=False)
    win_lose = db.Column(db.Integer, nullable=False)
    draw_lose = db.Column(db.Integer, nullable=False)
    lose_lose = db.Column(db.Integer, nullable=False)
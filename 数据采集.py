from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from exts import db
from models import *

# 根据XPATH定位元素
def find(path):
    global driver
    return driver.find_element(by=By.XPATH, value=path).text

# 获取比赛信息
def find_game():
    global game_id
    # 比赛场次
    session = find('/html/body/div[3]/div[6]/div[1]/div/div[3]/div[1]')
    # 比赛时间
    game_time = find('/html/body/div[3]/div[6]/div[1]/div/div[3]/div[3]/span[2]') + ' ' + find(
        '/html/body/div[3]/div[6]/div[1]/div/div[3]/div[3]/span[3]')
    # 主队
    host = find('/html/body/div[3]/div[6]/div[1]/div/div[3]/div[2]/div[2]').split(' ')[0]
    # 客队
    guest = find('/html/body/div[3]/div[6]/div[1]/div/div[3]/div[2]/div[2]').split(' ')[2]

    # 比赛结果
    simple = find('/html/body/div[3]/div[6]/div[2]/table[1]/tbody/tr[1]/td[1]/strong')
    rang = find('/html/body/div[3]/div[6]/div[2]/table[1]/tbody/tr[2]/td[1]/strong')
    score = find('/html/body/div[3]/div[6]/div[2]/table[1]/tbody/tr[3]/td[1]/strong')
    goals = int(find('/html/body/div[3]/div[6]/div[2]/table[1]/tbody/tr[4]/td[1]/strong'))
    half = find('/html/body/div[3]/div[6]/div[2]/table[1]/tbody/tr[5]/td[1]/strong')

    # 存储结果
    # 获取队伍id
    host_id = Team.query.filter_by(name=host)
    guest_id = Team.query.filter_by(name=guest)
    # 需考虑队伍没有入库的情况
    if len(host_id) == 0:
        # 1.创建ORM对象
        team = Team(name=host)
        # 2.将ORM对象添加到db.session中
        db.session.add(team)
        # 3.将db.session中的改变同步到数据库中
        db.session.commit()
        # 4.获取id
        host_id = Team.query.filter_by(name=host)
    if len(guest_id) == 0:
        # 1.创建ORM对象
        team = Team(name=guest)
        # 2.将ORM对象添加到db.session中
        db.session.add(team)
        # 3.将db.session中的改变同步到数据库中
        db.session.commit()
        # 4.获取id
        guest_id = Team.query.filter_by(name=guest)

    # 创建ORM对象
    game = Game(dan=False, host_id=host_id, guest_id=guest_id, game_time=game_time, session=session, simple=simple, rang=rang, score=score, goals=goals, half=half)
    # 将ORM对象添加到db.session中
    db.session.add(game)
    # 将db.session中的改变同步到数据库中
    db.session.commit()

    # 返回比赛id
    game_id = Team.query.filter_by(session=session)

# 获取胜平负信息
def find_simple():
    date_time = find('//*[@id="had_tb"]/tr[1]/td[1]')
    win_price = find('//*[@id="had_tb"]/tr[2]/td[2]')
    draw_price = find('//*[@id="had_tb"]/tr[3]/td[3]')
    lose_price = find('//*[@id="had_tb"]/tr[4]/td[4]')

    # 1.创建ORM对象
    simple = Simple(game_id=game_id, date_time=date_time, win_price=win_price, draw_price=draw_price, lose_price=lose_price)
    # 2.将ORM对象添加到db.session中
    db.session.add(simple)
    # 3.将db.session中的改变同步到数据库中
    db.session.commit()

# 获取让球胜平负信息
def find_rang():
    date_time = find('//*[@id="hhad_tb"]/tr[1]/td[1]')
    rang_win_price = find('//*[@id="hhad_tb"]/tr[1]/td[2]')
    rang_draw_price = find('//*[@id="hhad_tb"]/tr[1]/td[3]')
    rang_lose_price = find('//*[@id="hhad_tb"]/tr[1]/td[4]')

    # 1.创建ORM对象
    rang = Simple(game_id=game_id, date_time=date_time, rang_win_price=rang_win_price, rang_draw_price=rang_draw_price, rang_lose_price=rang_lose_price)
    # 2.将ORM对象添加到db.session中
    db.session.add(rang)
    # 3.将db.session中的改变同步到数据库中
    db.session.commit()

# 获取总进球数信息
def find_goals():
    i = 1
    while find('//*[@id="ttg_tb"]/tr[' + str(i) + ']') != '':
        date_time = find('//*[@id="ttg_tb"]/tr[1]/td[1]')
        zero_price = find('//*[@id="ttg_tb"]/tr[1]/td[2]')
        one_price = find('//*[@id="ttg_tb"]/tr[1]/td[3]')
        two_price = find('//*[@id="ttg_tb"]/tr[1]/td[4]')
        there_price = find('//*[@id="ttg_tb"]/tr[1]/td[5]')
        four_price = find('//*[@id="ttg_tb"]/tr[1]/td[6]')
        five_price = find('//*[@id="ttg_tb"]/tr[1]/td[7]')
        six_price = find('//*[@id="ttg_tb"]/tr[1]/td[8]')
        seven_price = find('//*[@id="ttg_tb"]/tr[1]/td[9]')

        # 1.创建ORM对象
        goals = Goals(game_id=game_id, date_time=date_time, zero_price=zero_price, one_price=one_price,
                      two_pricee=two_price, there_price=there_price, four_price=four_price, five_price=five_price,
                      six_price=six_price, seven_price=seven_price)
        # 2.将ORM对象添加到db.session中
        db.session.add(goals)
        # 3.将db.session中的改变同步到数据库中
        db.session.commit()

        i += 1

# 构建驱动
driver = webdriver.Chrome()
# 前往网站
driver.get(
    'https://www.lottery.gov.cn/jc/zqgdjj/?m=100026')
# 最大化窗口
driver.maximize_window()
# 等待页面渲染
sleep(5)

game_id = 0

# 退出驱动
driver.quit()
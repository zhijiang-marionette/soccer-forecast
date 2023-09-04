from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from exts import db
from models import *
from datetime import datetime
from app import app

# 根据XPATH定位元素
def find(path):
    global driver
    return driver.find_element(by=By.XPATH, value=path).text

# 获取比赛信息
def find_game():
    global game_id
    # 判断是否为单关
    try:
        driver.find_element(by=By.XPATH, value='//*[@id="had_title"]/em')
        dan = True
    except:
        dan = False
    # 比赛场次
    session = find('/html/body/div[3]/div[6]/div[1]/div/div[3]/div[1]')
    # 比赛时间
    game_time = datetime.strptime(find('/html/body/div[3]/div[6]/div[1]/div/div[3]/div[3]/span[2]') + ' ' + find(
        '/html/body/div[3]/div[6]/div[1]/div/div[3]/div[3]/span[3]'), '%Y-%m-%d %H:%M:%S')
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
    host_team = Team.query.filter_by(name=host).all()
    guest_team = Team.query.filter_by(name=guest).all()
    # 需考虑队伍没有入库的情况
    if len(host_team) == 0:
        # 1.创建ORM对象
        team = Team(name=host)
        # 2.将ORM对象添加到db.session中
        db.session.add(team)
        # 3.将db.session中的改变同步到数据库中
        db.session.commit()
        # 4.获取id
        host_id = Team.query.filter_by(name=host).all()[0].id
    else:
        host_id = Team.query.filter_by(name=host).all()[0].id
    if len(guest_team) == 0:
        # 1.创建ORM对象
        team = Team(name=guest)
        # 2.将ORM对象添加到db.session中
        db.session.add(team)
        # 3.将db.session中的改变同步到数据库中
        db.session.commit()
        # 4.获取id
        guest_id = Team.query.filter_by(name=guest).all()[0].id
    else:
        guest_id = Team.query.filter_by(name=guest).all()[0].id

    # 创建ORM对象
    game = Game(dan=dan, host_id=host_id, guest_id=guest_id, game_time=game_time, session=session, simple=simple, rang=rang, score=score, goals=goals, half=half, url=url)
    # 将ORM对象添加到db.session中
    db.session.add(game)
    # 将db.session中的改变同步到数据库中
    db.session.commit()

    # 返回比赛id
    game_id = Game.query.filter_by(session=session).all()[0].id

# 获取胜平负信息
def find_simple():
    i = 1
    while find('//*[@id="had_tb"]/tr[' + str(i) + ']') != '':
        arr = find('//*[@id="had_tb"]/tr[' + str(i) + ']').split(' ')
        date_time = datetime.strptime(arr[0] + ' ' + arr[1], '%Y-%m-%d %H:%M:%S')
        win_price = float(arr[2])
        draw_price = float(arr[3])
        lose_price = float(arr[4])

        # 1.创建ORM对象
        simple = Simple(game_id=game_id, date_time=date_time, win_price=win_price, draw_price=draw_price,
                        lose_price=lose_price)
        # 2.将ORM对象添加到db.session中
        db.session.add(simple)
        # 3.将db.session中的改变同步到数据库中
        db.session.commit()
        i += 1


# 获取让球胜平负信息
def find_rang():
    i = 1
    while find('//*[@id="hhad_tb"]/tr[' + str(i) + ']') != '':
        arr = find('//*[@id="hhad_tb"]/tr[' + str(i) + ']').split(' ')
        date_time = datetime.strptime(arr[0] + ' ' + arr[1], '%Y-%m-%d %H:%M:%S')
        rangfou = find('//*[@id="hhad_title"]/span')[1:3]
        rang_win_price = float(arr[2])
        rang_draw_price = float(arr[3])
        rang_lose_price = float(arr[4])

        # 1.创建ORM对象
        rang = Rang(rangfou=rangfou, game_id=game_id, date_time=date_time, rang_win_price=rang_win_price,
                      rang_draw_price=rang_draw_price, rang_lose_price=rang_lose_price)
        # 2.将ORM对象添加到db.session中
        db.session.add(rang)
        # 3.将db.session中的改变同步到数据库中
        db.session.commit()

        i += 1

# 获取总进球数信息
def find_goals():
    element_arr = driver.find_elements(by=By.XPATH, value='//*[@id="ttg_tb"]/tr')
    for j in range(len(element_arr)):
        arr = find('//*[@id="ttg_tb"]/tr[' + str(j + 1) + ']').split(' ')
        date_time = datetime.strptime(arr[0] + ' ' + arr[1], '%Y-%m-%d %H:%M:%S')
        zero_price = float(arr[2])
        one_price = float(arr[3])
        two_price = float(arr[4])
        there_price = float(arr[5])
        four_price = float(arr[6])
        five_price = float(arr[7])
        six_price = float(arr[8])
        seven_price = float(arr[9])

        # 1.创建ORM对象
        goals = Goals(game_id=game_id, date_time=date_time, zero_price=zero_price, one_price=one_price,
                      two_price=two_price, there_price=there_price, four_price=four_price, five_price=five_price,
                      six_price=six_price, seven_price=seven_price)
        # 2.将ORM对象添加到db.session中
        db.session.add(goals)
        # 3.将db.session中的改变同步到数据库中
        db.session.commit()


# 获取半全场信息
def find_half():
    element_arr = driver.find_elements(by=By.XPATH, value='//*[@id="hafu_tb"]/tr')
    for j in range(len(element_arr)):
        arr = find('//*[@id="hafu_tb"]/tr[' + str(j + 1) + ']').split(' ')
        date_time = datetime.strptime(arr[0] + ' ' + arr[1], '%Y-%m-%d %H:%M:%S')
        win_win = float(arr[2])
        draw_win = float(arr[3])
        lose_win = float(arr[4])
        win_draw = float(arr[5])
        draw_draw = float(arr[6])
        lose_draw = float(arr[7])
        win_lose = float(arr[8])
        draw_lose = float(arr[9])
        lose_lose = float(arr[10])

        # 1.创建ORM对象
        half = Half(game_id=game_id, date_time=date_time, win_win=win_win, draw_win=draw_win, lose_win=lose_win,
                      win_draw=win_draw, draw_draw=draw_draw, lose_draw=lose_draw, win_lose=win_lose,
                      draw_lose=draw_lose, lose_lose=lose_lose)
        # 2.将ORM对象添加到db.session中
        db.session.add(half)
        # 3.将db.session中的改变同步到数据库中
        db.session.commit()

url = 'https://www.lottery.gov.cn/jc/zqgdjj/?m=60000'
# 构建驱动
driver = webdriver.Chrome()
# 前往网站
driver.get(url)
# 最大化窗口
driver.maximize_window()
# 等待页面渲染
sleep(5)

game_id = 0

for j in range(60001, 70000):
    # 判断是否为无效网址
    if not find('//*[@id="leagueMatch"]'):
        continue

    # 爬取历史奖金信息
    with app.app_context():
        find_game()
        find_simple()
        find_rang()
        find_goals()
        find_half()

    print(url, '数据已爬取完毕')

    url = 'https://www.lottery.gov.cn/jc/zqgdjj/?m=' + str(0) + str(
        j) if j < 100000 else 'https://www.lottery.gov.cn/jc/zqgdjj/?m=' + str(j)

    # 新开窗口
    driver.execute_script("window.open('', '_blank');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(url)

    # 切换回初始窗口
    driver.switch_to.window(driver.window_handles[0])
    # 关闭原始窗口
    driver.close()
    sleep(5)
    # 重新定位窗口
    driver.switch_to.window(driver.window_handles[0])
    sleep(2)

# 退出驱动
driver.quit()
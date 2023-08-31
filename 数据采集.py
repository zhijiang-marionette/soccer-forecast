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
    i = 1
    while find('//*[@id="had_tb"]/tr[' + str(i) + ']') != '':
        arr = find('//*[@id="had_tb"]/tr[' + str(i) + ']').split(' ')
        date_time = arr[0] + '' + arr[1]
        win_price = int(arr[2])
        draw_price = int(arr[3])
        lose_price = int(arr[4])

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
        date_time = arr[0] + '' + arr[1]
        rang_win_price = int(arr[2])
        rang_draw_price = int(arr[3])
        rang_lose_price = int(arr[4])

        # 1.创建ORM对象
        rang = Simple(game_id=game_id, date_time=date_time, rang_win_price=rang_win_price,
                      rang_draw_price=rang_draw_price, rang_lose_price=rang_lose_price)
        # 2.将ORM对象添加到db.session中
        db.session.add(rang)
        # 3.将db.session中的改变同步到数据库中
        db.session.commit()

    i += 1

# 获取总进球数信息
def find_goals():
    i = 1
    while find('//*[@id="ttg_tb"]/tr[' + str(i) + ']') != '':
        arr = find('//*[@id="ttg_tb"]/tr[' + str(i) + ']').split(' ')
        date_time = arr[0] + '' + arr[1]
        zero_price = int(arr[3])
        one_price = int(arr[4])
        two_price = int(arr[5])
        there_price = int(arr[6])
        four_price = int(arr[7])
        five_price = int(arr[8])
        six_price = int(arr[9])
        seven_price = int(arr[10])

        # 1.创建ORM对象
        goals = Goals(game_id=game_id, date_time=date_time, zero_price=zero_price, one_price=one_price,
                      two_pricee=two_price, there_price=there_price, four_price=four_price, five_price=five_price,
                      six_price=six_price, seven_price=seven_price)
        # 2.将ORM对象添加到db.session中
        db.session.add(goals)
        # 3.将db.session中的改变同步到数据库中
        db.session.commit()

        i += 1

# 获取半全场信息
def find_half():
    i = 1
    while find('//*[@id="hafu_tb"]/tr[' + str(i) + ']') != '':
        arr = find('//*[@id="hafu_tb"]/tr[' + str(i) + ']').split(' ')
        date_time = arr[0] + '' + arr[1]
        win_win = int(arr[2])
        draw_win = int(arr[3])
        lose_win = int(arr[4])
        win_draw = int(arr[5])
        draw_draw = int(arr[6])
        lose_draw = int(arr[7])
        win_lose = int(arr[8])
        draw_lose = int(arr[9])
        lose_lose = int(arr[10])

        # 1.创建ORM对象
        half = Half(game_id=game_id, date_time=date_time, win_win=win_win, draw_win=draw_win, lose_win=lose_win,
                      win_draw=win_draw, draw_draw=draw_draw, lose_draw=lose_draw, win_lose=win_lose,
                      draw_lose=draw_lose, lose_lose=lose_lose)
        # 2.将ORM对象添加到db.session中
        db.session.add(half)
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


# 获取初始窗口句柄
initial_window = driver.current_window_handle

# 测试：新建窗口
driver.execute_script("window.open('', '_blank');")
driver.switch_to.window(driver.window_handles[1])
driver.get("https://www.baidu.com")
driver.find_element(By.ID, 'kw').send_keys('hello python')
sleep(5)
driver.close()


# 切换回初始窗口
driver.switch_to.window(initial_window)
sleep(2)
game_id = 0

# 退出驱动
driver.quit()

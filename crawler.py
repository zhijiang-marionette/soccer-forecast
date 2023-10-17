import requests
import json

# 爬取竞彩网开的赛事，并汇总成列表
def get_game_list() -> list:
    # 发送请求获取网页内容
    url = 'https://webapi.sporttery.cn/gateway/jc/football/getMatchListV1.qry?clientCode=3001'
    response = requests.get(url)
    html = response.content

    # 解析返回内容，转换为字典格式
    dict_data = json.loads(html)

    res = []

    for item in dict_data['value']['matchInfoList']:
        for dic in item['subMatchList']:
            game = dict(matchNum=dic['matchNum'], league=dic['leagueAllName'],
                        team=dic['homeTeamAllName'] + 'vs' + dic['awayTeamAllName'],
                        time=dic['matchDate'] + dic['matchTime'], game_id=dic['matchId'])
            res.append(game)

    return res

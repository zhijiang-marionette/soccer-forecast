# 项目配置信息
# 本地数据库配置信息
# HOSTNAME = '127.0.0.1'
# PORT = '3306'
# DATABASE = 'soccer'
# USERNAME = 'root'
# PASSWORD = 'ljm2000214'
# DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
# SQLALCHEMY_DATABASE_URI = DB_URI
from urllib import parse

# 服务器数据库配置信息
HOSTNAME = '47.98.238.87'
PORT = '3306'
DATABASE = 'game_data'
USERNAME = 'root'
PASSWORD = parse.quote_plus('LYHlyh20000329@')
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True

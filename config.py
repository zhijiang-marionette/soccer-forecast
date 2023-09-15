from urllib import parse
# 项目配置信息
# 本地数据库配置信息
# HOSTNAME = '127.0.0.1'
# PORT = '3306'
# DATABASE = 'soccer'
# USERNAME = 'root'
# PASSWORD = 'ljm2000214'
# DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
# SQLALCHEMY_DATABASE_URI = DB_URI

# 服务器数据库配置信息
HOSTNAME = '47.98.238.87'
PORT = '3306'
DATABASE = 'game_data'
USERNAME = 'root'
PASSWORD = parse.quote_plus('LYHlyh20000329@')
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True

# 邮箱相关配置
MAIL_SEVER = 'smtp.qq.com' # qq邮箱
MAIL_PORT = 465
MAIL_USERNAME = '962395743@qq.com'
MAIL_PASSWORD = 'pharcwzskfqubcjf'
MAIL_USE_TLS = False
MAIL_USE_SSL = True
# 项目配置信息
# 数据库配置信息
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'soccer'
USERNAME = 'root'
PASSWORD = 'ljm2000214'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
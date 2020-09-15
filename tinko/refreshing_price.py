import pymysql
from pymysql.cursors import DictCursor

connection = pymysql.connect(
    host='localhost',
    user='user',
    password='password',
    db='iata',
    charset='utf8mb4',
    cursorclass=DictCursor
)
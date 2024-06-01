# https://jongsky.tistory.com/17 참조

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from psycopg2

# 접속레이아웃 참조: https://lovelydiary.tistory.com/324
HOSTNAME ='105.53.140.229'
PORT = '5432'
USERNAME= 'oee_cb'
PASSWORD='amsdi$01'
DATABASE='oee_cb_db'
CHARSET1='utf8' 
CHARSET2='utf-8'

# https://parkjju.github.io/vue-TIL/python/2021-03-08-sqlAlchemy.html 참조
db_ip ='105.53.140.229'
db_port = '5432'
db_id = 'oee_cb'
db_passwd ='amsdi$01'
db_name='oee_cb_db'
encoding='utf-8'

def create_engine( self ):
        try:
            self.engine = create_engine(
                'postgresql+psycopg2://' + self.inv_user + ':' + self.inv_password + '@' + self.inv_host + ':5432/' + self.inv_database
            )
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgeSQL", error)

# con_str_fmt='mysql+mysqldb://{0}:{1}@{2}:{3}/{4}?charset={5}'
con_str_fmt='mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset={5}'
pg_con_str_fmt=f'postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}'
con_str=con_str_fmt.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE, CHARSET1)
DB_URL=pg_con_str_fmt

print("DB_URL---:" , DB_URL) 

class engineconn:
    def __init__(self):
        self.engine = create_engine( DB_URL  )
        self.engine.echo = True                                       

    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn


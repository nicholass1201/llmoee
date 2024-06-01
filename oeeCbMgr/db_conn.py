# https://jongsky.tistory.com/17 참조

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

 
# https://parkjju.github.io/vue-TIL/python/2021-03-08-sqlAlchemy.html 참조
db_ip ='210.114.91.91'
db_port = '26868'
db_id = 'wc'
db_passwd ='wc!#'
db_name='wc'
# CHARSET1='utf8' 
encoding='utf-8'


# con_str_fmt='mysql+mysqldb://{0}:{1}@{2}:{3}/{4}?charset={5}'
con_str_fmt='mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset={5}'
con_str=con_str_fmt.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE, CHARSET1)
DB_URL=con_str



print("DB_URL---:" , DB_URL)  # DB_URL---: mysql+pymysql://acdev:ac!@#@122.49.74.237:3306/ac?charset=utf8

# DB_URL = 'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'
# DB_URL = 'mysql+pymysql://cadev:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'

class engineconn:

    def __init__(self):
        # self.engine = create_engine(DB_URL, encoding='utf-8' )
        # self.engine = create_engine("mysql+mysqldb://" + db_id + ":" + db_passwd + "@"
        #                                + db_ip + ":" + db_port + "/" + db_name, encoding='utf-8')
        self.engine = create_engine("mysql+pymysql://" + db_id + ":" + db_passwd + "@"
                                       + db_ip + ":" + db_port + "/" + db_name  )
        self.engine.echo = True                                       


    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn
# https://jongsky.tistory.com/17 참조

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from decouple import config
import psycopg2

class EngineConn:
    def __init__(self):
        self.hostname = config('HOSTNAME')
        self.port = config('PORT')
        self.username = config('USERNAME')
        self.password = config('PASSWORD')
        self.database = config('DATABASE')
        self.charset1 = config('CHARSET1')
        self.charset2 = config('CHARSET2')
        
        self.engine = None
        self._create_engine()

    def _create_engine(self):
        pg_con_str_fmt=f'postgresql+psycopg2://{self.username}:{self.password}@{self.hostname}:{self.port}/{self.database}'
        print("DB connection string---:" , pg_con_str_fmt) 

        try:
            self.engine = create_engine( pg_con_str_fmt )
            self.engine.echo = True
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgeSQL", error)
        finally:
            print(self.engine)

    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn
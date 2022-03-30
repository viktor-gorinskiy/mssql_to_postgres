import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys

class PgSql():
    
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.cursor = None
        self.conn = None
        
    def connect(self):
        self.conn = psycopg2.connect(dbname=self.database, user=self.username, password=self.password, host=self.server)
        
        self.cursor = self.conn.cursor()
        
    def insert_many(self, table='table', schema='public', s_values='%s', list_records=[]):
        sql_insert = f'INSERT INTO {schema}.{table}  VALUES ({s_values});'
        try:
            self.cursor.executemany(sql_insert, list_records)
        except psycopg2.errors.UniqueViolation as error:
            print('\n\n\t########### - ERROR - ###########\n\n', error)
            msg = f'Таблица {schema}.{table} не пустая, рекомендую удалить её и повторить.\nВозможно стоит пересоздать всю базу.\n'
            print(msg)
            sys.exit(1)
        self.conn.commit()

    
    def create_table_manual(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
    
    def create_schema(self, schema):
        sql = f'CREATE SCHEMA IF NOT EXISTS {schema};'
        self.cursor.execute(sql)
        self.conn.commit()

    def drop_table(self, schema, table):
        sql = f'DROP TABLE IF EXISTS {schema}.{table};'
        self.cursor.execute(sql)
        self.conn.commit()
        
    def close(self):
        self.cur.close()
        self.conn.close()


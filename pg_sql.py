import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

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
        # s_values = self.gen_S(table)
        sql_insert = f'INSERT INTO {schema}.{table}  VALUES ({s_values});'
        self.cursor.executemany(sql_insert, list_records)
        self.conn.commit()
    
    def create_table(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
    
    def create_schema(self, schema):
        sql = f'CREATE SCHEMA IF NOT EXISTS {schema};'
        self.cursor.execute(sql)
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()


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
        
    def get_sql_create_table(self, table):
        sql = f"""CREATE TABLE "{table}"(\n"""
        c = 0
        sql_lenes = self.get_columns(table)
        for sql_lene in sql_lenes:
            c+=1
            sql += sql_lene
            if c < len(sql_lenes):
                sql += ',\n'
            
        pk_str = self.get_primaryKeys(table)
    
        if pk_str:
            sql += ',\n' + pk_str + '\n'
        sql += ');'
        return(sql)
    
    def get_sql(self, columns):    
        sql_lines = []
        for column in columns:
            type_d = self.return_type(column[5], column[6], column[8])
            is_null= self.return_null(column[17])
            sql_line = f""""{column[3]}" {type_d} {is_null}"""
            sql_lines.append(sql_line)
        return sql_lines
    
    def insert_many(self, table='table', s_values='%s', list_records=[]):
        # s_values = self.gen_S(table)
        sql_insert = f'INSERT INTO "{table}"  VALUES ({s_values});'
        self.cursor.executemany(sql_insert, list_records)
        self.conn.commit()
    
    def create_table(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()

# from ast import Break
import imp
import pyodbc
import config

import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import datetime
import sys


# ms_database = 'MegicBrainTicket'
ms_database = config.ms_database

# ps_database = config.ps_database
# ps_database = ms_database
ps_database = ms_database

conn_ms = pyodbc.connect('DRIVER={FreeTDS};' + f"SERVER={config.ms_server};DATABASE={ms_database};UID={config.ms_username};PWD={config.ms_password}")
cursor_ms = conn_ms.cursor()



def len_columns(table):
    columns = cursor_ms.columns(table=table)
    c = 0
    for row in columns:
        c+=1
    return c

def gen_S(table):
    count_columns = len_columns(table)
    s_values = (", ".join(['%s' for x in range(count_columns)]))
    return s_values
    
def len_records_in_table(table):
    sql_count = f"SELECT COUNT(*) FROM {ms_database}.dbo.{table};"
    return cursor_ms.execute(sql_count).fetchone()[0]

# Получаем список таблиц.
tables = []
for row in cursor_ms.tables():
    if row.table_schem == "dbo":
        if row[3] == 'TABLE' and row[2] != 'sysdiagrams':
            tables.append(row[2])



def insert(table, list_records):
    print('\ttable def ==>', table, 'len(list_records)==>', len(list_records))
    conn_ps = psycopg2.connect(dbname=ps_database, user=config.ps_username, password=config.ps_password, host=config.ps_server)
    cursor_ps = conn_ps.cursor()
    
    s_values = gen_S(table)
    sql_insert = f'INSERT INTO "{table}"  VALUES ({s_values});'
    # print('\t sql_insert def ==>', sql_insert)
    cursor_ps.executemany(sql_insert, list_records)
    
    # try:
    #     cursor_ps.executemany(sql_insert, list_records)
    # except Exception as error:
    #     print('\n\tERROR',error, table, '\n')
    #     for r in list_records:
    #         print('\t', r)
    #     print('\n')
    #     if not 'duplicate key value' in str(error) or not 'duplicate key value violates unique constraint' in str(error):
    #         sys.exit(1)
        
    conn_ps.commit()
    # cursor_ps.close()
    
    

for table in tables:
    s_values = gen_S(table)
    
    count_records_table = len_records_in_table(table)
    
    sql_select = f"SELECT * FROM [{table}]"
    all_records = cursor_ms.execute(sql_select)
    print('Table ==>',table, 'count_records_table ==>', count_records_table)
    
    sql_s = []
    cicle = 0
    pull = 10
    for row in all_records:
        cicle += 1
        sql_s.append(row)
        
        if not cicle%pull:                  # Если заполнился пул, то скидываем его на загрузку в посгрес
            insert(table, sql_s)
            print('\t1', 'cicle ==>', cicle,'<>', 'cicle%pull ==>', cicle%pull,  'count_records_table ==>', count_records_table, 'len sql_s ==>', len(sql_s))
            sql_s = []
        
        
        # if cicle == count_records_table:    # Если общее количество записей равно текущему состоянию счетчика, то скидываем его на загрузку в посгрес
    insert(table, sql_s)
    sql_s = []
    print()

    
    
    
    # s_values = gen_S(table)
    # sql = f'INSERT INTO "{table}"  VALUES ({s_values});'
    # print('start executemany')
    # cursor_ps.executemany(sql,sql_s)
    # conn_ps.commit()
    # print()
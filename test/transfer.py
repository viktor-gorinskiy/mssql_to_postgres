from ast import Break
import pyodbc
import config

import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import datetime



# ms_database = 'MegicBrainTicket'
ms_database = config.ms_database

# ps_database = config.ps_database
# ps_database = ms_database
ps_database = ms_database

conn_ms = pyodbc.connect('DRIVER={FreeTDS};' + f"SERVER={config.ms_server};DATABASE={ms_database};UID={config.ms_username};PWD={config.ms_password}")
cursor_ms = conn_ms.cursor()


conn_ps = psycopg2.connect(dbname=ps_database, user=config.ps_username, password=config.ps_password, host=config.ps_server)
cursor_ps = conn_ps.cursor()


def convert_type(date):
    # Будем вормировать из полученых данных стрку для передачи в посгрес
    strings=""
    c = 0
    # print('date ==>', date)
    for var in date:
        c += 1
        # print('var ==>',var, type(var))
        if var is None:         # Если тип не определен или пустое значение, то заменяем его на NULL
            strings += f'NULL'
        elif type(var) == str:  # Все стороки должны быть в кавычках
            strings += f"""'{var}'"""
        # Тут конвертим дату
        elif type(var) == datetime.datetime: strings += f"""'{var.isoformat(" ", "microseconds")}'"""
        elif type(var) == datetime.date: strings += f"""'{var.isoformat()}'"""
        # Тут меняем будевые значения с 0,1 на True, False
        elif type(var) == bool:
            if var: strings += f'True'
            else: strings += f'False'
        # Все остальные типы данных оставляем как есть
        else:
            strings += f'{var}'
        # Добавляем запятую после каждого значения, кроме последнего
        if c < len(date):
            strings += ', '
    return strings   

    
def truncate_table(TABLE_NAME):
    cursor_ps.execute("TRUNCATE TABLE {table} RESTART IDENTITY".format(table=TABLE_NAME))
    conn_ps.commit()
    
# Получаем список таблиц.
tables = []
for row in cursor_ms.tables():
    if row.table_schem == "dbo":
        if row[3] == 'TABLE' and row[2] != 'sysdiagrams':
            tables.append(row[2])


for table in tables:
    print('Table ==>',table)
    # truncate_table(table)
    
    sql_count = f"SELECT COUNT(*) FROM {ms_database}.dbo.{table};"
    all_rows = cursor_ms.execute(sql_count).fetchone()[0]

    step = int(round(all_rows*0.00001, 1)*1000)
    if step < 1: step = 1

    print('Step', all_rows, '|', step)
    
    sql_select = f"SELECT * FROM [{table}]"
 
    c = 0
    for row in cursor_ms.execute(sql_select):
        if c%step == 0:
            print(c, '<==>', all_rows)
        c += 1
        sql_data = convert_type(row)
        query =  f"""INSERT INTO "{table}" VALUES({sql_data});"""
        try:
            cursor_ps.execute(query);
        except Exception as error:
            print('ERROR ==>', error)
            print('row ==>',row)
            print('sql_data ==>', sql_data)
            print('query ==>', query)
            break
    conn_ps.commit()
    print()
    

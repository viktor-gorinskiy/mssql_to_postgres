from ast import Break
import pyodbc
import config

import psycopg2
import config
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2

# from datetime import date, datetime
import datetime

# ms_database = 'MegicBrainTicket'
ms_database = config.ms_database

# ps_database = config.ps_database
ps_database = ms_database

conn_ms = pyodbc.connect('DRIVER={FreeTDS};' + f"SERVER={config.ms_server};DATABASE={ms_database};UID={config.ms_username};PWD={config.ms_password}")
cursor_ms = conn_ms.cursor()


conn_ps = psycopg2.connect(dbname=ps_database, user=config.ps_username, password=config.ps_password, host=config.ps_server)
cursor_ps = conn_ps.cursor()


table = 'MTS_MobilDetalsComment'


sql_select = f"SELECT * FROM [{table}]"

def convert_type(date):
    strings=""
    c = 0
    for var in date:
        c += 1
        print('var ==>',var, type(var))
        if var is None: strings += f'NULL'
     
        elif type(var) == str:
            if var:
                strings += f"""'{var}'"""
            else: strings += f'NULL'
            
        elif type(var) == datetime.datetime: strings += f"""'{var.isoformat(" ", "microseconds")}'"""
        elif type(var) == datetime.date: strings += f"""'{var.isoformat()}'"""
        
        elif type(var) == bool:
            if var: strings += f'True'
            else: strings += f'False'
        else:
            strings += f'{var}'

        if c < len(date):
            strings += ', '

    return strings

    
columns = ['Id', 'MilKode1C', 'IdTip', 'Num', 'Note', 'DateUpdate', 'Fl_WebView', 'DateCreate']

c = 0
for row in cursor_ms.execute(sql_select):
    # c+=1
    # if c >= 10: break
    # print('\tconvert_type ==>',convert_type(row))
    print('row ==>', row)
    sql_data = convert_type(row)
    print('sql_data ==>', sql_data)

    print('\n')
    columns_str = '"' + '", "'.join(columns) + '"'
    # columns_str = ','.join(['"' + str(i) + '" ' if i else 'NULL' for i in columns])
    query =  f"""INSERT INTO "{table}" VALUES({sql_data});"""
    print('query ==>', query)
    cursor_ps.execute(query);
    conn_ps.commit()
    print()
    
# INSERT INTO "ATSLine" ("Id", "MilKode1C", "IdTip", "Num", "Note", "DateUpdate", "Fl_WebView", "DateCreate") VALUES(1609, 0, 2, '5811', 'Участок эксплуотации оборудования №1', '2022-01-20 13:06:23.687000', True, '2022-01-20');
# INSERT INTO "ATSLine" ("Id", "MilKode1C", "IdTip", "Num", "Note", "DateUpdate", "Fl_WebView", "DateCreate") VALUES(1   , , 2, '1020', 'Отделение подготовки сывороток', '2014-01-20 13:52:10.327000', True, '2014-01-20');



# print('\n','columns')
# columns = []
# ATSLine = cursor_ms.columns(table=table)                                                                                                              
# for row in ATSLine:
#     columns.append(row[3])
#     # print(row)

# print(columns)

# INSERT INTO table_name(column1, column2, …)VALUES (value1, value2, …);
# columns = ['Id', 'MilKode1C', 'IdTip', 'Num', 'Note', 'DateUpdate', 'Fl_WebView', 'DateCreate']


# # INSERT INTO Products VALUES (1, 'Galaxy S9', 'Samsung', 4, 63000)
# for src in src_dates:
#     print(src)
    
#     query =  f"INSERT INTO {table} {src};"

#     print(query)
    

    
# def insert(vendor_list):
#     """ insert multiple vendors into the vendors table  """
#     sql = "INSERT INTO vendors(vendor_name) VALUES(%s)"
#     conn = None
#     try:
#         conn = psycopg2.connect(dbname=ps_database, user=config.ps_username, password=config.ps_password, host=config.ps_server)
#         cursor = conn.cursor()
#         cursor.executemany(sql,vendor_list)
#         # commit the changes to the database
#         conn.commit()
#         # close communication with the database
#         cursor.close()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()
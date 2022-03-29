# src = ['1579', '1556', '1', '2730', '', 'datetime.datetime(2021, 5, 12, 8, 22, 1, 833000)', 'True', 'datetime.date(2021, 5, 11)']

# src = ['Id', 'MilKode1C', 'IdTip', 'Num', 'Note', 'DateUpdate', 'Fl_WebView', 'DateCreate']

# columns_str = '"' + '", "'.join(src) + '"'
# print(columns_str)

# # # import datetime
# # # d = datetime.date(2011, 1, 1)
# # # unixt = d.strftime("%s")

# # # print(unixt)


# # from datetime import date, datetime
# # from datetime import datetime, timezone


# # # date_string = "01/12/2011"
# # date_string = src[5].split('(')[1].replace(')','')
# # print(datetime.strptime(date_string, "%Y, %m, %d, %H, %M, %S, %f").fromisoformat())

# # # print(datetime.now(timezone.utc))


# values = ','.join(["'" + str(i) + "'" if i else 'NULL' for i in src])

# c = 'insert into myTable VALUES ({});'.format(values)
# print(c)

# from ast import Break
# import pyodbc
# # import config

import psycopg2
import config
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2

ps_database = config.ps_database

conn_ps = psycopg2.connect(dbname=ps_database, user=config.ps_username, password=config.ps_password, host=config.ps_server)
cursor_ps = conn_ps.cursor()

# values = ", ".join(['%s' for x in range(len(columns))])
# lll = ", ".join(columns)
# data = ("744", "1000", "Зарубеж/Роуминг", "Казахстан: K'CELL",)
# sql = 'INSERT INTO "MTS_MobilDetalsComment"  VALUES (%s, %s, %s, %s);'


data = ("747", "1000", "Зарубеж/Роуминг", "Казахстан: K'CELL",)
values = (", ".join(['%s' for x in range(len(data))]))
sql_table = "MTS_MobilDetalsComment"
sql = f'INSERT INTO "{sql_table}"  VALUES ({values});'


cursor_ps.execute(sql, data)
conn_ps.commit()


# mssql_to_postgres


```
cat /etc/odbcinst.ini
[FreeTDS]
Description = TDS driver (Sybase/MS SQL)
Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so
#Setup = /usr/lib/odbc/libtdsS.so
CPTimeout =
CPReuse =
```
### pyodbc
```
apt install tdsodbc
apt install unixodbc-dev
pip install pyodbc
```
### psycopg2
```
apt install libpq-dev
pip install psycopg2
```
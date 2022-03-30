from distutils.command.config import config
import pyodbc

class MsSql():
    
    def __init__(self, odbc_driver='', server='', port=1433, database='', username='', password=''):
        self.DRIVER = odbc_driver
        self.server = server
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.cur = None
        self.conn = None
    
    def connect(self):
        self.conn = pyodbc.connect(driver=self.DRIVER, server=self.server, database=self.database, port=self.port, uid=self.username, pwd=self.password)
        self.conn.setdecoding(pyodbc.SQL_CHAR, encoding='latin1')
        self.conn.setencoding('latin1')
        
        self.cursor = self.conn.cursor()
        
    def close(self):
        self.cur.close()
        self.conn.close()
       
    def get_columns(self, schema='', table=''):
        columns = []
        for row in self.cursor.columns(table=table, schema=schema):
            columns.append(row)
        return columns

    def return_primaryKeys(self,primaryKeys):
        return f"""PRIMARY KEY ("{primaryKeys}")"""
        
    def get_primaryKeys(self, schema='', table=''):
        primaryKeys = self.cursor.primaryKeys(table=table, schema=schema) 
        for row in primaryKeys:
            return self.return_primaryKeys(row[3])
        return False


    
    ############################################
    
    def len_columns(self, schema='', table=''):
        columns = self.cursor.columns(table=table, schema=schema)
        c = 0
        for tmp in columns:
            c+=1
        return c
    
    def len_records_in_table(self, schema, table):
        sql_count = f"SELECT COUNT(*) FROM [{self.database}].{schema}.[{table}];"
        count = self.cursor.execute(sql_count).fetchone()
        return count[0]

    def get_all_records(self, schema, table):
        sql_select = f"SELECT * FROM [{self.database}].{schema}.[{table}]"
        all_records = self.cursor.execute(sql_select)
        return all_records
        
    def get_tables(self, schema, ignore_tables=[], ignore_prefix=[]):
        tables = []
        for row in self.cursor.tables():
            if row.table_schem == schema:
                if row[3] == 'TABLE' and row[2] not in ignore_tables and not str(row[2]).startswith(tuple(ignore_prefix)):
                    tables.append(row[2])
        return tables

    def get_schemas(self):
        tmp_table_schems = []
        for table_schem in self.cursor.tables():
            tmp_table_schems.append(table_schem[1])
        table_schems = set(tmp_table_schems)
        return table_schems


# import config
# mssql = MsSql(
#     odbc_driver=config.odbc_driver,
#     server=config.ms_server,
#     port=config.ms_server_port,
#     database=config.ms_database,
#     username=config.ms_username,
#     password=config.ms_password,
# )
# mssql.connect()
# # columns = mssql.get_columns(schema='dbo', table='Workers1C_Contract')

# # for col in columns:
# #     print(col)
    
    
# tables = mssql.get_tables('dbo')

# for table in tables:
#     print(table)
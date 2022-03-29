import pyodbc

class MsSql():
    
    def __init__(self, odbc_driver, server, database, username, password):
        self.DRIVER = odbc_driver
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.cur = None
        self.conn = None
    
    def connect(self):
        self.conn = pyodbc.connect('DRIVER={FreeTDS};' + f"SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}")
        self.cursor = self.conn.cursor()
       
    def get_columns(self, table):
        columns = self.cursor.columns(table=table)
        return columns

    def return_primaryKeys(self,primaryKeys):
        return f"""PRIMARY KEY ("{primaryKeys}")"""
        
    def get_primaryKeys(self, table):
        primaryKeys = self.cursor.primaryKeys(table=table)                                                                                                  
        for row in primaryKeys:
            return self.return_primaryKeys(row[3])
        return False

    def close(self):
        self.cur.close()
        self.conn.close()
    
    ############################################
    
    def len_columns(self, table):
        columns = self.cursor.columns(table=table)
        c = 0
        for row in columns:
            c+=1
        return c
    
    def len_records_in_table(self, schema, table):
        sql_count = f"SELECT COUNT(*) FROM {self.database}.{schema}.{table};"
        return self.cursor.execute(sql_count).fetchone()[0]

    def get_all_records(self, schema, table):
        sql_select = f"SELECT * FROM {self.database}.{schema}.{table}"
        all_records = self.cursor.execute(sql_select)
        return all_records
        
    def get_tables(self, schema, ignore_tables=[]):
        tables = []
        for row in self.cursor.tables():
            if row.table_schem == schema:
                if row[3] == 'TABLE' and row[2] not in ignore_tables:
                    tables.append(row[2])
        return tables

    def get_schemas(self):
        tmp_table_schems = []
        for table_schem in self.cursor.tables():
            tmp_table_schems.append(table_schem[1])
        table_schems = set(tmp_table_schems)
        return table_schems
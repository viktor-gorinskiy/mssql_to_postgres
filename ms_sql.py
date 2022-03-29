import pyodbc

class MsSql():
    
    def __init__(self, odbc_driver, table_schem, server, database, username, password):
        self.DRIVER = odbc_driver
        self.server = server
        self.database = database
        self.table_schem = table_schem
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
    
    def len_records_in_table(self, table):
        sql_count = f"SELECT COUNT(*) FROM {self.database}.{self.table_schem}.{table};"
        return self.cursor.execute(sql_count).fetchone()[0]

    def get_all_records(self, table):
        sql_select = f"SELECT * FROM [{table}]"
        all_records = self.cursor.execute(sql_select)
        return all_records
        
    def get_tables(self, ignore_tables=[]):
        tables = []
        for row in self.cursor.tables():
            if row.table_schem == self.table_schem:
                if row[3] == 'TABLE' and row[2] not in ignore_tables:
                    tables.append(row[2])
        return tables

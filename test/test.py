# import config
# odbc_driver = 'FreeTDS'



# a = 'DRIVER={FreeTDS};' + f"SERVER={config.ms_server};DATABASE={config.ms_database};UID={config.ms_username};PWD={config.ms_password}"
# b = f'DRIVER={{FreeTDS}};SERVER={config.ms_server};DATABASE={config.ms_database};UID={config.ms_username};PWD={config.ms_password}'
# print(a)
# print(b)

# def insert(a, b):
#     print(b, len(a))


# count_records_table = 5030
# pull = 1000
# c = 0
# sql_s = []



# for row in range(count_records_table):
#     c += 1
#     sql_s.append(row)
    
#     if not c%pull:
#         insert(sql_s, 'tic')
#         sql_s = []
        
#     # if c == count_records_table:
    
# insert(sql_s, 'end')
# sql_s = []

# class MStoPGsql():
    
#     def __init__(self, **kwargs ):
#         print (kwargs)
#         print(kwargs['odbc_driver'])
        

# import config

# mssql = MStoPGsql(
#     odbc_driver=config.odbc_driver,
#     server=config.ms_server,
#     database=config.ms_database,
#     username=config.ms_username,
#     password=config.ms_password,
#     table_schem=config.table_schem
# )


c = [
    '_1C_Synchronization',
    '_FIO_Last',
    '_Workers1C_Contract',
    'test'
    ]

prefixes = ['_', 'v']


s = '_hello world'
# prefixes = ['hi', 'bye', 'no']

for a in c:
    result = a.startswith(tuple(prefixes))
    print(a, result)
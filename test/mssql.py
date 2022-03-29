import pyodbc
import config


# ms_database = 'MagicBrain'
ms_database = config.ms_database


connection = pyodbc.connect('DRIVER={FreeTDS};' + f"SERVER={config.ms_server};DATABASE={ms_database};UID={config.ms_username};PWD={config.ms_password}")
cursor = connection.cursor()

# print(cursor.tables())

# for row in cursor.tables():
#     print(row)


table = 'MTS_MobilDetalsComment'
c = 1
for row in cursor.tables():
    # if row.table_schem == "dbo":
    c +=1
    # print(c, row[2])
    print(c, row)
        # if row[3] == 'TABLE' and row[2] != 'sysdiagrams':
        #     c +=1
        #     print(c, row)
        # print('\t',row.remarks)
        
# cursor.tables()
# columns = [column[0] for column in cursor.description]
# print('===>',columns)


tmp_table_schems = []
for table_schem in cursor.tables():
    tmp_table_schems.append(table_schem[1])
table_schems = set(tmp_table_schems)

print(table_schems)


print('\n','columns')
columns = cursor.columns(table=table)                                                                                                              
for row in columns:
    print(row)


print('\n','primaryKeys')
primaryKeys = cursor.primaryKeys(table=table)                                                                                                        
for row in primaryKeys:
    print(row)


print('\n', 'foreignKeys')
foreignKeys = cursor.foreignKeys(table=table)
for row in foreignKeys:
     print(row)
    #  print(dict(zip(columns, row)))
     
     
# table_cat
# table_schem
# table_name
# column_name
# data_type
# type_name
# column_size
# buffer_length
# decimal_digits
# num_prec_radix
# nullable
# remarks
# column_def
# sql_data_type
# sql_datetime_sub
# char_octet_length
# ordinal_position
# is_nullable: One of SQL_NULLABLE, SQL_NO_NULLS, SQL_NULLS_UNKNOWN.
    
     
# #Sample select query
# cursor.execute("SELECT @@version;") 
# row = cursor.fetchone() 
# while row: 
#     print(row[0])
#     row = cursor.fetchone()

        
        



# Microsoft SQL Serve
ms_database = '1C_Employees'
ms_server = '10-sqltest-vsrv'
ms_server_port = 1433
ms_username = 'gorinskiy' 
ms_password = 'gorinskiy1'
odbc_driver = 'FreeTDS'
ignore_schemas = ['INFORMATION_SCHEMA', 'sys']
ignore_tables = ['sysdiagrams', 'pLogData', 'Demand_Archiv']
ignore_prefix = ['_']

# Postgres
pg_database = ms_database
pg_username = 'postgres_user'
pg_password = 'phuX6neWohg1Pexuh3phuyeeLe3Hoh'
pg_server   = 'postgres.vbest.local'
pg_server_port = 5432

# Settings
drop_tables = True #False
pull = 5000

# Microsoft SQL Serve
ms_database = 'VBSite'
ms_server = '10-sqltest-vsrv,1433'
ms_username = 'gorinskiy' 
ms_password = 'gorinskiy1'
odbc_driver = 'FreeTDS'
ignore_schemas = ['INFORMATION_SCHEMA', 'sys']
ignore_tables=['sysdiagrams']

# Postgres
pg_database = ms_database
pg_username = 'postgres_user'
pg_password = 'phuX6neWohg1Pexuh3phuyeeLe3Hoh'
pg_server   = 'postgres.vbest.local'

# Settings
drop_tables = True #False
pull = 1000
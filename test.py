# from sqlalchemy import create_engine
# import pandas as pd
# import numpy as np



# engine = create_engine('mysql+pymysql://root:root123@localhost:5306/test_db')
# databases = pd.read_sql_query("show databases", engine)
# df = pd.DataFrame(np.random.random((3,3)), columns = ['A','B','C'])
# df.to_sql("testtable", engine, index = False, if_exists = "replace")
# pd.read_sql_query("select * from testtable", engine)



import requests
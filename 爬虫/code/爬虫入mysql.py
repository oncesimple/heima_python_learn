import pandas as pd
from sqlalchemy import create_engine,Table,Column,Integer,String,MetaData,ForeignKey

engine = create_engine("mysql+pymysql://账户:密码@主机地址:端口/")
name = 0
nb = engine.execute(f"show databases;")
print(nb.first())
# data_df = pd.DataFrame()
# data_df.to_sql(name= "test tab", con=engine, if_exists= "append", dtype= {"id":VARCHAR(10)})


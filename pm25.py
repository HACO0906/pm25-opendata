import pymysql
import pandas as pd
import requests,io
from datetime import datetime
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os
from dotenv import load_dotenv

load_dotenv()
def get_data():
    print("取得pm2.5資料中")
    try:
         #api_url="https://data.moenv.gov.tw/api/v2/aqx_p_02?api_key=af57253c-e838-46da-a1f5-12b43afd75f3&limit=1000&sort=datacreationdate%20desc&format=CSV"

        api_url="https://data.moenv.gov.tw/api/v2/aqx_p_02?api_key=846e44e1-8cc5-4893-ad87-c79d2d383706&limit=1000&sort=datacreationdate%20desc&format=JSON"
        resp=requests.get(api_url,verify=False)
        print(resp)
        df=pd.read_json(io.StringIO(resp.text))
        df1=df.drop_duplicates(subset=["site","datacreationdate"]).dropna()
        df1
        data=df1.values.tolist()
        print(df)

        return data
    except Exception as e:
      print(e)
    return None
    

def insert_data(data):
    print(data)
    try:
        sqlstr='insert  ignore into data (site,county,pm25,datacreationdate,itemunit)\
        values(%s,%s,%s,%s,%s)'
        cursor.executemany(sqlstr,data)   
        conn.commit()
        if cursor.rowcount==0:
            print("目前更新資料")
        print(f"新增{cursor.rowcount}筆資料!") 
    except Exception as e:
        print(e)
        

def open_db():
  try:
    conn = pymysql.connect(
        host=os.environ.get("HOST"),
        port=int(os.environ.get("PORT")),
        user=os.environ.get("USER"),
        password=os.environ.get("PASSWORD"),
        database=os.environ.get("NAME"),
        ssl={"ca":None}
    )

    cursor = conn.cursor()
    return conn,cursor
  except Exception as e:
         print(e)
  return None,None

conn, cursor = open_db()

print(conn, cursor)

def create_table():
    global conn,cursor
    try:
        sqlstr='''
        create table if not exists data(
        id int primary key auto_increment,
        site varchar(50),
        county varchar(20),
        pm25 int,
        datacreationdate datetime,
        itemunit varchar(20),
        unique key uq_site_datacreationdate (site,datacreationdate)
        )
        '''
        index=cursor.execute(sqlstr)
        conn.commit()   

        cursor.execute(sqlstr)
        conn.commit()
        print("建立資料表成功!")
    except Exception as e:
        print(e)

print("---------------------------------")
print(f"運行時間:{datetime.now()}")
conn,cursor=open_db()

if conn is not None:

   create_table()
   data=get_data()
   #print(data)
   if data:
       insert_data(data)
   else:
       print("目前無更新資料")
   conn.close()
else:
    print("資料開啟失敗!") 

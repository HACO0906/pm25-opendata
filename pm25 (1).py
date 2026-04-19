import pymysql


def open_db():
    conn=pymysql.connect(
        host="gateway01.ap-northeast-1.prod.aws.tidbcloud.com",
        port=4000,
        user="6pYHNSdgs1tSGNy.root",
        password="PrIq2wAnkgMtb352",
        database="test",
        ssl={"ca":"isrgrootx1.pem"}
    )

    cursor=conn.cursor()

    return conn,cursor


def create_table():
    global conn,cursor
    try:
        # unique  插入資料唯一的約束
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
       
        cursor.execute(sqlstr)
        conn.commit()
        print("建立資料表成功!")
    except Exception as e:
        print(e)




conn,cursor=open_db()
print(conn,cursor)

create_table()

conn.commit()



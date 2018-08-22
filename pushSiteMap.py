#数据库操作库
import pymysql,os,time,json,requests
#ORM 框架
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.TBootstrapRes import TBootstrapRes
from models.TCode import TCode

import env
_env=env.initEnv()
pymysql.install_as_MySQLdb()
#链接数据库
engine = create_engine(_env["python_sql"])
DB_Session = sessionmaker(bind=engine)
session = DB_Session()

code=session.query(TCode).filter(TCode.code=='BD_PUSH_BOOT_RES_ID').first()
tid=0;
if code.code_val != None:
	tid = int(code.code_val)
	print("code值:"+code.code_val)
resList = session.query(TBootstrapRes).filter(TBootstrapRes.tid>tid).order_by(TBootstrapRes.tid.asc()).all()
data=""
for res in resList :
	pushUrl=_env["domain"]+"detail/"+res.dir_name
	print("push地址:%s"%(pushUrl))
	data+=pushUrl+"\n"
	tid = res.tid
code.code_val=tid
session.commit()
session.close()
url="http://data.zz.baidu.com/urls?site=www.17sobt.com&token=ybn6pppfWpVrVkqq"
print(data)
if data!="":
	result = requests.request('POST' , url, data=data, verify=False ,timeout = 5)
	print(result.json())
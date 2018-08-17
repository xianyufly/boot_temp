#数据库操作库
import pymysql,os,time,json,requests
#ORM 框架
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from thirdFileUtil import weiyun
from thirdFileUtil import zipCompress
from models.TBootstrapRes import TBootstrapRes
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import env
_env=env.initEnv()
#链接数据库
engine = create_engine(_env["python_sql"])
DB_Session = sessionmaker(bind=engine)
session = DB_Session()

'''[summary]
初始化环境
[description]
'''
def initEnv(p_dir_name):
	dir_name = str(time.time())
	account_str=weiyun.init()
	rootDirKey, mainDirKey = weiyun.getRootAndMainDirKey()
	# 先在主文件夹下创建父文件夹
	dir_key, pdir_key = weiyun.wy_diskDirCreate(
	    mainDirKey, rootDirKey, p_dir_name)
 	# 再在父文件夹下创建文章文件夹
	dir_key, p_dir_key = weiyun.wy_diskDirCreate(dir_key, pdir_key, dir_name)
	return dir_name, dir_key, p_dir_key,account_str

try :
	#工作目录
	workfolder=_env['zip_work']
	templatefolder=workfolder+"/zip";
	list_file = os.listdir(templatefolder)
	for i in list_file:
		#读取json 描述文件
		jsonPath=templatefolder+"/"+i+"/desc.json"
		json_object = open(jsonPath,'r', encoding='utf-8')
		try:
			file_context = json_object.read()
			data=json.loads(file_context)
		finally:
			json_object.close()
		num=session.query(TBootstrapRes).filter(TBootstrapRes.code==data['code']).count()
		if num == 0 :
			dir_name, dir_key, p_dir_key,account_str=initEnv("bootstap_template");
			tempImg=templatefolder+"/"+i+"/screen.png"
			#上传封面图片到微云并转化图片地址
			file_id, filename=weiyun.wy_fileUpload(dir_key,p_dir_key,tempImg)
			share_url=weiyun.wy_shareUrl(dir_key,file_id, filename)
			if share_url != "" :
				weiyun.initWebDriver()
				face_url=weiyun.wy_filePath(share_url,"img")
				weiyun.quitWebDriver()
			else :
				face_url=""
			#上传zip文件到微云
			zipPath=templatefolder+"/"+i+"/"+i+".zip"
			file_id, filename=weiyun.wy_fileUpload(dir_key,p_dir_key,zipPath)
			#copy zip 文件到 /data/www/html目录 并解压 然后生成预览地址
			zipCompress.uncompress(zipPath,_env['html_aim_path']+"/"+i)
			view_url=_env['preview_domain']+i+"/index.html"
			res=TBootstrapRes(file_id=file_id,title=data['title'],memo=data['memo'],code=data['code'],view_url=view_url,face_url=face_url,dir_key=dir_key,p_dir_key=p_dir_key,dir_name=dir_name,qq=account_str)
			session.add(res)
			session.commit()
finally:
	#保存对象文件到数据库
	session.close()
import os,time,json
from thirdFileUtil import filterSubffix,cutImage,zipCompress
import env
_env=env.initEnv()
#整理下载资源
workfolder=_env['zip_work']
templatefolder=workfolder+"/template";
list_file = os.listdir(templatefolder)
for i in list_file :
	htmlWorkfolder=workfolder+"/template/"+i
	filterSubffix.dealWith(htmlWorkfolder)
#下载资源首页截图 并打水印
for i in list_file :
	#判断是否有desc.json 描述文件
	descPath=workfolder+"/template/"+i+"/desc.json"
	if os.path.exists(descPath) == True:
		#创建文件
		file_object = open(descPath,'r', encoding='utf-8')
		try:
			file_context = file_object.read()
			data=json.loads(file_context)
		finally:
			file_object.close()
	else :
		break

	htmlWorkfolder=workfolder+"/template/"+i
	pagePath=htmlWorkfolder+"/index.html"
	if os.path.exists(pagePath) != True:
		break;
	zipFolderName=data['code']
	cutImageSavePath=workfolder+"/zip/"+zipFolderName
	if os.path.exists(cutImageSavePath) != True:
	    os.makedirs(cutImageSavePath)
	cutImage.dealwith(pagePath,cutImageSavePath)
	get_files_path=workfolder+"/template/"+i
	set_files_path=cutImageSavePath+"/"+zipFolderName+".zip"
	#打包到对应目录
	zipCompress.dealwith(get_files_path,set_files_path);
	#判断是否有desc.json 描述文件
	descPath=cutImageSavePath+"/desc.json"
	jsonPath=workfolder+"/template/"+i+"/desc.json"
	if os.path.exists(descPath) != True:
		#创建文件
		file_object = open(descPath,'w', encoding='utf-8')
		json_object = open(jsonPath,'r', encoding='utf-8')
		try:
			file_context = json_object.read()
			file_object.seek(0)
			file_object.truncate()
			file_object.write(file_context)
		finally:
			file_object.close()
			json_object.close()
#上传打包文件和首页截图到微云,打包文件到项目目录,保存资源到数据库
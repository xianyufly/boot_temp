'''[summary]
环境变量模块

[description]
'''
import platform


sysstr = platform.system()

def initEnv():
	env={
		"chrome_driver_path":"",
		"python_sql":"",
		#html 目录
		"html_aim_path":"",
		#预览地址
		"preview_domain":"",
		#zip工作目录
		"zip_work":"",
		#网站域名
		"domain":"",
		#siteMap文件路径
		"sitemap_path":""
	}
	if(sysstr =="Windows"):
		#window平台
		env["chrome_driver_path"]="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe"
		env["python_sql"]="mysql+mysqldb://root:xian0402@localhost:3306/news"
		env["html_aim_path"]="D:\\Apache2.4\\htdocs"
		env["preview_domain"]="http://localhost/"
		env["zip_work"]="C:\\Users\\Administrator\\Desktop\\work"
		env["domain"]="http://localhost:3000/"
		env["sitemap_path"]="C:\\Users\\Administrator\\Desktop\\python_news\\pro_zx_nuxt\\site.txt"
	elif(sysstr == "Linux"):
		#linux平台
		env["chrome_driver_path"]="/usr/local/chromedriver"
		env["python_sql"]="mysql+mysqldb://17sobt.com:17sobt.com@123456@localhost:6306/news"
		env["html_aim_path"]="/data/www/html"
		env["preview_domain"]="https://demo.17sobt.com/"
		env["zip_work"]="/data/pythonwork/wrok"
		env["domain"]="https://www.17sobt.com/"
		env["sitemap_path"]="/data/www/pro/site.txt"
	return env
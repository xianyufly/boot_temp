'''[summary]
过滤文件夹后缀
[description]
'''
import os
import re

def endWith(*endstring):
	ends=endstring
	def run(s):
		f=map(s.endswith,ends)
		if True in f: 
			return s
	return run
def copyImg(workfolder):
	aimfolder = workfolder+"/images"
	if os.path.exists(aimfolder) != True:
	    # 创建文件夹
	    os.makedirs(aimfolder)
	list_file = os.listdir(workfolder)
	a = endWith('.png','.jpg','.gif','.jpeg')
	f_file = filter(a,list_file)
	for i in f_file:
		sourceFile=workfolder+"/"+i
		targetFile=aimfolder+"/"+i
		os.rename(sourceFile, targetFile)
def copyJs(workfolder):
	aimfolder = workfolder+"/js"
	if os.path.exists(aimfolder) != True:
	    # 创建文件夹
	    os.makedirs(aimfolder)
	list_file = os.listdir(workfolder)
	a = endWith('.js')
	f_file = filter(a,list_file)
	for i in f_file:
		sourceFile=workfolder+"/"+i
		targetFile=aimfolder+"/"+i
		os.rename(sourceFile, targetFile)
def copyCss(workfolder):
	aimfolder = workfolder+"/css"
	if os.path.exists(aimfolder) != True:
	    # 创建文件夹
	    os.makedirs(aimfolder)
	list_file = os.listdir(workfolder)
	a = endWith('.css')
	f_file = filter(a,list_file)
	for i in f_file:
		sourceFile=workfolder+"/"+i
		targetFile=aimfolder+"/"+i
		os.rename(sourceFile, targetFile)
def copyFont(workfolder):
	aimfolder = workfolder+"/css"
	if os.path.exists(aimfolder) != True:
	    # 创建文件夹
	    os.makedirs(aimfolder)
	list_file = os.listdir(workfolder)
	a = endWith('.eot','.woff','.ttf','.svg')
	f_file = filter(a,list_file)
	for i in f_file:
		sourceFile=workfolder+"/"+i
		targetFile=aimfolder+"/"+i
		os.rename(sourceFile, targetFile)
#拷贝字体文件到css
def copyFontToCss(workfolder):
	aimfolder = workfolder+"/css"
	if os.path.exists(aimfolder) != True:
	    # 创建文件夹
	    os.makedirs(aimfolder)
	list_file = os.listdir(workfolder)
	for i in list_file:
		match = re.match(r'(.*)\.eot-(.*)|(.*)\.svg-(.*)|(.*)\.ttf-(.*)|(.*)\.woff[1-9]?-(.*)|(.*)\.woff[1-9]', i)
		if match:
			sourceFile=workfolder+"/"+i
			targetFile=aimfolder+"/"+i
			os.rename(sourceFile, targetFile)

#替换script路径
def switchScriptSrc(matched):
	srcipt=matched.group("script")
	src=matched.group("src")
	tppabs=matched.group("tppabs")
	if src.startswith("js/")==False:
		aimSrc="js/"+src
		srcipt=srcipt.replace(src,aimSrc)
	if tppabs !=None :
			srcipt=srcipt.replace(tppabs,"")
	return srcipt
def regReplaceScript(content):
	newStr = re.sub(
	    r"(?P<script><script [^>]*src=[\'\"](?P<src>[^\'\"]+)[^>]* [^>]*tppabs=[\'\"](?P<tppabs>[^\'\"]+)[^>]*?></script>)", switchScriptSrc, content)
	return newStr
#替换css路径
def switchCssSrc(matched):
	srcipt=matched.group("link")
	src=matched.group("href")
	tppabs=matched.group("tppabs")
	if src.startswith("css/")==False:
		aimSrc="css/"+src
		srcipt=srcipt.replace(src,aimSrc)
	if tppabs !=None :
			srcipt=srcipt.replace(tppabs,"")
	return srcipt
def regReplaceLink(content):
	newStr = re.sub(
	    r"(?P<link><link [^>]*href=[\'\"](?P<href>[^\'\"]+)[^>]* [^>]*tppabs=[\'\"](?P<tppabs>[^\'\"]+)[^>]*?>)", switchCssSrc, content)
	return newStr
#替换image路径
def switchImageSrc(matched):
	srcipt=matched.group("img")
	src=matched.group("src")
	tppabs=matched.group("tppabs")
	if src.startswith("images/")==False:
		aimSrc="images/"+src
		srcipt=srcipt.replace(src,aimSrc)
	if tppabs !=None :
			srcipt=srcipt.replace(tppabs,"")
	return srcipt
def regReplaceImg(content):
	newStr = re.sub(
	    r"(?P<img><img [^>]*src=[\'\"](?P<src>[^\'\"]+)[^>]* [^>]*tppabs=[\'\"](?P<tppabs>[^\'\"]+)[^>]*?>)", switchImageSrc, content)
	return newStr

#替换image路径
def switchATag(matched):
	srcipt=matched.group("alink")
	src=matched.group("href")
	tppabs=matched.group("tppabs")
	if tppabs !=None :
			srcipt=srcipt.replace(tppabs,"")
			# htmlPath=tppabs.split("/")
			# srcipt=srcipt.replace(src,htmlPath)
	return srcipt
def regReplaceATag(content):
	newStr = re.sub(
	    r"(?P<alink><a [^>]*href=[\'\"](?P<href>[^\'\"]+)[^>]* [^>]*tppabs=[\'\"](?P<tppabs>[^\'\"]+)[^>]*?>)", switchATag, content)
	return newStr
def swithchBack(matched):

	style=matched.group("style")
	src=matched.group("src")
	if src.startswith("images/")==False:
		aimSrc="images/"+src
		style=style.replace(src,aimSrc)
	return style
#处理背景图片
def regReplaceBackImg(content):
	newStr = re.sub(
	    r"(?P<style>style=[\'\"][^\'\"]*background-image:\s*url\(\"(?P<src>[^\(\)\"\']+)\"\)[^\'\"]*?[\'\"])", swithchBack, content)
	newStr = re.sub(
	    r"(?P<style>style=[\'\"][^\'\"]*background:\s*url\((?P<src>[^\(\)\"\']+)\)[^\'\"]*?[\'\"])", swithchBack, newStr)
	# newStr=newStr.replace('data-src="images/images/','data-src="images/')
	return newStr

def operHtml(workfolder):
	list_file = os.listdir(workfolder)
	a = endWith('.html','htm')
	f_file = filter(a,list_file)
	for i in f_file:
		#处理HTML路径
		htmlPath=workfolder+"/"+i
		# htmlPath=workfolder+"/index.html"
		file_object = open(htmlPath,'r+', encoding='utf-8')
		try:
			file_context = file_object.read()
			file_context = regReplaceScript(file_context)
			file_context = regReplaceLink(file_context)
			file_context = regReplaceImg(file_context)
			file_context = regReplaceATag(file_context)
			file_context = regReplaceBackImg(file_context)
			file_object.seek(0)
			file_object.truncate()
			file_object.write(file_context)
		finally:
			file_object.close()
def dealWith(workfolder):
	copyImg(workfolder)
	copyJs(workfolder)
	copyCss(workfolder)
	copyFontToCss(workfolder)
	copyFont(workfolder)
	operHtml(workfolder)
if __name__ == '__main__':
	workfolder="C:\\Users\\Administrator\\Desktop\\work\\template\\dist-flatify"
	copyImg(workfolder)
	copyJs(workfolder)
	copyCss(workfolder)
	copyFontToCss(workfolder)
	copyFont(workfolder)
	operHtml(workfolder)
	
	# list_file = os.listdir("C:\\Users\\Administrator\\Desktop\\webapplayers")
	# a = endWith('.png')
	# f_file = filter(a,list_file)
	# for i in f_file:
	# 	print(i)
	# 	os.rename(sourceFile, targetFile)

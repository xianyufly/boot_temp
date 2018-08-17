#!/usr/bin/env python
#coding:utf-8

import zipfile,os
import shutil
#把整个文件夹内的文件打包成zip文件（包括压缩路径下的字文件夹的文件）
def compress(get_files_path, set_files_path):
    f = zipfile.ZipFile(set_files_path , 'w', zipfile.ZIP_DEFLATED )
    for dirpath, dirnames, filenames in os.walk( get_files_path ):      
        fpath = dirpath.replace(get_files_path,'') #注意2
        fpath = fpath and fpath + os.sep or ''     #注意2
        for filename in filenames: 
            f.write(os.path.join(dirpath,filename), fpath+filename)
    comment="\
    #####################免责声明###########################\n\
    1. 17sobt.com 本站资源来源于网络,仅用于学习使用,请勿用于商业\n\
       用途，否则产生的一切后果将由您自己承担！\n\
    2. 网页模板都是站长从国外大小网站收集而来，旨在为朋友们在工作或\n\
       学习时提高效率、节省时间\n\
    #########################################################\
    "
    f.comment=bytes(comment.encode('GBK'))
    f.close()
    print("compress operate success")

def uncompress(sourceZipPath,aimDirPath):
    filename = sourceZipPath  #要解压的文件
    filedir = aimDirPath  #解压后放入的目录
    if os.path.exists(aimDirPath) != True:
        # 创建文件夹
        os.makedirs(aimDirPath)
    else:
        shutil.rmtree(aimDirPath)
    r = zipfile.is_zipfile(filename)
    if r:
        fz = zipfile.ZipFile(filename,'r')
        for file in fz.namelist():
            fz.extract(file,filedir)
    else:
        print('This file is not zip file')

def dealwith(get_files_path,set_files_path):
    compress(get_files_path, set_files_path)

if __name__=='__main__':
    get_files_path = "C:\\Users\\Administrator\\Desktop\\work\\template\\webapplayers" #需要压缩的文件夹
    aim_folder_path = "C:\\Users\\Administrator\\Desktop\\work\\zip\\webapplayers"
    if os.path.exists(aim_folder_path) != True:
        # 创建文件夹
        os.makedirs(aim_folder_path)
    set_files_path = aim_folder_path+"\\webapplayers.zip" #存放的压缩文件地址(注意:不能与上述压缩文件夹一样)
    compress(get_files_path, set_files_path) 
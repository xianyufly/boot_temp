"""[summary]
微云服务器--上传
[description]
"""
import os
import time
import requests
import urllib
import json
import re
import random 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# sha1 加密算法
from hashlib import sha1
import base64
# 导入支持双击操作的模块
from selenium.webdriver import ActionChains

#数据库操作库
import pymysql
#ORM 框架
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import sys
sys.path.append("..")
from models.WyCookie import WyCookie
from models.WyQq import WyQq
from models.TArticle import TArticle
from thirdFileUtil import ipPool
import env
#系统变量
_env=env.initEnv()

pymysql.install_as_MySQLdb()
#链接数据库
engine = create_engine(_env["python_sql"])
DB_Session = sessionmaker(bind=engine)

'''
初始化driver
'''
def initChromeDriver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument("--no-sandbox")
    # 对应的chromedriver的放置目录
    driver = webdriver.Chrome(executable_path=(
        _env["chrome_driver_path"]), chrome_options=chrome_options)
    return driver


# # 微云账号
# account_str = "1187383721"
# pwd_str = "mirror0402"

# 公用变量
web_wx_rc = ""
pgv_pvi = ""
pgv_si = ""
ptisp = ""
ptui_loginuin = ""
pt2gguin = ""
uin = ""
skey = ""
ptcz = ""
p_uin = ""
pt4_token = ""
p_skey = ""
wyctoken = ""

# 全局变量
rootDirKey, mainDirKey = "", ""
'''
返回根目录key
'''


def getRootAndMainDirKey():
    global rootDirKey, mainDirKey
    return rootDirKey, mainDirKey


'''
返回cookie内容
'''


def getCookieByParam(cookieData, key, domain=""):
    val = ""
    # 初始化要获取的cookie
    for item in cookieData:
        if domain == "" and item["name"] == key:
            val = item["value"]
        elif domain != "" and item["name"] == key and item["domain"] == domain:
            val = item["value"]
    return val

'''
代理请求--普通post请求
'''
def proxyRquest_normal(url,data,headers):
    targeturl = "https://www.weiyun.com"
    flag = True
    while flag:
        try :
            # begTime = time.time()
            proxy_addr=ipPool.randomGetIp(targeturl)
            # endTime = time.time()
            # print("代理IP获取时间:%s"%(str(endTime-begTime)))
            proxies = {
              "http": "http://"+proxy_addr,
              "https": "http://"+proxy_addr,
            }
            flag=False
            # begTime = time.time()
            result = requests.request('POST' , url, proxies = proxies, data=json.dumps(
                data), headers=headers, verify=False ,timeout = 5)
            # endTime = time.time()
            # print("代理请求时间:%s"%(str(endTime-begTime)))
        except requests.exceptions.ProxyError as err:
            flag=True
        except WinError as err:
            print(err)
            flag=True
        
    return result

'''
代理请求--文件上传post请求
'''
def proxyRquest_file(url,data,files,headers):
    targeturl = "https://www.weiyun.com"
    flag = True
    while flag:
        try :
            proxy_addr=ipPool.randomGetIp(targeturl)
            proxies = {
              "http": "http://"+proxy_addr,
              "https": "http://"+proxy_addr,
            }
            flag=False
            result = requests.request('POST', url, proxies = proxies, data=data,
                              files=files, headers=headers, verify=False)
        except requests.exceptions.ProxyError as err:
            flag=True
    return result

    

'''
微云--初始化
参数

返回

'''


def init():
    global web_wx_rc, pgv_pvi, pgv_si, ptisp, ptui_loginuin, pt2gguin, uin, skey, ptcz, p_uin, pt4_token, p_skey, wyctoken
    global rootDirKey, mainDirKey
    #
    session = DB_Session()
    # tid = session.query(func.max(TArticle.tid)).first()
    tid = int(time.time())
    print(tid)
    mod = session.query(WyQq).filter(WyQq.is_can_upload ==0).all()
    offset =0
    if(tid!=None):
        offset=tid%len(mod)
    qq=session.query(WyQq).filter(WyQq.is_can_upload ==0).order_by(WyQq.tid.asc()).limit(1).offset(offset).first()

    account_str=qq.account_str
    pwd_str=qq.pwd_str
    print("tid:%s,account_str:%s"%(tid,account_str))
    #从数据库查询cookie
    wycookieTeamp = session.query(WyCookie).filter(WyCookie.account_str == account_str).first()
    if(wycookieTeamp):
        web_wx_rc = wycookieTeamp.web_wx_rc
        pgv_pvi = wycookieTeamp.pgv_pvi
        pgv_si = wycookieTeamp.pgv_si
        ptisp = wycookieTeamp.ptisp
        ptui_loginuin = wycookieTeamp.ptui_loginuin
        pt2gguin = wycookieTeamp.pt2gguin
        uin = wycookieTeamp.uin
        skey = wycookieTeamp.skey
        ptcz = wycookieTeamp.ptcz
        p_uin = wycookieTeamp.p_uin
        pt4_token = wycookieTeamp.pt4_token
        p_skey = wycookieTeamp.p_skey
        wyctoken = wycookieTeamp.wyctoken
        rootDirKey = wycookieTeamp.rootDirKey
        mainDirKey = wycookieTeamp.mainDirKey
        # 验证cookie是否可以使用
        flag=wy_safeBox()
        if flag :
            print("success")
            return account_str;
    try:
        driver = initChromeDriver()
        url = "https://www.weiyun.com"
        driver.get(url)
        driver.switch_to_frame("qq_login_iframe")
        driver.get_screenshot_as_file("weiyun.png")
        switch = driver.find_element_by_id("switcher_plogin")
        switch.click()
        account = driver.find_element_by_id("u")
        account.send_keys(account_str)
        pwd = driver.find_element_by_id("p")
        pwd.send_keys(pwd_str)
        loginButton = driver.find_element_by_id("login_button")
        loginButton.click()
        # 获取root_dir_key
        flag = True
        reg = re.compile(r'\"root_dir_key\":\"(.*?)\"')

        while flag:
            try:
                rootDirKeyArray = reg.findall(driver.page_source)
                rootDirKey = rootDirKeyArray[0]
                flag = False
            except:
                flag = True
            finally:
                time.sleep(0.1)
        # 获取 main_dir_key
        flag = True
        reg = re.compile(r'\"main_dir_key\":\"(.*?)\"')
        while flag:
            try:
                mainDirKeyArray = reg.findall(driver.page_source)
                mainDirKey = mainDirKeyArray[0]
                flag = False
            except:
                flag = True
            finally:
                time.sleep(0.1)
        # 获取网站cookie
        cookie = driver.get_cookies()
        web_wx_rc = getCookieByParam(cookie, "web_wx_rc", ".weiyun.com")
        pgv_pvi = getCookieByParam(cookie, "pgv_pvi", ".weiyun.com")
        pgv_si = getCookieByParam(cookie, "pgv_si", ".weiyun.com")
        ptisp = getCookieByParam(cookie, "ptisp", ".weiyun.com")
        ptui_loginuin = getCookieByParam(cookie, "ptui_loginuin", ".weiyun.com")
        pt2gguin = getCookieByParam(cookie, "pt2gguin", ".weiyun.com")
        uin = getCookieByParam(cookie, "uin", ".weiyun.com")
        skey = getCookieByParam(cookie, "skey", ".weiyun.com")
        ptcz = getCookieByParam(cookie, "ptcz", ".weiyun.com")
        p_uin = getCookieByParam(cookie, "p_uin", ".weiyun.com")
        pt4_token = getCookieByParam(cookie, "pt4_token", ".weiyun.com")
        p_skey = getCookieByParam(cookie, "p_skey", ".weiyun.com")
        wyctoken = getCookieByParam(cookie, "wyctoken", ".weiyun.com")
        #删除旧数据
        wycookie=WyCookie(account_str=account_str,web_wx_rc=web_wx_rc,pgv_pvi=pgv_pvi,pgv_si=pgv_si,ptisp=ptisp,ptui_loginuin=ptui_loginuin
            ,pt2gguin=pt2gguin,uin=uin,skey=skey,ptcz=ptcz,p_uin=p_uin,pt4_token=pt4_token,p_skey=p_skey,wyctoken=wyctoken,rootDirKey=rootDirKey,mainDirKey=mainDirKey)
        if(wycookieTeamp):
            session.delete(wycookieTeamp)
        session.add(wycookie)
        session.commit()
        return account_str        
    except Exception as err:
        print("fail")
    finally:
        session.close()
        # 关闭浏览器
        driver.quit()

'''[summary]
微云 - 获取腾讯微云下载地址
参数
pdir_key:上级目录
file_id: 文件ID
file_name:文件名称
[description]
'''
def wy_safeBox():
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "content-type": "application/json;charset=UTF-8",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": "web_wx_rc=%s; pgv_pvi=%s; pgv_si=%s; ptisp=%s; ptui_loginuin=%s; pt2gguin=%s; uin=%s; skey=%s; ptcz=%s; p_uin=%s; pt4_token=%s; p_skey=%s; wyctoken=%s" % (web_wx_rc, pgv_pvi, pgv_si, ptisp, ptui_loginuin, pt2gguin, uin, skey, ptcz, p_uin, pt4_token, p_skey, wyctoken),
        "origin": "https://www.weiyun.com",
        "referer": "https://www.weiyun.com/disk",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
    }
    req_header = {
        "seq": int(str(int(time.time()))+'6484240'),
        "type": 1,
        "cmd": 2402,
        "appid": 30013,
        "version": 3,
        "major_version": 3,
        "minor_version": 3,
        "fix_version": 3,
        "wx_openid": "",
        "user_flag": 0
    }
    req_body = {
        "ReqMsg_body": {
            "ext_req_head": {
                "token_info": {
                    "token_type": 0,
                    "login_key_type": 1,
                    "login_key_value": skey
                }
            },
            ".weiyun.SafeBoxCheckStatusMsgReq_body":  {
            }
        }
    }
    data = {
        "req_header": json.dumps(req_header),
        "req_body": json.dumps(req_body)
    }
    url = "https://www.weiyun.com/webapp/json/weiyunSafeBox/SafeBoxCheckStatus?refer=chrome_windows&g_tk="+wyctoken+"&r="+str(random.random())
    # targeturl = "https://www.weiyun.com"
    # proxy_addr=ipPool.randomGetIp(targeturl)
    # proxies = {
    #   "http": "http://"+proxy_addr,
    #   "https": "http://"+proxy_addr,
    # }
    # result = requests.request('POST' , url, proxies = proxies, data=json.dumps(
    #     data), headers=headers, verify=False)
    result = proxyRquest_normal(url,data,headers)
    flag =True
    try :
        successBean = result.json()
        if successBean['data']:
            flag =True    
    except Exception as err:
        print(err)
        flag=False
    return flag


'''[summary]
微云--创建文件夹
参数
pdir_key:上级目录
ppdir_key: 上上级目录
skey:登陆用户skey
dir_name:创建文件名称
返回
当前目录dir_key,和父目录pdir_key
[description]
'''


def wy_diskDirCreate(pdir_key, ppdir_key, dir_name):
    global skey
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/json;charset=UTF-8",
        "cookie": "web_wx_rc=%s; pgv_pvi=%s; pgv_si=%s; ptisp=%s; ptui_loginuin=%s; pt2gguin=%s; uin=%s; skey=%s; ptcz=%s; p_uin=%s; pt4_token=%s; p_skey=%s; wyctoken=%s" % (web_wx_rc, pgv_pvi, pgv_si, ptisp, ptui_loginuin, pt2gguin, uin, skey, ptcz, p_uin, pt4_token, p_skey, wyctoken),
        "origin": "https://www.weiyun.com",
        "referer": "https://www.weiyun.com/disk",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
    }
    req_header = {
        "seq": int(str(int(time.time()))+'6484240'),
        "type": 1,
        "cmd": 2614,
        "appid": 30013,
        "version": 3,
        "major_version": 3,
        "minor_version": 3,
        "fix_version": 3,
        "wx_openid": "",
        "user_flag": 0
    }
    req_body = {
        "ReqMsg_body": {
            "ext_req_head": {
                "token_info": {
                    "token_type": 0,
                    "login_key_type": 1,
                    "login_key_value": skey
                }
            },
            ".weiyun.DiskDirCreateMsgReq_body": {
                "pdir_key": pdir_key,
                "ppdir_key": ppdir_key,
                "dir_name": dir_name,
                "file_exist_option": 2,
                "create_type": 1
            }
        }
    }
    data = {
        "req_header": json.dumps(req_header),
        "req_body": json.dumps(req_body)
    }
    url = "https://www.weiyun.com/webapp/json/weiyunQdiskClient/DiskDirCreate?refer=chrome_windows&g_tk="+wyctoken+"&r="+str(random.random())
    # targeturl = "https://www.weiyun.com"
    # proxy_addr=ipPool.randomGetIp(targeturl)
    # proxies = {
    #   "http": "http://"+proxy_addr,
    #   "https": "http://"+proxy_addr,
    # }
    # result = requests.request('POST', url, proxies = proxies, data=json.dumps(
    #     data), headers=headers, verify=False)
    result = proxyRquest_normal(url,data,headers)
    successBean = result.json()
    pdir_key = ""
    dir_key = ""
    if successBean["data"]["rsp_header"]["retcode"] == 0:
        dir_key = successBean["data"]["rsp_body"]["RspMsg_body"]["dir_key"]
        pdir_key = successBean["data"]["rsp_body"]["RspMsg_body"]["pdir_key"]
        return dir_key, pdir_key
    else:
        return dir_key, pdir_key

'''[summary]
微云--小文件文件上传
参数
pdir_key:上级目录
ppdir_key: 上上级目录
skey:登陆用户skey
localFilePath:本地文件地址
返回
上传的文件ID: file_id
文件名称:filename
[description]
'''


def wy_fileUpload(pdir_key, ppdir_key, localFilePath):
    fsize = os.path.getsize(localFilePath)
    filename = os.path.basename(localFilePath)
    file_id, filename="",""
    if fsize>512*1024:
        file_id, filename=wy_fileUpload_big(pdir_key,ppdir_key,localFilePath)
    else:
        file_id, filename=wy_fileUpload_small(pdir_key,ppdir_key,localFilePath)
    return file_id, filename
'''[summary]
微云--小文件文件上传
参数
pdir_key:上级目录
ppdir_key: 上上级目录
skey:登陆用户skey
localFilePath:本地文件地址
返回
上传的文件ID: file_id
文件名称:filename
[description]
'''


def wy_fileUpload_small(pdir_key, ppdir_key, localFilePath):
    global skey
    fsize = os.path.getsize(localFilePath)
    filename = os.path.basename(localFilePath)
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": "web_wx_rc=%s; pgv_pvi=%s; pgv_si=%s; ptisp=%s; ptui_loginuin=%s; pt2gguin=%s; uin=%s; skey=%s; ptcz=%s; p_uin=%s; pt4_token=%s; p_skey=%s; wyctoken=%s" % (web_wx_rc, pgv_pvi, pgv_si, ptisp, ptui_loginuin, pt2gguin, uin, skey, ptcz, p_uin, pt4_token, p_skey, wyctoken),
        "origin": "https://www.weiyun.com",
        "referer": "https://www.weiyun.com/disk/folder/"+pdir_key,
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
    }
    data = {
        "req_header": {
            "cmd": 247120,
            "appid": 30013,
            "major_version": 3,
            "minor_version": 0,
            "fix_version": 0,
            "version": 0
        },
        "req_body": {
            "ReqMsg_body": {
                "weiyun.PreUploadMsgReq_body": {
                    "common_upload_req": {
                        "ppdir_key": ppdir_key,
                        "pdir_key": pdir_key,
                        "file_size": fsize,
                        "filename": filename,
                        "file_exist_option": 6,
                        "use_mutil_channel": True,
                        "ext_info": {
                            "take_time": int(time.time())
                        }
                    },
                    "upload_scr": 0,
                    "channel_count": 4
                }
            }
        }
    }  
    url = "https://upload.weiyun.com/ftnup_v2/weiyun?cmd=247120"
    files = {
        "upload": open(localFilePath, "rb")
    }
    jsonData = {
        "json": json.dumps(data)
    }
    result = requests.request('POST', url, data=jsonData,
                              files=files, headers=headers, verify=False)
    # result = proxyRquest_file(url,jsonData,files,headers)
    successBean = result.json()
    # print(successBean)
    file_id = ""
    filename = ""
    if successBean["rsp_header"]["retcode"] == 0:
        file_id = successBean["rsp_body"]["RspMsg_body"]["weiyun.PreUploadMsgRsp_body"]["common_upload_rsp"]["file_id"]
        filename = successBean["rsp_body"]["RspMsg_body"]["weiyun.PreUploadMsgRsp_body"]["common_upload_rsp"]["filename"]
        return file_id, filename
    else:
        return file_id, filename

'''[summary]
微云--分片上传切片到微云
参数
localFilePath:本地文件地址
block_info_list:切边信息
upload_key:微云返回信息
id:微云返回信息
ex:微云返回信息
返回
上传的文件ID: file_id
文件名称:filename
[description]
'''
def readFileBlob(localFilePath,block_info_list,upload_key,channel,ex,pdir_key):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": "web_wx_rc=%s; pgv_pvi=%s; pgv_si=%s; ptisp=%s; ptui_loginuin=%s; pt2gguin=%s; uin=%s; skey=%s; ptcz=%s; p_uin=%s; pt4_token=%s; p_skey=%s; wyctoken=%s" % (web_wx_rc, pgv_pvi, pgv_si, ptisp, ptui_loginuin, pt2gguin, uin, skey, ptcz, p_uin, pt4_token, p_skey, wyctoken),
        "origin": "https://www.weiyun.com",
        "referer": "https://www.weiyun.com/disk/folder/"+pdir_key,
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
    }
    flie=open(localFilePath, "rb")
    for block in block_info_list :
        flie.seek(block['offset'])
        blob=flie.read(block['size'])
        data = {
            "req_header": {
                "cmd": 247121,
                "appid": 30013,
                "major_version": 3,
                "minor_version": 0,
                "fix_version": 0,
                "version": 0
            },
            "req_body": {
                "ReqMsg_body": {
                    "weiyun.UploadPieceMsgReq_body": {
                        "upload_key": upload_key,
                        "channel": {
                            "id": channel['id'],
                            "offset": block['offset'],
                            "len": block['size']
                        },
                        "ex": ex
                    }
                }
            }
        }
        files = {
            "upload": blob
        }
        jsonData = {
            "json": json.dumps(data)
        }
        url = "https://upload.weiyun.com/ftnup_v2/weiyun?cmd=247121"
        result = requests.request('POST', url,data=jsonData, files=files, headers=headers, verify=False)
        # result = proxyRquest_file(url,jsonData,files,headers)
        successBean = result.json()
    flie.close()
'''[summary]
微云--大文件上传 文件大于>1M
参数
pdir_key:上级目录
ppdir_key: 上上级目录
skey:登陆用户skey
localFilePath:本地文件地址
返回
上传的文件ID: file_id
文件名称:filename
[description]
'''
def wy_fileUpload_big(pdir_key, ppdir_key, localFilePath):
    global skey
    fsize = os.path.getsize(localFilePath)
    filename = os.path.basename(localFilePath)
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": "web_wx_rc=%s; pgv_pvi=%s; pgv_si=%s; ptisp=%s; ptui_loginuin=%s; pt2gguin=%s; uin=%s; skey=%s; ptcz=%s; p_uin=%s; pt4_token=%s; p_skey=%s; wyctoken=%s" % (web_wx_rc, pgv_pvi, pgv_si, ptisp, ptui_loginuin, pt2gguin, uin, skey, ptcz, p_uin, pt4_token, p_skey, wyctoken),
        "origin": "https://www.weiyun.com",
        "referer": "https://www.weiyun.com/disk/folder/"+pdir_key,
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
    }
    data = {
        "req_header": {
            "cmd": 247120,
            "appid": 30013,
            "major_version": 3,
            "minor_version": 0,
            "fix_version": 0,
            "version": 0
        },
        "req_body": {
            "ReqMsg_body": {
                "weiyun.PreUploadMsgReq_body": {
                    "common_upload_req": {
                        "ppdir_key": ppdir_key,
                        "pdir_key": pdir_key,
                        "file_size": fsize,
                        "filename": filename,
                        "file_exist_option": 6,
                        "use_mutil_channel": True,
                        "ext_info": {
                            "take_time": int(time.time())
                        }
                    },
                    "upload_scr": 0,
                    "channel_count": 4,
                    # "check_sha": aimData['check_sha'],
                    # "check_data": aimData['check_data'],
                    # "block_info_list": aimData['block_info_list']
                }
            }
        }
    }
    driver=initChromeDriver()
    workfolder = os.getcwd()
    tempUrl=workfolder+"/shaUtil.html";
    driver.get("file:///"+tempUrl)
    file=driver.find_element_by_id("file")
    file.send_keys(localFilePath)
    resultStr=""
    while resultStr=="":
        resultStr=driver.find_element_by_id("result").get_attribute("value")
        if resultStr!="":
            break
    aimData=json.loads(resultStr)
    driver.quit()
    data['req_body']['ReqMsg_body']['weiyun.PreUploadMsgReq_body']['check_sha']=aimData['check_sha']
    data['req_body']['ReqMsg_body']['weiyun.PreUploadMsgReq_body']['check_data']=aimData['check_data']
    data['req_body']['ReqMsg_body']['weiyun.PreUploadMsgReq_body']['block_info_list']=aimData['block_info_list']    
    url = "https://upload.weiyun.com/ftnup_v2/weiyun?cmd=247120"
    jsonData = {
        "json": json.dumps(data)
    }
    result = requests.request('POST', url, files=jsonData, headers=headers, verify=False)
    # result = proxyRquest_file(url,None,jsonData,headers)
    successBean = result.json()
    file_exist=successBean["rsp_body"]["RspMsg_body"]["weiyun.PreUploadMsgRsp_body"]['file_exist']
    if(file_exist!=True) :
        upload_key=successBean["rsp_body"]["RspMsg_body"]["weiyun.PreUploadMsgRsp_body"]['upload_key']
        ex=successBean["rsp_body"]["RspMsg_body"]["weiyun.PreUploadMsgRsp_body"]['ex']
        channel_0=successBean["rsp_body"]["RspMsg_body"]["weiyun.PreUploadMsgRsp_body"]['channel_list'][0]
        print("upload_key:%s"%upload_key);
        print("ex:%s"%ex);
        print("channel_0:%s"%channel_0);
        readFileBlob(localFilePath,aimData['block_info_list'],upload_key,channel_0,ex,pdir_key)
    ##多线程上传切片
    file_id = ""
    filename = ""
    if successBean["rsp_header"]["retcode"] == 0:
        file_id = successBean["rsp_body"]["RspMsg_body"]["weiyun.PreUploadMsgRsp_body"]["common_upload_rsp"]["file_id"]
        filename = successBean["rsp_body"]["RspMsg_body"]["weiyun.PreUploadMsgRsp_body"]["common_upload_rsp"]["filename"]
        return file_id, filename
    else:
        return file_id, filename

'''[summary]
微云-文件删除
参数
pdir_key:上级目录
ppdir_key: 上上级目录
skey:登陆用户skey
file_id:微云文件ID
filename:文件名称
返回
[description]
'''


def wy_diskFileBatchDeleteEx(pdir_key, ppdir_key, file_id, filename):
    global skey
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "content-type": "application/json;charset=UTF-8",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": "web_wx_rc=%s; pgv_pvi=%s; pgv_si=%s; ptisp=%s; ptui_loginuin=%s; pt2gguin=%s; uin=%s; skey=%s; ptcz=%s; p_uin=%s; pt4_token=%s; p_skey=%s; wyctoken=%s" % (web_wx_rc, pgv_pvi, pgv_si, ptisp, ptui_loginuin, pt2gguin, uin, skey, ptcz, p_uin, pt4_token, p_skey, wyctoken),
        "origin": "https://www.weiyun.com",
        "referer": "https://www.weiyun.com/disk/folder/"+pdir_key,
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
    }
    req_header = {
        "seq": int(str(int(time.time()))+'6484240'),
        "type": 1,
        "cmd": 2509,
        "appid": 30013,
        "version": 3,
        "major_version": 3,
        "minor_version": 3,
        "fix_version": 3,
        "wx_openid": "",
        "user_flag": 0
    }
    req_body = {
        "ReqMsg_body": {
            "ext_req_head": {
                "token_info": {
                    "token_type": 0,
                    "login_key_type": 1,
                    "login_key_value": skey
                }
            },
            ".weiyun.DiskDirFileBatchDeleteExMsgReq_body": {
                "file_list": [
                    {
                        "ppdir_key": ppdir_key,
                        "pdir_key": pdir_key,
                        "file_id": file_id,
                        "filename": filename
                    }
                ]
            }
        }
    }
    data = {
        "req_header": json.dumps(req_header),
        "req_body": json.dumps(req_body)
    }
    url = "https://www.weiyun.com/webapp/json/weiyunQdiskClient/DiskDirFileBatchDeleteEx?refer=chrome_windows&g_tk="+wyctoken+"&r="+str(random.random())
    # targeturl = "https://www.weiyun.com"
    # proxy_addr=ipPool.randomGetIp(targeturl)
    # proxies = {
    #   "http": "http://"+proxy_addr,
    #   "https": "http://"+proxy_addr,
    # }
    # #,proxies = proxies
    # result = requests.request('POST', url,proxies = proxies, data=json.dumps(
    #     data), headers=headers, verify=False)
    result = proxyRquest_normal(url,data,headers)


'''[summary]
微云-文件夹删除
参数
pdir_key:上级目录
ppdir_key: 上上级目录
skey:登陆用户skey
dir_key:文件夹key
dir_name:文件夹名称
返回
[description]
'''


def wy_diskDirBatchDeleteEx(pdir_key, ppdir_key, dir_key, dir_name):
    global skey
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "content-type": "application/json;charset=UTF-8",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": "web_wx_rc=%s; pgv_pvi=%s; pgv_si=%s; ptisp=%s; ptui_loginuin=%s; pt2gguin=%s; uin=%s; skey=%s; ptcz=%s; p_uin=%s; pt4_token=%s; p_skey=%s; wyctoken=%s" % (web_wx_rc, pgv_pvi, pgv_si, ptisp, ptui_loginuin, pt2gguin, uin, skey, ptcz, p_uin, pt4_token, p_skey, wyctoken),
        "origin": "https://www.weiyun.com",
        "referer": "https://www.weiyun.com/disk",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
    }
    req_header = {
        "seq": int(str(int(time.time()))+'6484240'),
        "type": 1,
        "cmd": 2509,
        "appid": 30013,
        "version": 3,
        "major_version": 3,
        "minor_version": 3,
        "fix_version": 3,
        "wx_openid": "",
        "user_flag": 0
    }
    req_body = {
        "ReqMsg_body": {
            "ext_req_head": {
                "token_info": {
                    "token_type": 0,
                    "login_key_type": 1,
                    "login_key_value": skey
                }
            },
            ".weiyun.DiskDirFileBatchDeleteExMsgReq_body": {
                "dir_list": [
                    {
                        "ppdir_key": ppdir_key,
                        "pdir_key": pdir_key,
                        "dir_key": dir_key,
                        "dir_name": dir_name
                    }
                ]
            }
        }
    }
    data = {
        "req_header": json.dumps(req_header),
        "req_body": json.dumps(req_body)
    }
    url = "https://www.weiyun.com/webapp/json/weiyunQdiskClient/DiskDirFileBatchDeleteEx?refer=chrome_windows&g_tk="+wyctoken+"&r="+str(random.random())
    # targeturl = "https://www.weiyun.com"
    # proxy_addr=ipPool.randomGetIp(targeturl)
    # proxies = {
    #   "http": "http://"+proxy_addr,
    #   "https": "http://"+proxy_addr,
    # }
    # #,proxies = proxies
    # result = requests.request('POST', url,proxies = proxies, data=json.dumps(
    #     data), headers=headers, verify=False)
    result = proxyRquest_normal(url,data,headers)


'''[summary]
微云 - 获取腾讯微云分享地址
参数
pdir_key:上级目录
file_id: 文件ID
file_name:文件名称
[description]
'''


def wy_shareUrl(pdir_key, file_id, file_name):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "content-type": "application/json;charset=UTF-8",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": "web_wx_rc=%s; pgv_pvi=%s; pgv_si=%s; ptisp=%s; ptui_loginuin=%s; pt2gguin=%s; uin=%s; skey=%s; ptcz=%s; p_uin=%s; pt4_token=%s; p_skey=%s; wyctoken=%s" % (web_wx_rc, pgv_pvi, pgv_si, ptisp, ptui_loginuin, pt2gguin, uin, skey, ptcz, p_uin, pt4_token, p_skey, wyctoken),
        "origin": "https://www.weiyun.com",
        "referer": "https://www.weiyun.com/disk",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
    }
    req_header = {
        "seq": int(str(int(time.time()))+'6484240'),
        "type": 1,
        "cmd": 12100,
        "appid": 30013,
        "version": 3,
        "major_version": 3,
        "minor_version": 3,
        "fix_version": 3,
        "wx_openid": "",
        "user_flag": 0
    }
    req_body = {
        "ReqMsg_body": {
            "ext_req_head": {
                "token_info": {
                    "token_type": 0,
                    "login_key_type": 1,
                    "login_key_value": skey
                }
            },
            ".weiyun.WeiyunShareAddV2MsgReq_body":  {
                "note_list": [

                ],
                "dir_list": [

                ],
                "file_list": [
                    {
                        "pdir_key": pdir_key,
                        "file_id": file_id
                    }
                ],
                "share_type": 0,
                "share_name": file_name
            }
        }
    }
    data = {
        "req_header": json.dumps(req_header),
        "req_body": json.dumps(req_body)
    }
    url = "https://www.weiyun.com/webapp/json/weiyunShare/WeiyunShareAddV2?refer=chrome_windows&g_tk="+wyctoken+"&r="+str(random.random())
    # targeturl = "https://www.weiyun.com"
    # proxy_addr=ipPool.randomGetIp(targeturl)
    # proxies = {
    #   "http": "http://"+proxy_addr,
    #   "https": "http://"+proxy_addr,
    # }
    # #,proxies = proxies
    # result = requests.request('POST', url,proxies = proxies, data=json.dumps(
    #     data), headers=headers, verify=False)
    result = proxyRquest_normal(url,data,headers)
    successBean = result.json()
    if successBean["data"]["rsp_header"]["retcode"] == 0:
        short_url = successBean["data"]["rsp_body"]["RspMsg_body"]["short_url"]
        return short_url
    else:
        return ""

'''[summary]
微云 - 获取腾讯微云下载地址
参数
pdir_key:上级目录
file_id: 文件ID
file_name:文件名称
[description]
'''


def wy_downloadUrl(file_list):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "content-type": "application/json;charset=UTF-8",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": "web_wx_rc=%s; pgv_pvi=%s; pgv_si=%s; ptisp=%s; ptui_loginuin=%s; pt2gguin=%s; uin=%s; skey=%s; ptcz=%s; p_uin=%s; pt4_token=%s; p_skey=%s; wyctoken=%s" % (web_wx_rc, pgv_pvi, pgv_si, ptisp, ptui_loginuin, pt2gguin, uin, skey, ptcz, p_uin, pt4_token, p_skey, wyctoken),
        "origin": "https://www.weiyun.com",
        "referer": "https://www.weiyun.com/disk",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
    }
    req_header = {
        "seq": int(str(int(time.time()))+'6484240'),
        "type": 1,
        "cmd": 2402,
        "appid": 30013,
        "version": 3,
        "major_version": 3,
        "minor_version": 3,
        "fix_version": 3,
        "wx_openid": "",
        "user_flag": 0
    }
    req_body = {
        "ReqMsg_body": {
            "ext_req_head": {
                "token_info": {
                    "token_type": 0,
                    "login_key_type": 1,
                    "login_key_value": skey
                }
            },
            ".weiyun.DiskFileBatchDownloadMsgReq_body":  {
                "file_list": file_list,
                "download_type": 16
            }
        }
    }
    data = {
        "req_header": json.dumps(req_header),
        "req_body": json.dumps(req_body)
    }
    url = "https://www.weiyun.com/webapp/json/weiyunQdiskClient/DiskFileBatchDownload?refer=chrome_windows&g_tk="+wyctoken+"&r="+str(random.random())
    # targeturl = "https://www.weiyun.com"
    # proxy_addr=ipPool.randomGetIp(targeturl)
    # proxies = {
    #   "http": "http://"+proxy_addr,
    #   "https": "http://"+proxy_addr,
    # }
    # #,proxies = proxies
    # result = requests.request('POST', url,proxies = proxies, data=json.dumps(
    #     data), headers=headers, verify=False)
    result = proxyRquest_normal(url,data,headers)
    successBean = result.json()
    if successBean["data"]["rsp_header"]["retcode"] == 0:
        download_url = []
        filelist=successBean["data"]["rsp_body"]["RspMsg_body"]["file_list"]
        for file in filelist :
            download_url.append(file["download_url"])
        return download_url
    else:
        return ""


'''[summary]
微云-获取文件服务器地址
[description]
'''
driver2=""
def initWebDriver():
    global driver2
    driver2 = initChromeDriver()

'''[summary]
退出webDriver浏览器
[description]
'''
def quitWebDriver():
     global driver2
     driver2.quit()

def wy_filePath(share_url, type):
    try:
        global driver2
        driver2.get(share_url)
        flag = True
        if type == 'img':
            # while flag:
            #     try:
            media_img = driver2.find_element_by_class_name("media-img")
            img_url = media_img.find_element_by_tag_name("img")
            aim_url = img_url.get_property("src")
            return aim_url
        elif type == 'video':
            while flag:
                try:
                    vjs_video_3_html5_api = driver2.find_element_by_id(
                        "vjs_video_3_html5_api")
                    flag = False
                except:
                    flag = True
                finally:
                    time.sleep(0.1)
            aim_url = vjs_video_3_html5_api.get_property("src")
            return aim_url
        else:
            return ""
    except Exception as err :
        print("地址转化失败:",share_url)
        print(err)
        quitWebDriver()

if __name__ == '__main__':
    try:
        #创建文件夹
        init()
        rootDirKey, mainDirKey = getRootAndMainDirKey()
        print("rootDirKey:%s,mainDirKey:%s"%(rootDirKey, mainDirKey))
        dir_key,pdir_key=wy_diskDirCreate(mainDirKey,rootDirKey,"A_文件夹")
        print("创建文件夹dir_key:%s,pdir_key:%s"%(dir_key,pdir_key))
        #上传本地文件
        localFilePath="C:\\Users\\Administrator\\Desktop\\tt\\1.jpg"
        file_id,filename=wy_fileUpload(dir_key,pdir_key,localFilePath)
        # # 删除微云文件
        # wy_diskFileBatchDeleteEx(dir_key,pdir_key,'fc85ad18-f96f-42c6-8eab-81f36fb16864','1.mp4')
        # # 删除微云文件夹
        # wy_diskDirBatchDeleteEx(mainDirKey,rootDirKey,'a909c646d29d98e531174278ac14597e','A_测试')
        # file_list=[
        #     {
        #         "pdir_key": "a909c646985f636b296e5d07ca7c749c",
        #         "file_id": "5851dbcf-7dea-4ef5-9a45-dca73090767f"
        #     },
        #     {
        #         "pdir_key": "a909c646985f636b296e5d07ca7c749c",
        #         "file_id": "5851dbcf-7dea-4ef5-9a45-dca73090767f"
        #     }
        # ]
        # download_url=wy_downloadUrl(file_list)
        # print("下载地址:",download_url)
        # share_url=wy_shareUrl(dir_key,
        #             file_id, filename)
        # print("分享地址:",share_url)
        # aim_url=wy_filePath(share_url,"video")
        # print(aim_url)
        # initWebDriver()
        # img_url=wy_filePath(share_url,"img")
        # print(img_url)
    except Exception as err:
        print(err)
    finally:
        print("关闭浏览器")
        # driver.quit()
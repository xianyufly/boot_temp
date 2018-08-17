#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image, ImageEnhance, ImageDraw , ImageFont
import time,sys
#模拟浏览器框架
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# 导入支持双击操作的模块
from selenium.webdriver import ActionChains
sys.path.append("..")
import env
#系统变量
_env=env.initEnv()
driver=None

def initDriver():
	global driver
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--no-sandbox")
	chrome_options.add_argument('lang=zh_CN.utf-8')
	# 对应的chromedriver的放置目录
	driver = webdriver.Chrome(executable_path=(
	    _env["chrome_driver_path"]), chrome_options=chrome_options)

def quitDriver():
	global driver
	if driver :
		driver.quit()

def cut(path,pagePath):
    global driver
    driver.get(pagePath)
    time.sleep(1)
    driver.get_screenshot_as_file(path+"/screen.png")
    #裁剪掉滚动条
    img = Image.open(path+"/screen.png")
    crop_size = (0,0,img.size[0]-17,img.size[1])
    cropped = img.crop(crop_size)
    cropped.save(path+"/screen.png")
    text1 = "17sobt.com"
    text2 = "一起搜模板"
    im = Image.open(path+"/screen.png")
    mark1 = text2img(text1,font_color="#E75000",font_type='Enjoy The Show.ttf',font_size=20)
    mark2 = text2img(text2,font_color="#E95200",font_size=20)
    image = watermark(im, mark1, 'right_top', 0.9)
    image = watermark(image, mark2, 'right_top_30', 0.9)
    if image:
        image.save(path+"/screen.png")
        # image.show()
    else:
        print("Sorry, Failed.")

def text2img(text, font_color="#EF4F03",font_type="nzjt.TTF", font_size=20):
    """生成内容为 TEXT 的水印"""
 
    font = ImageFont.truetype(font_type, font_size)
    #多行文字处理
    text = text.split('\n')
    mark_width = 0
    for  i in range(len(text)):
        (width, height) = font.getsize(text[i])
        if mark_width < width:
            mark_width = width
    mark_height = height * len(text)
 
    #生成水印图片
    mark = Image.new('RGBA', (mark_width,mark_height))
    draw = ImageDraw.ImageDraw(mark, "RGBA")
    # draw.setfont(font)
    for i in range(len(text)):
        (width, height) = font.getsize(text[i])
        draw.text((0, i*height), text[i],font = font, fill=font_color)
    return mark
 
def set_opacity(im, opacity):
    """设置透明度"""
 
    assert opacity >=0 and opacity < 1
    if im.mode != "RGBA":
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im
 
def watermark(im, mark, position, opacity=1):
    """添加水印"""
 
    try:
        if opacity < 1:
            mark = set_opacity(mark, opacity)
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        if im.size[0] < mark.size[0] or im.size[1] < mark.size[1]:
            print("The mark image size is larger size than original image file.")
            return False
 
        #设置水印位置
        if position == 'left_top':
            x = 0
            y = 0
        elif position == 'left_bottom':
            x = 0
            y = im.size[1] - mark.size[1]
        elif position == 'right_top':
            x = im.size[0] - mark.size[0] - 40
            y = 0
        elif position == 'right_top_30':
            x = im.size[0] - mark.size[0] - 40
            y = 20
        elif position == 'right_bottom':
            x = im.size[0] - mark.size[0] + 5
            y = im.size[1] - mark.size[1] + 10
        else:
            x = (im.size[0] - mark.size[0]) / 2
            y = (im.size[1] - mark.size[1]) / 2
 
        layer = Image.new('RGBA', im.size,)
        layer.paste(mark,(x,y))
        return Image.composite(layer, im, layer)
    except Exception as e:
        print(">>>>>>>>>>> WaterMark EXCEPTION:  " + str(e))
        return False

def main():
    text1 = "17sobt.com"
    text2 = "17搜模板"
    
    im = Image.open('C:\\Users\\Administrator\\Desktop\\webapplayers\\screen.png')
    mark1 = text2img(text1,font_color="#E75000",font_type='Enjoy The Show.ttf',font_size=20)
    mark2 = text2img(text2,font_color="#E95200",font_size=20)
    
    image = watermark(im, mark1, 'right_top', 0.9)
    image = watermark(image, mark2, 'right_top_30', 0.9)
    
    if image:
        image.save('C:\\Users\\Administrator\\Desktop\\webapplayers\\screen2.png')
        image.show()
    else:
        print("Sorry, Failed.")

def dealwith(pagePath,cutImageSavePath):
	initDriver()
	cut(cutImageSavePath,pagePath)
	quitDriver()

if __name__ == '__main__':
	initDriver()
	path="C:\\Users\\Administrator\\Desktop\\work\\template\\material-pro-blue"
	pagePath="C:\\Users\\Administrator\\Desktop\\work\\template\\material-pro-blue\\index.html"
	cut(path,pagePath)
	quitDriver()
# if __name__ == '__main__':
#     main()

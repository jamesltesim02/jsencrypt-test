#!/usr/bin/python
#coding: utf-8

import timeit,random,time,os
from PIL import Image,ImageDraw
from PIL import  ImageEnhance 
from PIL import  ImageFilter
import urllib2, json, base64
import hashlib


Get_path = "./img_data/"    #下载图片保存路径
Get_url = "http://cms.pokermanager.club/cms-api/captcha?token=%s"
Get_number = 50            #下载图片数量
Cutting = './Cutting/'      #临时保存
Iconset = './tmp/'      #数据存储
ico = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k','l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def request(url):
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	content = response.read()
	return json.loads(content)

class IMG(object):
  
    def GetImgCode(self):
        get_img_start = time.time()
        if os.path.isdir(Get_path):
            pass
        else:
            mkdir = os.makedirs(Get_path)
        if Get_url !='':
	        for i in range(0,Get_number):
	            filePath = Get_path+str(i)+'.jpeg'
	            rel = request('http://cms.pokermanager.club/cms-api/token/generateCaptchaToken')
	            if rel['iErrCode'] == 0:
	            	url = Get_url %(rel['result'])
	            	rel = request(url)
	            	if rel['iErrCode'] == 0:
	            		with open(filePath,'w+') as f:
							f.write(base64.b64decode(rel['result']))
	            
        else:
        	print('验证码下载地址为空')
        	exit()	 


    def HandleVerify(self): 

        imgs = os.listdir(Get_path)
        for file in imgs:
        	if not file.startswith('.') or file.startswith('..'):
        		im = Image.open(os.path.join(Get_path, file))
        		im = self.CleanLine(im)
        		im = self.clearNoise(im)
        		self.ImgCutting(im)

    def CleanLine(self,im):
		for x in range(im.size[1]):
			for y in range(im.size[0]):
				pix = im.getpixel((y,x))
				if pix[0] <=50 and pix[1] <=50 and  pix[2] <=50:
					im.putpixel((y,x), (255, 255, 255))

		im = im.convert("P")
		im2 = Image.new("P",im.size,255)
		for x in range(im.size[1]):
			for y in range(im.size[0]):
				pix = im.getpixel((y,x))
				if pix in [190, 154, 82, 118, 191, 197, 46]: # these are the numbers to get
					im2.putpixel((y,x),0)
		return im2
        

    def ImgCutting(self,img):
		inletter = False
		foundletter=False
		start = 0
		end = 0

		letters = []
		for y in range(img.size[0]): 
		    for x in range(img.size[1]):
		        pix = img.getpixel((y,x))
		        if pix != 255:
		            inletter = True
		    if foundletter == False and inletter == True:
		        foundletter = True
		        start = y

		    if foundletter == True and inletter == False:
		        foundletter = False
		        end = y
		        letters.append((start,end))

		    inletter=False


		count = 0
		for letter in letters:
		    m = hashlib.md5()
		    im3 = img.crop(( letter[0] , 0, letter[1],img.size[1] ))
		    m.update("%s%s"%(time.time(),count))
		    im3.save("./Cutting/%s.png"%(m.hexdigest()))
		    count += 1

    def clearNoise(self,img):  
		pixdata = img.load()
		w,h = img.size
		for y in range(1,h-1):
			for x in range(1,w-1):
				count = 0
				if pixdata[x,y-1] > 245:
					count = count + 1
				if pixdata[x,y+1] > 245:
					count = count + 1
				if pixdata[x-1,y] > 245:
					count = count + 1
				if pixdata[x+1,y] > 245:
					count = count + 1
				if count > 3:
					pixdata[x,y] = 255
		return img

    def Class_dir(self):
        for j in range(len(ico)):
            file_name = Iconset+str(ico[j])
            os.mkdir(file_name)

if __name__ == '__main__':
    Img = IMG()
    Img.GetImgCode()
    # Img.HandleVerify()
    # Img.Class_dir()
    
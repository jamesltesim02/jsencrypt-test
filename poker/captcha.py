#-*- coding:utf8 -*-
from PIL import Image
import math
import time
import os
import hashlib
import base64
from io import BytesIO

class VectorCompare:
  #计算矢量大小
  def magnitude(self,concordance):
    total = 0
    for word,count in concordance.iteritems():
      total += count ** 2
    return math.sqrt(total)

  #计算矢量之间的 cos 值
  def relation(self,concordance1, concordance2):
    relevance = 0
    topvalue = 0
    for word, count in concordance1.iteritems():
      if concordance2.has_key(word):
        topvalue += count * concordance2[word]
    return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))

def depoint(img):   #input: gray image
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

def buildvector(im):
  d1 = {}
  count = 0
  for i in im.getdata():
    d1[count] = i
    count += 1
  return d1

def crack(src):
  byte_data = base64.b64decode(src)
  image_data = BytesIO(byte_data)
  im = Image.open(image_data)
  for x in range(im.size[1]):
    for y in range(im.size[0]):
      pix = im.getpixel((y,x))
      if pix[0] <=50 and pix[1] <=50 and  pix[2] <=50:
        im.putpixel((y,x), (255, 255, 255))

  #(将图片转换为8位像素模式)
  im = im.convert("P")
  im2 = Image.new("P",im.size,255)
  his = im.histogram()
  values = {}

  for x in range(im.size[1]):
    for y in range(im.size[0]):
      pix = im.getpixel((y,x))
      if pix in [190, 154, 82, 118, 191, 197, 46]: # these are the numbers to get
        im2.putpixel((y,x),0)
  
  im2 = depoint(im2)

  inletter = False
  foundletter=False
  start = 0
  end = 0

  letters = []

  for y in range(im2.size[0]): 
    for x in range(im2.size[1]):
      pix = im2.getpixel((y,x))
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
  v = VectorCompare()

  iconset = ['0','1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

  #加载训练集
  imageset = []
  for letter in iconset:
    for img in os.listdir(os.path.dirname(os.path.realpath(__file__)) + '/Cutting/%s/'%(letter)):
      temp = []
      if img != "Thumbs.db" and img != ".DS_Store":
        temp.append(buildvector(Image.open(os.path.dirname(os.path.realpath(__file__)) + '/Cutting/%s/%s'%(letter,img))))
      imageset.append({letter:temp})


  count = 0
  #对验证码图片进行切割
  validName = ''
  for letter in letters:
    m = hashlib.md5()
    im3 = im2.crop(( letter[0] , 0, letter[1],im2.size[1] ))

    guess = []

    #将切割得到的验证码小片段与每个训练片段进行比较
    for image in imageset:
      for x,y in image.iteritems():
        if len(y) != 0:
          guess.append( ( v.relation(y[0],buildvector(im3)),x) )

    guess.sort(reverse=True)
    validName += guess[0][1]
  return validName

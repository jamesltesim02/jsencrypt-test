#! /usr/bin/env python
# coding=utf-8

import requests
import os, base64
import uuid

base_url = "http://cms.pokermanager.club/cms-api/"

def downloadImages():
  token = requests.post(base_url + "token/generateCaptchaToken").json()["result"]

  for i in range(1, 100):
    captcha = requests.post(
        base_url + "captcha",
        data = {"token": token},
        headers = {
          "Referer": "ttp://cms.pokermanager.club/cms-web/cmsLogin.html",
          "Origin": "http://cms.pokermanager.club",
          "Cookie": "aliyungf_tc=AQAAABkgK1BrQwoA2bAydGNyyaRWl6+i; userLanguage=zh",
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"
        }
      ).json()["result"]
    
    imgdata = base64.b64decode(captcha)
    imgfile = open("captchares/" + str(uuid.uuid1()) + ".jpg", "wb")
    imgfile.write(imgdata)
    imgfile.close()

def getCaptcha():
  token_result = requests.post(base_url + "token/generateCaptchaToken")
  token = token_result.json()["result"]
  cookie = token_result.cookies.get_dict()
  
  captcha_result = requests.post(
      base_url + "captcha",
      data = {"token": token},
      headers = {
        "Referer": "ttp://cms.pokermanager.club/cms-web/cmsLogin.html",
        "Origin": "http://cms.pokermanager.club",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"
      },
      cookies = cookie
    )

  captcha = captcha_result.json()["result"]
  
  return token, captcha, cookie

if __name__ == '__main__':
  token, captcha, cookie = getCaptcha()
  imgdata = base64.b64decode(captcha)
  imgfile = open("temp/captcha.jpg", "wb")
  imgfile.write(imgdata)
  imgfile.close()
  print(token)
  print(cookie)
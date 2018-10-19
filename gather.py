import requests
import json
import os, base64
import uuid

base_url = "http://cms.pokermanager.club/cms-api/"

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

# print(token)
# print(captcha)
#! /usr/bin/env python
# coding=utf-8

import requests
from cryptor import rsacrypt
import json

base_url = "http://cms.pokermanager.club/cms-api/"
token = '305c300d06092a864886f70d0101010500034b003048024100ac6b5b3631b62d43807c7e6ffaf5fc3c661ec13e2bf5926986013de0fbf06b913f5fac864a60ba4b017b792e1e9e9bb3555ea1eab85810d0cd0920d20623e3a30203010001'
reqData = rsacrypt.info_crypt(token, '18206774149', 'aa8888')

result = requests.post(
    base_url + "login",
    data = {
      "token": token,
      "data": reqData,
      "safeCode": "xp37",
      "locale": "zh"
    },
    headers = {
      "Referer": "http://cms.pokermanager.club/cms-web/cmsLogin.html",
      "Origin": "http://cms.pokermanager.club",
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36",
    },
    cookies = {'aliyungf_tc': 'AQAAAIM/OEWLkQEA2bAydBqRRmhRE3XR'}
  ).json()

print(result)

# api http://cms.pokermanager.club/cms-api/login
# origin http://cms.pokermanager.club
# referer http://cms.pokermanager.club/cms-web/cmsLogin.html
# useragent Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36
# Cookie aliyungf_tc=AQAAABkgK1BrQwoA2bAydGNyyaRWl6+i; userLanguage=zh
# accept application/json, text/javascript, */*; q=0.01
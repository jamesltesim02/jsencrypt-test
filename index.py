#! /usr/bin/env python
# coding=utf-8

from cryptor import rsacrypt

token = '305c300d06092a864886f70d0101010500034b003048024100d812a482263f7f6fe89756af3e50cd3ee12b66c5977f996994df948e05a69aebf422ca1bb8567231531dd574ead8a959ac6f8067718effcb01591e5649e99fb70203010001'
username = '18206774149'
password = 'aa8888'

result = rsacrypt.info_crypt(username, password, token)

print(result)

# api http://cms.pokermanager.club/cms-api/login
# origin http://cms.pokermanager.club
# referer http://cms.pokermanager.club/cms-web/cmsLogin.html
# useragent Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36
# Cookie aliyungf_tc=AQAAABkgK1BrQwoA2bAydGNyyaRWl6+i; userLanguage=zh
# accept application/json, text/javascript, */*; q=0.01
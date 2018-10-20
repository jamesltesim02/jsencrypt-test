#! /usr/bin/env python
# coding=utf-8

import requests
from cryptor import rsacrypt
from poker import captcha as capcracker
import json
import os

domain = 'http://cms.pokermanager.club'
base_url = domain + '/cms-api/'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
headers = {
    'Referer': domain + '/cms-web/cmsLogin.html',
    'Origin': domain,
    'User-Agent': user_agent
  }
tempfile_path = os.path.dirname(os.path.realpath(__file__)) + '/temp/tokenandcookie.text'

def getCaptcha():
  # 获取token
  token_result = requests.post(base_url + 'token/generateCaptchaToken')
  token = token_result.json()['result']
  # 获取cookie
  cookie = token_result.cookies.get_dict()
  
  # 请求验证码
  captcha_result = requests.post(
      base_url + 'captcha',
      data = {
        'token': token
      },
      headers = headers,
      cookies = cookie
    )
  captcha = captcha_result.json()['result']
  
  return token, captcha, cookie

def login():
  username, password = '18206774149', 'aa8888'

  # 获取验证码
  token, captcha, cookie = getCaptcha()
  # 识别验证码
  safeCode = capcracker.crack(captcha)
  # 加密账号密码
  reqData = rsacrypt.info_crypt(token, '18206774149', 'aa8888')

  # 请求参数
  data = {
      'token': token,
      'data': reqData,
      'safeCode': safeCode,
      'locale': 'zh'
    }

  # 请求登录
  result = requests.post(
      base_url + 'login',
      # 'http://10.96.52.35:3000/common/captcha',
      data = data,
      headers = headers,
      cookies = cookie
    ).json()

  if result['iErrCode'] == 0:
    tempfile = open(tempfile_path, 'w+')
    tempfile.write(json.dumps({
      'token': result['result'],
      'cookie': cookie
    }))
    tempfile.close()
    set_julebu()
    return
  
  if result['iErrCode'] == 1103:
    login()
    return

  raise Exception(json.dumps(result))

def execute_api(api, params={}):
  if os.path.exists(tempfile_path) == False:
    login()

  tempfile = open(tempfile_path, 'r')
  tcinfo = json.loads(tempfile.read())
  
  result = requests.post(
      base_url + api,
      data = params,
      headers = {
        'Referer': domain + '/cms-web/cmsLogin.html',
        'Origin': domain,
        'User-Agent': user_agent,
        'token': tcinfo['token']
      },
      cookies = tcinfo['cookie']
    ).json()

  if result['iErrCode'] == 1000:
    login()
    return execute_api(api, params)

  return result

def set_julebu():
  julebu_list = execute_api('club/getClubList')
  julebu_id = julebu_list['result'][0]['lClubID']
  execute_api('club/clubInfo', params={'clubId': julebu_id})

def getBuyinList():
  return execute_api('game/getBuyinList')

if __name__ == '__main__':
  #user_token = login()
  #print(user_token)
  result = getBuyinList()
  print(result)
  # login()
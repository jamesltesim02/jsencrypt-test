#! /usr/bin/env python
# coding=utf-8

import execjs
import os

def info_crypt(token, username, password):
  encryptjs = open(os.path.dirname(os.path.realpath(__file__)) + '/all.min.js', 'r').read()
  customFun = """
      ;function getPublicKey(key) {
        var encrypt = new window.JSEncrypt();
        encrypt.setPublicKey(key);
        return encrypt.getPublicKey();
      }
      ;function getEncrypt(key, username, password) {
        var encrypt = new JSEncrypt();
        encrypt.setPublicKey(key);
        return encrypt.encrypt(username + ',' + hex_md5(password));
      }
    """
  jsEnv = encryptjs + customFun
  ctx = execjs.compile(jsEnv)

  result = ctx.call("getEncrypt", token, username, password)
  return result 

from hashlib import md5
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64
import execjs
import os

def info_crypt(username, password, token):
  encryptjs = open(os.path.dirname(os.path.realpath(__file__)) + '/jsencrypt.js', 'r').read()
  customFun = """
      ;function getPublicKey(key) {
        var encrypt = new window.JSEncrypt();
        encrypt.setPublicKey(key);
        return encrypt.getPublicKey();
      }
    """
  jsEnv = encryptjs + customFun
  ctx = execjs.compile(jsEnv)

  md5pass = md5(password.encode('utf-8')).hexdigest().upper()
  inputText = username + ',' + md5pass
  publickey = ctx.call("getPublicKey", token)

  rsakey = RSA.import_key(publickey)
  cipher = Cipher_pkcs1_v1_5.new(rsakey)

  return base64.b64encode(cipher.encrypt(inputText))

import base64
import hashlib
import random
import struct
import time
from Crypto.Cipher import AES


BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]

class prpcrypt():
    def __init__(self,app_id,key):
        self.mode = AES.MODE_ECB
        self.app_id = app_id
        self.key = key
        self.iv = ""

    def encrypt(self, data, key):
        cyptor = AES.new(key, self.mode, self.iv)
        padData = pad(data)
        encryptedData = cyptor.encrypt(padData)
        return base64.b64encode(encryptedData)

    def decrypt(self, data, key):
        enc = base64.b64decode(data)
        cyptor = AES.new(key, self.mode, self.iv)
        restlt = cyptor.decrypt(enc)
        return unpad(restlt.rstrip('\0'))

    def encryptDataToMi(self, data, url, method):
        destUri = url
        appId = self.app_id
        nonce = self.createNonce()
        base64Nonce = base64.b64encode(nonce)
        secret = self.getSecret(nonce)
        base64Secret = base64.b64encode(secret)
        dataBase64 = self.encrypt(data, secret)

        signature = self.createSign(method, destUri, appId, base64Secret, dataBase64, "")
        return {
            'data': dataBase64,
            'app_id': appId,
            'signature': signature,
            '_nonce': base64Nonce
        }


    def createNonce(self):
        timeInt = (int)(time.time()/60)
        r1 = (int)(random.random()*timeInt)
        r2 = (int)(random.random()*timeInt)
        nonce = struct.pack('>3L', r1, r2, timeInt)
        return nonce

    def decryptDataFromMi(self, params, url, method):
        nonce_t = base64.b64decode(params['_nonce'])
        if len(nonce_t) < 4:
            return {
                'code': -6,
                'message': '_nonce is invalid',
                'result': ''
            }

        timeInof = struct.unpack(">3L", nonce_t)
        timeMinNow = (int)(time.time()/60)
        if abs(timeInof[2]-timeMinNow) > 2:
            return {
                'code': -6,
                'message': 'time > 2 minutes',
                'result': ''
            }
        else:
            secret = self.getSecret(nonce_t)
            secretB64 = base64.b64encode(secret)
            signature = params['signature']
            requestData = params['data']
            path = url
            appId = params['app_id']
            sign = self.createSign(method, path, appId, secretB64, requestData, "")
            if signature == sign:
                return self.decrypt(requestData, secret)
            else:
                return {
                    'code': -6,
                    'message': 'check sign fail',
                    'result': ''
                }
    def getSecret(self, nonce):
        sh = hashlib.sha256(self.key)
        sh.update(nonce)
        return (sh.digest())

    def createSign(self, method, rawUrl, appId, secret, data, did):
        hashStr = ""
        if did:
            hashStr = method + "&" + rawUrl + "&app_id=" + appId + "&did=" + did + "&data=" + data + "&" + secret
        else :
            hashStr = method + "&" + rawUrl + "&app_id=" + appId + "&data=" + data + "&" + secret
        #print hashStr
        sh = hashlib.sha1()
        sh.update(hashStr)
        return base64.b64encode(sh.digest())

    def getDecryptDataSimple(self,data,_nonce):
        secret = self.getSecret(base64.b64decode(_nonce))
        return self.decrypt(data,secret)

    def getEncryptDataSimple(self,data,_nonce):
        secret = self.getSecret(base64.b64decode(_nonce))
        return self.encrypt(data,secret)
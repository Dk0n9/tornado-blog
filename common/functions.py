# coding: utf8
import re
import json
import time
import random
import urlparse
import binascii
from hashlib import pbkdf2_hmac
from string import ascii_letters


def getNowTime():
    return int(time.time())  # 取十位


def formatTime(timestamp, format='%Y-%m-%d %H:%M:%S'):
    timeObj = time.localtime(int(timestamp))
    return time.strftime(format, timeObj)


def object2Json(dictObject):
    try:
        result = json.dumps(dictObject)
        return result
    except Exception, e:
        return False


def json2Object(jsonString):
    try:
        result = json.loads(jsonString)
        return result
    except Exception, e:
        return False


def generateSalt(length=8):
    salt = ''.join(random.sample(ascii_letters, length))
    return salt


def generatePassword(source, salt):
    plainText = source[0] + salt + source[1:]
    mcrypt = pbkdf2_hmac('sha256', plainText, salt, 100000)
    return binascii.hexlify(mcrypt)  # length: 64

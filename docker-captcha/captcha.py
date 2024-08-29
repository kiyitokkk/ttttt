from flask import Flask, request

import bypassgeetest
from aes import AESCrypt
from md5 import getmd5

app = Flask(__name__)
@app.route("/captcha/geetest", methods=['POST'])
def geetest():

    encrypt_data = request.data
    timestamp = request.headers.get('timestamp')
    sign = request.headers.get('sign')
    if getmd5(timestamp) == sign:
        aes = AESCrypt(sign[:16], sign[16:])
        decrypt_data = aes.decrypt(encrypt_data)
        bypass = bypassgeetest.BypassGeetest(decrypt_data)
        return bypass.run()
    else:
        return "参数错误"




@app.route("/captcha", methods=['GET'])
def test():
    return "Captcha Server"

app.run(host="0.0.0.0", port=6060)


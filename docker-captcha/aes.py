# coding:utf-8
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class AESCrypt:
    def __init__(self, key, iv):
        self.key = key.encode('utf-8') # 密钥 16、24或32字节
        self.mode = AES.MODE_CBC  # 模式
        self.iv = iv.encode('utf-8')# 初始化向量 16字节

    def encrpyt(self, text):
        '''加密'''
        text_pad = pad(text.encode('utf-8'), AES.block_size)  # 填充后的字节串
        crpytor = AES.new(self.key, self.mode, self.iv)  # 生成算法对象
        encrypt_data = crpytor.encrypt(text_pad)  # 对数据进行加密
        # return base64.b64encode(encrypt_data).decode()
        return encrypt_data

    def decrypt(self, text):
        '''解密'''
        # data = base64.b64decode(text.encode())
        crpytor = AES.new(self.key, self.mode, self.iv)
        decrypt_data = crpytor.decrypt(text)  # 对数据进行解密
        res = unpad(decrypt_data, AES.block_size).decode()  # 去除多余字符
        return res


#
# if __name__ == '__main__':
#     aes = AESCrypt("1234567891234561", "1234567891234561")
#     data = '1234awdawdawdawdaadawaawdawda56'
#     encrypt_data = aes.encrpyt(data)
#     print(f'【{data}】加密-->【{encrypt_data}】')
#     decrypt_data = aes.decrypt(encrypt_data)
#     print(f'【{encrypt_data}】解密-->【{decrypt_data}】')

import base64
import time
import uuid
import execjs
import requests
import json
import cv2
import random


def identify_gap(bg, tp, out):
    """
    bg: 背景图片
    tp: 缺口图片
    out:输出图片
    """
    # 读取背景图片和缺口图片
    bg_img = cv2.imread(bg)  # 背景图片
    tp_img = cv2.imread(tp)  # 缺口图片

    # 识别图片边缘
    bg_edge = cv2.Canny(bg_img, 100, 200)
    tp_edge = cv2.Canny(tp_img, 100, 200)

    # 转换图片格式
    bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
    tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)

    # 缺口匹配
    res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配

    # 绘制方框
    th, tw = tp_pic.shape[:2]
    tl = max_loc  # 左上角点的坐标
    br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标
    cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2)  # 绘制矩形
    cv2.imwrite(out, bg_img)  # 保存在本地

    # 返回缺口的X坐标
    return tl[0]


def save_img_(img_src, name):
    try:
        response = requests.get(img_src)
        with open(name, 'wb') as file_obj:
            file_obj.write(response.content)
    except:
        print("图片保存失败")


def get_time():
    from datetime import datetime, timezone, timedelta
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    return formatted_time


class BypassGeetest():
    # 极验本地滑块验证
    def __init__(self, captchaId):
        self.time_str = None
        self.captchaId = captchaId
        self.req_timestamp = 0
        self.img_bg_path = 'bg.jpg'
        self.img_silce_path = 'slice.jpg'
        self.img_out_path = 'result.jpg'
        self.lot_number = ''
        self.slice = ''
        self.bg = ''
        self.ypos = ''
        self.datetime = ''
        self.payload = ''
        self.process_token = ''
        self.w = ''

    def get_img_(self):
        req_timestamp = int(time.time() * 1000)
        url = ("https://gcaptcha4.geetest.com/load?callback=geetest_{}&captcha_id={}&challenge={"
               "}&client_type=web&risk_type=slide&lang=zh").format(
            req_timestamp, self.captchaId, uuid.uuid4())
        res = requests.get(url)
        res = json.loads(res.text[22:-1])['data']
        save_img_("https://static.geetest.com/" + res['bg'], "bg.jpg")
        save_img_("https://static.geetest.com/" + res['slice'], "slice.jpg")
        self.lot_number = res['lot_number']
        self.slice = res['slice']
        self.bg = res['bg']
        self.ypos = res['ypos']
        self.process_token = res['process_token']
        self.payload = res['payload']
        self.datetime = res['pow_detail']['datetime']
        self.time_str = get_time()

    def get_w_(self):
        x_ = identify_gap(self.img_bg_path, self.img_silce_path, self.img_out_path)
        e = {"setLeft": x_, "passtime": random.randint(1000, 3000), "userresponse": x_ + 0.8590780160645,
             "device_id": "",
             "lot_number": self.lot_number,
             "pow_msg": "1|0|md5|{}|24f56dc13c40dc4a02fd0318567caef5"
                        "|8930a87fd9174f758d74450c534b2001||51aa715baa40f7fa".format(self.time_str),
             "pow_sign": "27958eb8a398b0a69b9b236d622eb874", "geetest": "captcha", "lang": "zh", "ep": "123",
             "biht": "1426265548", "Wf3q": "TI7T",
             "em": {"ph": 0, "cp": 0, "ek": "11", "wd": 1, "nt": 0, "si": 0, "sc": 0}}
        e = json.dumps(e)
        t = {
            "captchaId": self.captchaId,
            "product": "float",
            "btnWidth": "100%",
            "language": "zho",
            "riskType": "slide",
            "protocol": "https://",
            "lotNumber": self.lot_number,
            "captchaType": "slide",
            "slice": self.slice,
            "bg": self.bg,
            "ypos": self.ypos,
            "arrow": "arrow_1",
            "js": "/js/gcaptcha4.js",
            "css": "/css/gcaptcha4.css",
            "staticPath": "/v4/static/v1.7.9-6a43b6",
            "gctPath": "/v4/gct/gct4.5a2e755576738ba0499d714db4f1c9e0.js",
            "showVoice": False,
            "feedback": "https://www.geetest.com/Helper",
            "logo": True,
            "pt": "1",
            "captchaMode": "risk_manage",
            "guard": False,
            "checkDevice": True,
            "customTheme": {
                "_style": "stereoscopic",
                "_color": "hsla(224,98%,66%,1)",
                "_gradient": "linear-gradient(180deg, hsla(224,98%,71%,1) 0%, hsla(224,98%,66%,1) 100%)",
                "_hover": "linear-gradient(180deg, hsla(224,98%,66%,1) 0%, hsla(224,98%,71%,1) 100%)",
                "_brightness": "system",
                "_radius": "4px"
            },
            "powDetail": {
                "version": "1",
                "bits": 0,
                "datetime": self.datetime,
                "hashfunc": "md5"
            },
            "payload": self.payload,
            "processToken": self.process_token,
            "payloadProtocol": 1,
            "hash": "76b2d6af",
            "outside": True,
            "hideBindSuccess": False,
            "hideSuccess": False,
            "clientType": "web",
            "animate": False,
            "ques": 42,
            "imgs": [
                "captcha_v4/e70fbf1d77/slide/491f18e9b8/2022-04-21T09/bg/68704c8506844eb79b8499eb6a160873.png",
                "captcha_v4/e70fbf1d77/slide/491f18e9b8/2022-04-21T09/slice/68704c8506844eb79b8499eb6a160873.png"
            ],
            "deviceId": "",
            "powMsg": "1|0|md5|{}|24f56dc13c40dc4a02fd0318567caef5|8930a87fd9174f758d74450c534b2001||51aa715baa40f7fa".format(
                self.time_str),
            "powSign": "27958eb8a398b0a69b9b236d622eb874"
        }
        with open('geetest.js', 'r', encoding='utf-8') as f:
            jscode = f.read()
        w = execjs.compile(jscode).call('window.code', e, t)
        self.w = w

    def _pass(self):
        url = "https://gcaptcha4.geetest.com/verify"
        self.req_timestamp = int(time.time() * 1000)
        params = {
            "callback": "geetest_{}".format(self.req_timestamp),
            "captcha_id": self.captchaId,
            "client_type": "web",
            "lot_number": self.lot_number,
            "risk_type": "slide",
            "payload": self.payload,
            "process_token": self.process_token,
            "payload_protocol": "1",
            "pt": "1",
            "w": self.w
        }

        res = requests.get(url, params=params)
        try:
            return json.loads(res.text[22: -1])
        except:
            return "Geetest Server err"

    def run(self):
        self.get_img_()
        self.get_w_()
        return self._pass()

# geetest_1723197846054(
# bypass = BypassGeetest('24f56dc13c40dc4a02fd0318567caef5')
# for i in range(10):
# bypass.run()


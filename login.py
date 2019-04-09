from PIL import Image
from pymongo import MongoClient
import sys, os
from lxml import etree
sys.path.append(os.path.dirname(__file__))

import requests
import time
import json
import base64
from mylogger import Mylogger
from retrying import retry



USER_AGENT_LIST = [

    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
    "Opera/8.0 (Windows NT 5.1; U; en)",
    "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
    # Firefox
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    # Safari
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
    # chrome
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
    # 360
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    # 淘宝浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    # 猎豹浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    # QQ浏览器
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    # sogou浏览器
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
    # maxthon浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
    # UC浏览器
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    # IPod
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    # IPAD
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    # Android
    "Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    # QQ浏览器 Android版本
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    # Android Opera Mobile
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    # Android Pad Moto Xoom
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    # BlackBerry
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    # WebOS HP Touchpad
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    # Nokia N97
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    # Windows Phone Mango
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    # UC浏览器
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    # UCOpenwave
    "Openwave/ UCWEB7.0.2.37/28/999",
    # UC Opera
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",

    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"

]


class CodeError(Exception):
    pass

class Captchas(object):
    '''
    下载验证码
    '''

    answer = {
        "1": "23,35",
        "2": "110,43",
        "3": "192,41",
        "4": "263,44",
        "5": "43,118",
        "6": "101,117",
        "7": "178,116",
        "8": "263,117",

    }

    def __init__(self, session):
        self.session = session
        self.logger = Mylogger(name="12306", filename="logger.log", level="debug", stream=True).getlogger()
        self.headers = Login().headers

    def _download(self):
        url = "https://kyfw.12306.cn/passport/captcha/captcha-image64?"
        timestamp = str(int(time.time() * 1000))
        response = self.session.get(url + timestamp, headers=self.headers)

        # 判断返回数据是否为json类型
        try:
            data_parse = json.loads(response.text)
        except Exception as e:
            return self.download()

        img = data_parse["image"]
        code = data_parse["result_code"]
        msg = data_parse["result_message"]
        if code == "0":
            with open("captcha.jpg", "wb") as f:
                f.write(base64.b64decode(img))
            print("验证码保存成功")
        else:
            print("验证码保存失败")
            raise CodeError("{} code:{}".format(msg, code))
        time.sleep(1)

    def download(self):
        try:
            self._download()
        except CodeError as e:
            self.logger.warning("验证码保存失败， 错误：{}".format(e))
        except Exception as e:
            self.logger.error("验证码保存失败， 错误：{}".format(e))

    def get_captcha(self):
        '''
        获取验证码
        :return:
        '''
        url = "http://littlebigluo.qicp.net:47720/"
        session = requests.session()
        session.get(url=url, headers=self.headers)
        response = requests.post(
            url=url,
            files={
                "pic_xxfile": ("captcha.jpg", open("captcha.jpg", "rb"))
            },
            headers=self.headers
        )
        html = etree.HTML(response.content)
        text = html.xpath("//b/text()")[0].split()
        print("验证码为{}".format(" ".join(text)))
        return text

    def check_captcha(self, text):
        '''
        检验验证码
        :return:
        '''
        url = "https://kyfw.12306.cn/passport/captcha/captcha-check?answer={}&rand=sjrand&_={}"
        answer = []
        for i in text:
            answer.append(self.answer.get(str(i)))
        answer = ",".join(answer)
        timestamp = str(int(time.time() * 1000))
        response = self.session.get(url=url.format(answer, timestamp), headers=self.headers)
        data = json.loads(response.text)
        if data.get("result_code") == "4":
            return answer
        else:
            print(data)
            return False

class Login(object):
    ckeck_num = 0

    def __init__(self):
        self.session = requests.session()
        self.collection = MongoClient()["12306"]
        self.logger = Mylogger(name="12306", filename="logger.log", level="debug", stream=True).getlogger()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
        }

    def login_captcha(self):
        # 获取验证码
        captcha = Captchas(self.session)
        captcha.download()
        try:
            text = captcha.get_captcha()
            # 手动输入验证码
            # Image.open("captcha.jpg").show()
            # text = "".join(input("请输入验证码:").split())
        except IndexError as e:
            # 出现验证错误时等待5秒， 重新验证
            self.logger.warning(e)
            time.sleep(5)
            return self.login_captcha()
        return  captcha.check_captcha(text)

    def post_uamtk(self):
        url = "https://kyfw.12306.cn/passport/web/auth/uamtk-static"
        data={
            "appid": "otn",
        }
        response = self.session.post(url, data=data, headers=self.headers)
        msg = json.loads(response.text)
        print("uamtk", msg)
        if msg.get("result_message") == "验证通过":
            newapptk = msg.get("newapptk")
            return newapptk
        return None

    def post_uamauthclient(self, tk):
        url = "https://exservice.12306.cn/excater/uamauthclient"
        data = {"tk": tk}
        response = self.session.post(url, data=data, headers=self.headers)
        msg = json.loads(response.text)
        print("uamauthclient", msg)

    def post_checkLogin(self):
        url = "https://exservice.12306.cn/excater/login/checkLogin"
        response = self.session.post(url, headers=self.headers)
        msg = json.loads(response.text)
        print("ckecklogin", msg)

    def login(self, username, password, answer):
        url = "https://kyfw.12306.cn/passport/web/login"
        data = {
            "username": username,
            "password": password,
            "appid": "otn",
            "answer": answer,
        }
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": self.headers.get("User-Agent"),
            "Host": "kyfw.12306.cn",
            "Origin": "https://kyfw.12306.cn",
            "Referer": "https://kyfw.12306.cn/otn/resources/login.html",
        }
        self.session.cookies = requests.utils.add_dict_to_cookiejar(self.session.cookies, {"Cookie": "RAIL_DEVICEID=lxsNg_IyE0cbSQL4X7qIuKIjb32-voxjxYOv0OzLtU5lSZvW8htTvgs8T33oWMVkK9K_f7Lm8-KAKV0WJLPokcWZ012DrJgxH3q97V2m1PeaqzgbwW8pVJfdtLHOOcuyShvCGB6gMBueQRpwC7LS-Z6cVJa1ozzP"})
        response = self.session.post(url, data=data, headers=headers)
        if response.status_code == 200:
            msg = json.loads(response.text)
            print("msg", msg)
            return msg
        return

    def run(self,username, password):
        self.post_uamtk()
        answer = self.login_captcha()
        if not answer:
            return self.run(username, password)
        # 验证码识别成功
        else:
            print("验证码成功识别")
            msg = self.login(username, password, answer)
            if msg:
                if msg.get("result_code") == 0:
                    print("success")
                    tk = self.post_uamtk()
                    if tk:
                        self.post_uamauthclient(tk)
                        self.post_checkLogin()
                        print("登入成功")
                        return True
                else:
                    self.ckeck_num += 1
                    print("msg", msg)
                    if self.ckeck_num > 3:
                        print("尝试次数大于3次， 关闭程序")
                        return False
                    return self.run(username, password)




if __name__ == '__main__':

    login = Login()
    login.run(username, password")

import requests
import cookiejar

class Fuckzb():
    def __init__(self, name, pwd):
        self.name = name
        self.pwd = pwd
        self.s = requests.session()
        r = self.s.get('http://erp.atitech.com.cn/platform/passport/login.aspx')
        self.cookie = r.cookies


    def log(self):
        url = 'http://erp.atitech.com.cn/platform/passport/login.aspx?Anthem_CallBack=true'
        headers = {
            'Host': 'erp.atitech.com.cn',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-cn',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'http://erp.atitech.com.cn',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4',
            'Connection': 'keep-alive',
            'Referer': 'http://erp.atitech.com.cn/platform/passport/login.aspx',
            'Content-Length': '336',
        }
        data = {
            'Anthem_PageMethod': 'Client_Callback',
            'Anthem_UpdatePage': 'true',
            '__CLIENTPOSTDATA': 'platform_login%7CLogin%7CS%3A%3BS%3A'+ self.name +'%3BS%3A' + self.pwd + '%7C',
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '%2FwEPDwUJNTcyNDc5NTA3ZGSz3AtbmMvyRZeJPN43n2iVgAUaMg%3D%3D',
            '__VIEWSTATEGENERATOR': 'F05B9FE7',
            # 'ctl00$content$platform_login$validatebox_validateInputControl': yzm,
        }
        data['ctl00$content$platform_login$validatebox_validateInputControl'] = self.yzm()
        r = self.s.post(url=url, headers=headers, data=data, cookies = self.cookie)
        print(r.content)


    def yzm(self):
        url = 'http://erp.atitech.com.cn/CommonPages/EOS.ValidateCode.aspx'
        r = self.s.get(url=url, cookies = self.cookie)
        print(r.cookies)
        with open('cached/yzm.jpg', 'wb') as f:
            f.write(r.content)
        yzm = input(': ')
        return yzm

        





if __name__ == '__main__':
    f1 = Fuckzb('deanliu','amber1203')
    f1.log()
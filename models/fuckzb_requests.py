import requests
from flask import session,request
import json
from bs4 import BeautifulSoup
import random
import math
from models import Model

class Fuckzb(Model):
    def __init__(self):
        self.s = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4',
        }
        r = self.s.get('http://erp.atitech.com.cn/platform/passport/login.aspx', headers = self.headers)
        self.d_cookies = requests.utils.dict_from_cookiejar(r.cookies)
        # self.d_cookies = requests.utils.dict_from_cookiejar(r.cookies)


    def yzm(self):
        code = random.randint(1000000000,9999999999)
        url = 'http://erp.atitech.com.cn/CommonPages/EOS.ValidateCode.aspx?code={}'.format(code,)
        r = self.s.get(url=url, headers = self.headers, cookies = self.d_cookies)
        with open('static/img/{}.jpg'.format(code,), 'wb') as f:
            f.write(r.content)
        # yzm = input(': ')
        return code

    # @classmethod
    # def yzm(cls):
    #     code = random.randint(1000000000,9999999999)
    #     url = 'http://erp.atitech.com.cn/CommonPages/EOS.ValidateCode.aspx?code={}'.format(code,)
    #     r = requests.get(url=url, headers = cls.headers, cookies = cls.d_cookies)
    #     with open('static/img/{}.jpg'.format(code,), 'wb') as f:
    #         f.write(r.content)
    #     # yzm = input(': ')
    #     return code

    def log(self,name,pwd,yzm):
        url = 'http://erp.atitech.com.cn/platform/passport/login.aspx?Anthem_CallBack=true'
        data = {
            'Anthem_PageMethod': 'Client_Callback',
            'Anthem_UpdatePage': 'true',
            # '__CLIENTPOSTDATA': 'platform_login%7CLogin%7CS%3A%3BS%3A'+ self.name +'%3BS%3A' + self.pwd + '%7C',
            '__CLIENTPOSTDATA': 'platform_login|Login|S:;S:{};S:{}|'.format(name, pwd),
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            # '__VIEWSTATE': '%2FwEPDwUJNTcyNDc5NTA3ZGSz3AtbmMvyRZeJPN43n2iVgAUaMg%3D%3D',
            '__VIEWSTATE': '/wEPDwUJNTcyNDc5NTA3ZGSz3AtbmMvyRZeJPN43n2iVgAUaMg==',
            '__VIEWSTATEGENERATOR': 'F05B9FE7',
            'ctl00$content$platform_login$validatebox_validateInputControl': yzm,
        }
        r = requests.post(url=url, headers=self.headers, data=data, cookies = self.d_cookies)
        return json.loads(r.text)['value']

    # @classmethod
    # def log(cls,name,pwd,yzm):
    #     url = 'http://erp.atitech.com.cn/platform/passport/login.aspx?Anthem_CallBack=true'
    #     data = {
    #         'Anthem_PageMethod': 'Client_Callback',
    #         'Anthem_UpdatePage': 'true',
    #         # '__CLIENTPOSTDATA': 'platform_login%7CLogin%7CS%3A%3BS%3A'+ self.name +'%3BS%3A' + self.pwd + '%7C',
    #         '__CLIENTPOSTDATA': 'platform_login|Login|S:;S:{};S:{}|'.format(name, pwd),
    #         '__EVENTTARGET': '',
    #         '__EVENTARGUMENT': '',
    #         # '__VIEWSTATE': '%2FwEPDwUJNTcyNDc5NTA3ZGSz3AtbmMvyRZeJPN43n2iVgAUaMg%3D%3D',
    #         '__VIEWSTATE': '/wEPDwUJNTcyNDc5NTA3ZGSz3AtbmMvyRZeJPN43n2iVgAUaMg==',
    #         '__VIEWSTATEGENERATOR': 'F05B9FE7',
    #         'ctl00$content$platform_login$validatebox_validateInputControl': yzm,
    #     }
    #     r = requests.post(url=url, headers=cls.headers, data=data, cookies = cls.d_cookies)
    #     return json.loads(r.text)['value']

    def get_zblist(self):
        url = 'http://erp.atitech.com.cn/iss/hr_techlog/prj_mainworklogquery_List.aspx?OBJID=389012f1-384f-447c-98ee-b2d32d0e44e9'
        r = requests.get(url=url, cookies = self.d_cookies, headers = self.headers)
        e = BeautifulSoup(r.text, "lxml")
        l = e.find_all("tr", class_='eosAjaxGridItem')
        all_contents = []
        for i in l:
            content = []
            for j in range(len(i.contents)):
                if j == 1 and i.contents[j].input == None:
                    break
                if j == 1 and i.contents[j].input != None:
                    content.append(i.contents[j].input['value'])
                else:
                    content.append(i.contents[j].string)
            if len(content) > 5:
                all_contents.append(content)
        return all_contents

    def get_addlist(self):
        url = 'http://erp.atitech.com.cn/iss/hr_techlog/prj_mainworklog_List.aspx?OBJID=5be9513b-4816-4864-952e-87779f9dcef4'
        r = requests.get(url=url, cookies = self.d_cookies, headers = self.headers)
        e = BeautifulSoup(r.text, "lxml")
        l = e.find_all("tr", class_='eosAjaxGridItem')
        # all_contents = [[j.string for j in i.contents] for i in l]
        # return all_contents

        all_contents = []
        for i in l:
            content = []
            for j in range(len(i.contents)):
                if j == 1 and i.contents[j].input == None:
                    break
                if j == 1 and i.contents[j].input != None:
                    content.append(i.contents[j].input['value'])
                else:
                    content.append(i.contents[j].string)
            if len(content) > 5:
                all_contents.append(content)
        return all_contents

    # @classmethod
    # def get_addlist(cls):
    #     url = 'http://erp.atitech.com.cn/iss/hr_techlog/prj_mainworklog_List.aspx?OBJID=5be9513b-4816-4864-952e-87779f9dcef4'
    #     r = requests.get(url=url, cookies = cls.d_cookies, headers = cls.headers)
    #     e = BeautifulSoup(r.text)
    #     l = e.find_all("tr", class_='eosAjaxGridItem')
    #     all_contents = []
    #     for i in l:
    #         content = []
    #         for j in range(len(i.contents)):
    #             if j == 1 and i.contents[j].input == None:
    #                 break
    #             if j == 1 and i.contents[j].input != None:
    #                 content.append(i.contents[j].input['value'])
    #             else:
    #                 content.append(i.contents[j].string)
    #         if len(content) > 5:
    #             all_contents.append(content)
    #     return all_contents

    def delete_zb(self, del_id):
        url = 'http://erp.atitech.com.cn/iss/hr_techlog/prj_mainworklog_List.aspx?OBJID=5be9513b-4816-4864-952e-87779f9dcef4&Anthem_CallBack=true'
        data = {
            'Anthem_PageMethod': 'Execute',
            'Anthem_UpdatePage': 'true',
            # '__CLIENTPOSTDATA': 'e_deletesql%7CExec%7CS%3Aea538a2f-ffa8-4e0a-a588-c600b87b895f',
            '__CLIENTPOSTDATA': 'e_deletesql|Exec|S:{}'.format(del_id,),
            # '__VIEWSTATE': '%2FwEPDwULLTEyNzQ3NTczMzEPZBYCZg9kFgICAw9kFgQCAQ8PFgIeBUxvZ2VkZ2QWAmYPDxYCHgRUZXh0BagB5oqA5pyv5pel5b%2BXIC0%2BIDxhIGhyZWY9Ii4uLy4uL2lzcy9ocl90ZWNobG9nL3Byal9tYWlud29ya2xvZ19MaXN0LmFzcHg%2FT0JKSUQ9NWJlOTUxM2ItNDgxNi00ODY0LTk1MmUtODc3NzlmOWRjZWY0IiB0aXRsZT0i5pel5b%2BX5aGr5YaZIiB0YXJnZXQ9Il9zZWxmIj7ml6Xlv5floavlhpk8L2E%2BZGQCAw9kFgJmD2QWAmYPZBYIAgEPDxYCHwFlZGQCAg8QZGQWAWZkAgMPDxYCHwFlZGQCBA8PFgIfAWVkZGRmIjRrU2h7Od6jXlY%2FolvVG6bKSQ%3D%3D',
            '__VIEWSTATE': '/wEPDwULLTEyNzQ3NTczMzEPZBYCZg9kFgICAw9kFgQCAQ8PFgIeBUxvZ2VkZ2QWAmYPDxYCHgRUZXh0BagB5oqA5pyv5pel5b+XIC0+IDxhIGhyZWY9Ii4uLy4uL2lzcy9ocl90ZWNobG9nL3Byal9tYWlud29ya2xvZ19MaXN0LmFzcHg/T0JKSUQ9NWJlOTUxM2ItNDgxNi00ODY0LTk1MmUtODc3NzlmOWRjZWY0IiB0aXRsZT0i5pel5b+X5aGr5YaZIiB0YXJnZXQ9Il9zZWxmIj7ml6Xlv5floavlhpk8L2E+ZGQCAw9kFgJmD2QWAmYPZBYIAgEPDxYCHwFlZGQCAg8QZGQWAWZkAgMPDxYCHwFlZGQCBA8PFgIfAWVkZGRmIjRrU2h7Od6jXlY/olvVG6bKSQ==',
            '__VIEWSTATEGENERATOR': '43C509D3',
            'ctl00$content$s_prj_worklog$s_prj_worklog$dt_Date_Start': '',
            'ctl00$content$s_prj_worklog$s_prj_worklog$dt_Date_End': '',
            'ctl00$content$s_prj_worklog$s_prj_worklog$e_Name': '',
            'ctl00$content$s_prj_worklog$s_prj_worklog$e_logstate': '',
            'ctl00$content$s_prj_worklog$s_prj_worklog$e_id': '',
            'ctl00$content$s_prj_worklog$s_prj_worklog$e_prj': '',
            '__EVENTTARGET': '',
        }
        requests.post(url = url , data = data , headers = self.headers, cookies = self.d_cookies)

    # @classmethod
    # def delete_zb(cls, del_id):
    #     url = 'http://erp.atitech.com.cn/iss/hr_techlog/prj_mainworklog_List.aspx?OBJID=5be9513b-4816-4864-952e-87779f9dcef4&Anthem_CallBack=true'
    #     data = {
    #         'Anthem_PageMethod': 'Execute',
    #         'Anthem_UpdatePage': 'true',
    #         # '__CLIENTPOSTDATA': 'e_deletesql%7CExec%7CS%3Aea538a2f-ffa8-4e0a-a588-c600b87b895f',
    #         '__CLIENTPOSTDATA': 'e_deletesql|Exec|S:{}'.format(del_id,),
    #         # '__VIEWSTATE': '%2FwEPDwULLTEyNzQ3NTczMzEPZBYCZg9kFgICAw9kFgQCAQ8PFgIeBUxvZ2VkZ2QWAmYPDxYCHgRUZXh0BagB5oqA5pyv5pel5b%2BXIC0%2BIDxhIGhyZWY9Ii4uLy4uL2lzcy9ocl90ZWNobG9nL3Byal9tYWlud29ya2xvZ19MaXN0LmFzcHg%2FT0JKSUQ9NWJlOTUxM2ItNDgxNi00ODY0LTk1MmUtODc3NzlmOWRjZWY0IiB0aXRsZT0i5pel5b%2BX5aGr5YaZIiB0YXJnZXQ9Il9zZWxmIj7ml6Xlv5floavlhpk8L2E%2BZGQCAw9kFgJmD2QWAmYPZBYIAgEPDxYCHwFlZGQCAg8QZGQWAWZkAgMPDxYCHwFlZGQCBA8PFgIfAWVkZGRmIjRrU2h7Od6jXlY%2FolvVG6bKSQ%3D%3D',
    #         '__VIEWSTATE': '/wEPDwULLTEyNzQ3NTczMzEPZBYCZg9kFgICAw9kFgQCAQ8PFgIeBUxvZ2VkZ2QWAmYPDxYCHgRUZXh0BagB5oqA5pyv5pel5b+XIC0+IDxhIGhyZWY9Ii4uLy4uL2lzcy9ocl90ZWNobG9nL3Byal9tYWlud29ya2xvZ19MaXN0LmFzcHg/T0JKSUQ9NWJlOTUxM2ItNDgxNi00ODY0LTk1MmUtODc3NzlmOWRjZWY0IiB0aXRsZT0i5pel5b+X5aGr5YaZIiB0YXJnZXQ9Il9zZWxmIj7ml6Xlv5floavlhpk8L2E+ZGQCAw9kFgJmD2QWAmYPZBYIAgEPDxYCHwFlZGQCAg8QZGQWAWZkAgMPDxYCHwFlZGQCBA8PFgIfAWVkZGRmIjRrU2h7Od6jXlY/olvVG6bKSQ==',
    #         '__VIEWSTATEGENERATOR': '43C509D3',
    #         'ctl00$content$s_prj_worklog$s_prj_worklog$dt_Date_Start': '',
    #         'ctl00$content$s_prj_worklog$s_prj_worklog$dt_Date_End': '',
    #         'ctl00$content$s_prj_worklog$s_prj_worklog$e_Name': '',
    #         'ctl00$content$s_prj_worklog$s_prj_worklog$e_logstate': '',
    #         'ctl00$content$s_prj_worklog$s_prj_worklog$e_id': '',
    #         'ctl00$content$s_prj_worklog$s_prj_worklog$e_prj': '',
    #         '__EVENTTARGET': '',
    #     }
    #     requests.post(url = url , data = data , headers = cls.headers, cookies = cls.d_cookies)


    def add_zb(self, date):
        url = 'http://erp.atitech.com.cn/iss/hr_techlog/prj_mainworklog_AddOrEdit.aspx?DT=0.5859502467063469&Anthem_CallBack=true'
        data = {
            'Anthem_PageMethod': 'Client_Callback',
            'Anthem_UpdatePage': 'true',
            # '__CLIENTPOSTDATA': 'v_prj_worklog%7CSave%7C%7C',
            '__CLIENTPOSTDATA': 'v_prj_worklog|Save||',
            # '__VIEWSTATE': '%2FwEPDwUJMjM1OTQ5NDE1D2QWAmYPZBYCAgMPZBYCZg9kFgICAQ9kFgJmD2QWAmYPDxYCHgRUZXh0BQoyMDE3LTA2LTEzFgIeCG9uY2hhbmdlBSVqYXZhc2NyaXB0Ol9kdDJfQ2hlY2tEYXRlKHRoaXMudmFsdWUpZGT7Sxdo3jIAcW4hLdPnBzuSpanHMw%3D%3D',
            '__VIEWSTATE': '/wEPDwUJMjM1OTQ5NDE1D2QWAmYPZBYCAgMPZBYCZg9kFgICAQ9kFgJmD2QWAmYPDxYCHgRUZXh0BQoyMDE3LTA2LTEzFgIeCG9uY2hhbmdlBSVqYXZhc2NyaXB0Ol9kdDJfQ2hlY2tEYXRlKHRoaXMudmFsdWUpZGT7Sxdo3jIAcW4hLdPnBzuSpanHMw==',
            '__VIEWSTATEGENERATOR': '7CD15153',
            'ctl00$content$v_prj_worklog$v_prj_worklog$sd': date,
            '__EVENTTARGET': '',
        }
        r = self.s.post(url = url , data = data , headers = self.headers, cookies = self.d_cookies)
        return json.loads(r.text)['value'][2:-1]

    # @classmethod
    # def add_zb(cls, date):
    #     url = 'http://erp.atitech.com.cn/iss/hr_techlog/prj_mainworklog_AddOrEdit.aspx?DT=0.5859502467063469&Anthem_CallBack=true'
    #     data = {
    #         'Anthem_PageMethod': 'Client_Callback',
    #         'Anthem_UpdatePage': 'true',
    #         # '__CLIENTPOSTDATA': 'v_prj_worklog%7CSave%7C%7C',
    #         '__CLIENTPOSTDATA': 'v_prj_worklog|Save||',
    #         # '__VIEWSTATE': '%2FwEPDwUJMjM1OTQ5NDE1D2QWAmYPZBYCAgMPZBYCZg9kFgICAQ9kFgJmD2QWAmYPDxYCHgRUZXh0BQoyMDE3LTA2LTEzFgIeCG9uY2hhbmdlBSVqYXZhc2NyaXB0Ol9kdDJfQ2hlY2tEYXRlKHRoaXMudmFsdWUpZGT7Sxdo3jIAcW4hLdPnBzuSpanHMw%3D%3D',
    #         '__VIEWSTATE': '/wEPDwUJMjM1OTQ5NDE1D2QWAmYPZBYCAgMPZBYCZg9kFgICAQ9kFgJmD2QWAmYPDxYCHgRUZXh0BQoyMDE3LTA2LTEzFgIeCG9uY2hhbmdlBSVqYXZhc2NyaXB0Ol9kdDJfQ2hlY2tEYXRlKHRoaXMudmFsdWUpZGT7Sxdo3jIAcW4hLdPnBzuSpanHMw==',
    #         '__VIEWSTATEGENERATOR': '7CD15153',
    #         'ctl00$content$v_prj_worklog$v_prj_worklog$sd': date,
    #         '__EVENTTARGET': '',
    #     }
    #     r = requests.post(url = url , data = data , headers = cls.headers, cookies = cls.d_cookies)
    #     return json.loads(r.text)['value'][2:-1]

    def add_zb_detail(self, date, start_time, end_time, content):
        mainlog = self.add_zb(date)
        overwork = 2
        overwork_hour = ''
        if int(end_time[0:2]) > 18:
            overwork = 1
            overwork_hour = math.ceil(int(end_time[0:2]) - 18)
        url = 'http://erp.atitech.com.cn/iss/hr_techlog/prj_SubWorklog_AddOrEdit.aspx?PK=&MAINLOG=' +  mainlog + '&DATE=' + date +'+00%3a00%3a00&DT=0.7084406246866846&Anthem_CallBack=true'
        data = {
            'Anthem_PageMethod': 'Client_Callback',
            'Anthem_UpdatePage': 'true',
            # '__CLIENTPOSTDATA': 'v_prj_worklog%7CSave%7C%7C',
            '__CLIENTPOSTDATA': 'v_prj_worklog|Save||',
            # '__VIEWSTATE': '%2FwEPDwUJMjUxNjQ3OTE1D2QWAmYPZBYCAgMPZBYCZg9kFgICAQ9kFgJmD2QWFmYPDxYCHgRUZXh0BRMyMDE3LTA2LTEzIDAwOjAwOjAwFgIeCG9uY2hhbmdlBSVqYXZhc2NyaXB0Ol9kdDJfQ2hlY2tEYXRlKHRoaXMudmFsdWUpZAIBDw8WAh8ABQkyMDE3LTYtMTMWAh8BBSVqYXZhc2NyaXB0Ol9kdDJfQ2hlY2tEYXRlKHRoaXMudmFsdWUpFgJmDw8WBh4FV2lkdGgbAAAAAAAAQUABAAAAHglNYXhMZW5ndGgCBR4EXyFTQgKAAhYCHwEFKmphdmFzY3JpcHQ6Y3RsQ2hlY2tUaW1lKHRoaXMudmFsdWUsJ2hobW0nKWQCAg8PFgIfAAUJMjAxNy02LTEzFgIfAQUlamF2YXNjcmlwdDpfZHQyX0NoZWNrRGF0ZSh0aGlzLnZhbHVlKRYCZg8PFgYfAhsAAAAAAABBQAEAAAAfAwIFHwQCgAIWAh8BBSpqYXZhc2NyaXB0OmN0bENoZWNrVGltZSh0aGlzLnZhbHVlLCdoaG1tJylkAgMPEGRkFgFmZAIEDw8WAh8AZWRkAgUPDxYCHwBlFgIeCm9uZGJsY2xpY2sF0wVjdGxTaG93Q29kZURpYWxvZyhjdGwwMF9jb250ZW50X3ZfcHJqX3dvcmtsb2dfdl9wcmpfd29ya2xvZ19lX0NVU1RPTUVSX0lELCAnQ1VTX0NVU1RPTUVSLkNvZGUsTkFNRScsICdpc3MnLCAncEtleScsICcnLCAnJywgJ1N0YXRlPVwnMVwnIGFuZCAocGtleSBpbiAoc2VsZWN0IG9iamVjdF9pZCBmcm9tIFNUX1NUQVRJT05fT0JKRUNUIHdoZXJlIFNUQVRJT05fSUQgaW4gKHNlbGVjdCBwa2V5IGZyb20gU1RfU1RBVElPTiB3aGVyZSBleGlzdHMgKHNlbGVjdCAxIGZyb20gU3RfU3RhdGlvbl9QZXJzb25fVmlldyBiIHdoZXJlIExvZ2luTmFtZT1cJ2RlYW5saXVcJyBhbmQgU3RhdGlvblR5cGU9XCcyXCcgYW5kIFNUX1NUQVRJT04uQ29kZSBsaWtlIGIuU3RhdGlvbkNvZGUlMkJcJyVcJykpKSBvciBwa2V5IGluIChzZWxlY3QgQ1VTVE9NRVJfSUQgZnJvbSBTQUxfUFJPSkVDVCB3aGVyZSBwa2V5IGluIChzZWxlY3Qgb2JqZWN0X2lkIGZyb20gU1RfU1RBVElPTl9PQkpFQ1Qgd2hlcmUgU1RBVElPTl9JRCBpbiAoc2VsZWN0IHBrZXkgZnJvbSBTVF9TVEFUSU9OIHdoZXJlIGV4aXN0cyAoc2VsZWN0IDEgZnJvbSBTdF9TdGF0aW9uX1BlcnNvbl9WaWV3IGIgd2hlcmUgTG9naW5OYW1lPVwnZGVhbmxpdVwnIGFuZCBTdGF0aW9uVHlwZT1cJzFcJyBhbmQgU1RfU1RBVElPTi5Db2RlIGxpa2UgYi5TdGF0aW9uQ29kZSUyQlwnJVwnKSkpKSknLCBmYWxzZSwgJ0NvZGUnLCBmYWxzZSkWAgIBDxYGHgV2YWx1ZQUD4oCmHgdvbmNsaWNrBdMFY3RsU2hvd0NvZGVEaWFsb2coY3RsMDBfY29udGVudF92X3Byal93b3JrbG9nX3ZfcHJqX3dvcmtsb2dfZV9DVVNUT01FUl9JRCwgJ0NVU19DVVNUT01FUi5Db2RlLE5BTUUnLCAnaXNzJywgJ3BLZXknLCAnJywgJycsICdTdGF0ZT1cJzFcJyBhbmQgKHBrZXkgaW4gKHNlbGVjdCBvYmplY3RfaWQgZnJvbSBTVF9TVEFUSU9OX09CSkVDVCB3aGVyZSBTVEFUSU9OX0lEIGluIChzZWxlY3QgcGtleSBmcm9tIFNUX1NUQVRJT04gd2hlcmUgZXhpc3RzIChzZWxlY3QgMSBmcm9tIFN0X1N0YXRpb25fUGVyc29uX1ZpZXcgYiB3aGVyZSBMb2dpbk5hbWU9XCdkZWFubGl1XCcgYW5kIFN0YXRpb25UeXBlPVwnMlwnIGFuZCBTVF9TVEFUSU9OLkNvZGUgbGlrZSBiLlN0YXRpb25Db2RlJTJCXCclXCcpKSkgb3IgcGtleSBpbiAoc2VsZWN0IENVU1RPTUVSX0lEIGZyb20gU0FMX1BST0pFQ1Qgd2hlcmUgcGtleSBpbiAoc2VsZWN0IG9iamVjdF9pZCBmcm9tIFNUX1NUQVRJT05fT0JKRUNUIHdoZXJlIFNUQVRJT05fSUQgaW4gKHNlbGVjdCBwa2V5IGZyb20gU1RfU1RBVElPTiB3aGVyZSBleGlzdHMgKHNlbGVjdCAxIGZyb20gU3RfU3RhdGlvbl9QZXJzb25fVmlldyBiIHdoZXJlIExvZ2luTmFtZT1cJ2RlYW5saXVcJyBhbmQgU3RhdGlvblR5cGU9XCcxXCcgYW5kIFNUX1NUQVRJT04uQ29kZSBsaWtlIGIuU3RhdGlvbkNvZGUlMkJcJyVcJykpKSkpJywgZmFsc2UsICdDb2RlJywgZmFsc2UpHgdWaXNpYmxlaGQCBg8PFgIfAGUWAh8FBakFY3RsU2hvd0NvZGVEaWFsb2coY3RsMDBfY29udGVudF92X3Byal93b3JrbG9nX3ZfcHJqX3dvcmtsb2dfZV9QUk9KRUNUX0lELCAnU0FMX1BST0pFQ1QuQ29kZSxOYW1lJywgJ2lzcycsICdwS2V5JywgJycsICcnLCAnQXVkaXRTdGF0ZT1cJzFcJyBhbmQgKENVU1RPTUVSX0lEIGluIChzZWxlY3Qgb2JqZWN0X2lkIGZyb20gU1RfU1RBVElPTl9PQkpFQ1Qgd2hlcmUgU1RBVElPTl9JRCBpbiAoc2VsZWN0IHBrZXkgZnJvbSBTVF9TVEFUSU9OIHdoZXJlIGV4aXN0cyAoc2VsZWN0IDEgZnJvbSBTdF9TdGF0aW9uX1BlcnNvbl9WaWV3IGIgd2hlcmUgTG9naW5OYW1lPVwnZGVhbmxpdVwnIGFuZCBTdGF0aW9uVHlwZT1cJzJcJyBhbmQgU1RfU1RBVElPTi5Db2RlIGxpa2UgYi5TdGF0aW9uQ29kZSUyQlwnJVwnKSkpIG9yIHBrZXkgaW4gKHNlbGVjdCBvYmplY3RfaWQgZnJvbSBTVF9TVEFUSU9OX09CSkVDVCB3aGVyZSBTVEFUSU9OX0lEIGluIChzZWxlY3QgcGtleSBmcm9tIFNUX1NUQVRJT04gd2hlcmUgZXhpc3RzIChzZWxlY3QgMSBmcm9tIFN0X1N0YXRpb25fUGVyc29uX1ZpZXcgYiB3aGVyZSBMb2dpbk5hbWU9XCdkZWFubGl1XCcgYW5kIFN0YXRpb25UeXBlPVwnMVwnIGFuZCBTVF9TVEFUSU9OLkNvZGUgbGlrZSBiLlN0YXRpb25Db2RlJTJCXCclXCcpKSkpJywgZmFsc2UsICdDb2RlJywgZmFsc2UpFgICAQ8WBh8GBQPigKYfBwWpBWN0bFNob3dDb2RlRGlhbG9nKGN0bDAwX2NvbnRlbnRfdl9wcmpfd29ya2xvZ192X3Byal93b3JrbG9nX2VfUFJPSkVDVF9JRCwgJ1NBTF9QUk9KRUNULkNvZGUsTmFtZScsICdpc3MnLCAncEtleScsICcnLCAnJywgJ0F1ZGl0U3RhdGU9XCcxXCcgYW5kIChDVVNUT01FUl9JRCBpbiAoc2VsZWN0IG9iamVjdF9pZCBmcm9tIFNUX1NUQVRJT05fT0JKRUNUIHdoZXJlIFNUQVRJT05fSUQgaW4gKHNlbGVjdCBwa2V5IGZyb20gU1RfU1RBVElPTiB3aGVyZSBleGlzdHMgKHNlbGVjdCAxIGZyb20gU3RfU3RhdGlvbl9QZXJzb25fVmlldyBiIHdoZXJlIExvZ2luTmFtZT1cJ2RlYW5saXVcJyBhbmQgU3RhdGlvblR5cGU9XCcyXCcgYW5kIFNUX1NUQVRJT04uQ29kZSBsaWtlIGIuU3RhdGlvbkNvZGUlMkJcJyVcJykpKSBvciBwa2V5IGluIChzZWxlY3Qgb2JqZWN0X2lkIGZyb20gU1RfU1RBVElPTl9PQkpFQ1Qgd2hlcmUgU1RBVElPTl9JRCBpbiAoc2VsZWN0IHBrZXkgZnJvbSBTVF9TVEFUSU9OIHdoZXJlIGV4aXN0cyAoc2VsZWN0IDEgZnJvbSBTdF9TdGF0aW9uX1BlcnNvbl9WaWV3IGIgd2hlcmUgTG9naW5OYW1lPVwnZGVhbmxpdVwnIGFuZCBTdGF0aW9uVHlwZT1cJzFcJyBhbmQgU1RfU1RBVElPTi5Db2RlIGxpa2UgYi5TdGF0aW9uQ29kZSUyQlwnJVwnKSkpKScsIGZhbHNlLCAnQ29kZScsIGZhbHNlKR8IaGQCBw8PFgIfAGVkZAIIDxBkZBYBAgFkAgkPDxYCHwBlZGQCCg8PFgIfAGVkZGSzzVIeLKe6V1XDP1L3WpEEFuh9NA%3D%3D',
            '__VIEWSTATE': '/wEPDwUJMjUxNjQ3OTE1D2QWAmYPZBYCAgMPZBYCZg9kFgICAQ9kFgJmD2QWFmYPDxYCHgRUZXh0BRMyMDE3LTA2LTEzIDAwOjAwOjAwFgIeCG9uY2hhbmdlBSVqYXZhc2NyaXB0Ol9kdDJfQ2hlY2tEYXRlKHRoaXMudmFsdWUpZAIBDw8WAh8ABQkyMDE3LTYtMTMWAh8BBSVqYXZhc2NyaXB0Ol9kdDJfQ2hlY2tEYXRlKHRoaXMudmFsdWUpFgJmDw8WBh4FV2lkdGgbAAAAAAAAQUABAAAAHglNYXhMZW5ndGgCBR4EXyFTQgKAAhYCHwEFKmphdmFzY3JpcHQ6Y3RsQ2hlY2tUaW1lKHRoaXMudmFsdWUsJ2hobW0nKWQCAg8PFgIfAAUJMjAxNy02LTEzFgIfAQUlamF2YXNjcmlwdDpfZHQyX0NoZWNrRGF0ZSh0aGlzLnZhbHVlKRYCZg8PFgYfAhsAAAAAAABBQAEAAAAfAwIFHwQCgAIWAh8BBSpqYXZhc2NyaXB0OmN0bENoZWNrVGltZSh0aGlzLnZhbHVlLCdoaG1tJylkAgMPEGRkFgFmZAIEDw8WAh8AZWRkAgUPDxYCHwBlFgIeCm9uZGJsY2xpY2sF0wVjdGxTaG93Q29kZURpYWxvZyhjdGwwMF9jb250ZW50X3ZfcHJqX3dvcmtsb2dfdl9wcmpfd29ya2xvZ19lX0NVU1RPTUVSX0lELCAnQ1VTX0NVU1RPTUVSLkNvZGUsTkFNRScsICdpc3MnLCAncEtleScsICcnLCAnJywgJ1N0YXRlPVwnMVwnIGFuZCAocGtleSBpbiAoc2VsZWN0IG9iamVjdF9pZCBmcm9tIFNUX1NUQVRJT05fT0JKRUNUIHdoZXJlIFNUQVRJT05fSUQgaW4gKHNlbGVjdCBwa2V5IGZyb20gU1RfU1RBVElPTiB3aGVyZSBleGlzdHMgKHNlbGVjdCAxIGZyb20gU3RfU3RhdGlvbl9QZXJzb25fVmlldyBiIHdoZXJlIExvZ2luTmFtZT1cJ2RlYW5saXVcJyBhbmQgU3RhdGlvblR5cGU9XCcyXCcgYW5kIFNUX1NUQVRJT04uQ29kZSBsaWtlIGIuU3RhdGlvbkNvZGUlMkJcJyVcJykpKSBvciBwa2V5IGluIChzZWxlY3QgQ1VTVE9NRVJfSUQgZnJvbSBTQUxfUFJPSkVDVCB3aGVyZSBwa2V5IGluIChzZWxlY3Qgb2JqZWN0X2lkIGZyb20gU1RfU1RBVElPTl9PQkpFQ1Qgd2hlcmUgU1RBVElPTl9JRCBpbiAoc2VsZWN0IHBrZXkgZnJvbSBTVF9TVEFUSU9OIHdoZXJlIGV4aXN0cyAoc2VsZWN0IDEgZnJvbSBTdF9TdGF0aW9uX1BlcnNvbl9WaWV3IGIgd2hlcmUgTG9naW5OYW1lPVwnZGVhbmxpdVwnIGFuZCBTdGF0aW9uVHlwZT1cJzFcJyBhbmQgU1RfU1RBVElPTi5Db2RlIGxpa2UgYi5TdGF0aW9uQ29kZSUyQlwnJVwnKSkpKSknLCBmYWxzZSwgJ0NvZGUnLCBmYWxzZSkWAgIBDxYGHgV2YWx1ZQUD4oCmHgdvbmNsaWNrBdMFY3RsU2hvd0NvZGVEaWFsb2coY3RsMDBfY29udGVudF92X3Byal93b3JrbG9nX3ZfcHJqX3dvcmtsb2dfZV9DVVNUT01FUl9JRCwgJ0NVU19DVVNUT01FUi5Db2RlLE5BTUUnLCAnaXNzJywgJ3BLZXknLCAnJywgJycsICdTdGF0ZT1cJzFcJyBhbmQgKHBrZXkgaW4gKHNlbGVjdCBvYmplY3RfaWQgZnJvbSBTVF9TVEFUSU9OX09CSkVDVCB3aGVyZSBTVEFUSU9OX0lEIGluIChzZWxlY3QgcGtleSBmcm9tIFNUX1NUQVRJT04gd2hlcmUgZXhpc3RzIChzZWxlY3QgMSBmcm9tIFN0X1N0YXRpb25fUGVyc29uX1ZpZXcgYiB3aGVyZSBMb2dpbk5hbWU9XCdkZWFubGl1XCcgYW5kIFN0YXRpb25UeXBlPVwnMlwnIGFuZCBTVF9TVEFUSU9OLkNvZGUgbGlrZSBiLlN0YXRpb25Db2RlJTJCXCclXCcpKSkgb3IgcGtleSBpbiAoc2VsZWN0IENVU1RPTUVSX0lEIGZyb20gU0FMX1BST0pFQ1Qgd2hlcmUgcGtleSBpbiAoc2VsZWN0IG9iamVjdF9pZCBmcm9tIFNUX1NUQVRJT05fT0JKRUNUIHdoZXJlIFNUQVRJT05fSUQgaW4gKHNlbGVjdCBwa2V5IGZyb20gU1RfU1RBVElPTiB3aGVyZSBleGlzdHMgKHNlbGVjdCAxIGZyb20gU3RfU3RhdGlvbl9QZXJzb25fVmlldyBiIHdoZXJlIExvZ2luTmFtZT1cJ2RlYW5saXVcJyBhbmQgU3RhdGlvblR5cGU9XCcxXCcgYW5kIFNUX1NUQVRJT04uQ29kZSBsaWtlIGIuU3RhdGlvbkNvZGUlMkJcJyVcJykpKSkpJywgZmFsc2UsICdDb2RlJywgZmFsc2UpHgdWaXNpYmxlaGQCBg8PFgIfAGUWAh8FBakFY3RsU2hvd0NvZGVEaWFsb2coY3RsMDBfY29udGVudF92X3Byal93b3JrbG9nX3ZfcHJqX3dvcmtsb2dfZV9QUk9KRUNUX0lELCAnU0FMX1BST0pFQ1QuQ29kZSxOYW1lJywgJ2lzcycsICdwS2V5JywgJycsICcnLCAnQXVkaXRTdGF0ZT1cJzFcJyBhbmQgKENVU1RPTUVSX0lEIGluIChzZWxlY3Qgb2JqZWN0X2lkIGZyb20gU1RfU1RBVElPTl9PQkpFQ1Qgd2hlcmUgU1RBVElPTl9JRCBpbiAoc2VsZWN0IHBrZXkgZnJvbSBTVF9TVEFUSU9OIHdoZXJlIGV4aXN0cyAoc2VsZWN0IDEgZnJvbSBTdF9TdGF0aW9uX1BlcnNvbl9WaWV3IGIgd2hlcmUgTG9naW5OYW1lPVwnZGVhbmxpdVwnIGFuZCBTdGF0aW9uVHlwZT1cJzJcJyBhbmQgU1RfU1RBVElPTi5Db2RlIGxpa2UgYi5TdGF0aW9uQ29kZSUyQlwnJVwnKSkpIG9yIHBrZXkgaW4gKHNlbGVjdCBvYmplY3RfaWQgZnJvbSBTVF9TVEFUSU9OX09CSkVDVCB3aGVyZSBTVEFUSU9OX0lEIGluIChzZWxlY3QgcGtleSBmcm9tIFNUX1NUQVRJT04gd2hlcmUgZXhpc3RzIChzZWxlY3QgMSBmcm9tIFN0X1N0YXRpb25fUGVyc29uX1ZpZXcgYiB3aGVyZSBMb2dpbk5hbWU9XCdkZWFubGl1XCcgYW5kIFN0YXRpb25UeXBlPVwnMVwnIGFuZCBTVF9TVEFUSU9OLkNvZGUgbGlrZSBiLlN0YXRpb25Db2RlJTJCXCclXCcpKSkpJywgZmFsc2UsICdDb2RlJywgZmFsc2UpFgICAQ8WBh8GBQPigKYfBwWpBWN0bFNob3dDb2RlRGlhbG9nKGN0bDAwX2NvbnRlbnRfdl9wcmpfd29ya2xvZ192X3Byal93b3JrbG9nX2VfUFJPSkVDVF9JRCwgJ1NBTF9QUk9KRUNULkNvZGUsTmFtZScsICdpc3MnLCAncEtleScsICcnLCAnJywgJ0F1ZGl0U3RhdGU9XCcxXCcgYW5kIChDVVNUT01FUl9JRCBpbiAoc2VsZWN0IG9iamVjdF9pZCBmcm9tIFNUX1NUQVRJT05fT0JKRUNUIHdoZXJlIFNUQVRJT05fSUQgaW4gKHNlbGVjdCBwa2V5IGZyb20gU1RfU1RBVElPTiB3aGVyZSBleGlzdHMgKHNlbGVjdCAxIGZyb20gU3RfU3RhdGlvbl9QZXJzb25fVmlldyBiIHdoZXJlIExvZ2luTmFtZT1cJ2RlYW5saXVcJyBhbmQgU3RhdGlvblR5cGU9XCcyXCcgYW5kIFNUX1NUQVRJT04uQ29kZSBsaWtlIGIuU3RhdGlvbkNvZGUlMkJcJyVcJykpKSBvciBwa2V5IGluIChzZWxlY3Qgb2JqZWN0X2lkIGZyb20gU1RfU1RBVElPTl9PQkpFQ1Qgd2hlcmUgU1RBVElPTl9JRCBpbiAoc2VsZWN0IHBrZXkgZnJvbSBTVF9TVEFUSU9OIHdoZXJlIGV4aXN0cyAoc2VsZWN0IDEgZnJvbSBTdF9TdGF0aW9uX1BlcnNvbl9WaWV3IGIgd2hlcmUgTG9naW5OYW1lPVwnZGVhbmxpdVwnIGFuZCBTdGF0aW9uVHlwZT1cJzFcJyBhbmQgU1RfU1RBVElPTi5Db2RlIGxpa2UgYi5TdGF0aW9uQ29kZSUyQlwnJVwnKSkpKScsIGZhbHNlLCAnQ29kZScsIGZhbHNlKR8IaGQCBw8PFgIfAGVkZAIIDxBkZBYBAgFkAgkPDxYCHwBlZGQCCg8PFgIfAGVkZGSzzVIeLKe6V1XDP1L3WpEEFuh9NA==',
            '__VIEWSTATEGENERATOR': '84FD06F3',
            # 'ctl00$content$v_prj_worklog$v_prj_worklog$e_DATE': '2017-06-13%2000%3A00%3A00',
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_DATE': date + ' 00:00:00',
            'ctl00$content$v_prj_worklog$v_prj_worklog$sd': date,
            # 'ctl00$content$v_prj_worklog$v_prj_worklog$sd_time': '9%3A00',
            'ctl00$content$v_prj_worklog$v_prj_worklog$sd_time': start_time,
            'ctl00$content$v_prj_worklog$v_prj_worklog$ed': date,
            # 'ctl00$content$v_prj_worklog$v_prj_worklog$ed_time': '18%3A00',
            'ctl00$content$v_prj_worklog$v_prj_worklog$ed_time': end_time,
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_WorkType': '211',
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_Callno': '',
            # 'ctl00$content$v_prj_worklog$v_prj_worklog$e_CUSTOMER_ID': '%E4%B8%AD%E5%9B%BD%E9%82%AE%E6%94%BF%E5%82%A8%E8%93%84%E9%93%B6%E8%A1%8C%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8',
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_CUSTOMER_ID': '中国邮政储蓄银行股份有限公司',
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_CUSTOMER_ID_hid': 'b00ad122-3d71-4431-bb0f-4a2e7aeb7754',
            # 'ctl00$content$v_prj_worklog$v_prj_worklog$e_PROJECT_ID': '%E4%B8%AD%E5%9B%BD%E9%82%AE%E6%94%BF%E5%82%A8%E8%93%84%E9%93%B6%E8%A1%8C%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8-%E4%B8%AD%E5%9B%BD%E9%82%AE%E6%94%BF%E5%82%A8%E8%93%84%E9%93%B6%E8%A1%8C%E9%82%AE%E6%94%BF%E9%87%91%E8%9E%8D%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%B3%BB%E7%BB%9F%E7%A1%AC%E4%BB%B6%E8%AE%BE%E5%A4%87%E7%BB%B4%E6%8A%A4%E6%9C%8D%E5%8A%A1%E9%87%87%E8%B4%AD%E5%90%88%E5%90%8C-16-2207',
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_PROJECT_ID': '中国邮政储蓄银行股份有限公司-中国邮政储蓄银行邮政金融计算机系统硬件设备维护服务采购合同-16-2207',
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_PROJECT_ID_hid': '99586bd0-4ffa-4863-94a5-fb16aef24a6a',
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_sqkh': '',
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_sfjb': overwork,    #1为加班
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_ADDHOUR': overwork_hour,  #加班小时
            # 'ctl00$content$v_prj_worklog$v_prj_worklog$e_MEMO': '%E9%A9%BB%E5%9C%BA',
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_MEMO': content.encode('gb2312'),
            'ctl00$content$v_prj_worklog$v_prj_worklog$e5_hid': '',
            '__EVENTTARGET': '',
        }
        r = self.s.post(url = url, data = data , headers = self.headers, cookies = self.d_cookies)

    # @classmethod
    # def add_zb_detail(cls, date, start_time, end_time, content):
    #     mainlog = cls.add_zb(date)
    #     overwork = 2
    #     overwork_hour = ''
    #     if int(end_time[0:2]) > 18:
    #         overwork = 1
    #         overwork_hour = math.ceil(int(end_time[0:2]) - 18)
    #     url = 'http://erp.atitech.com.cn/iss/hr_techlog/prj_SubWorklog_AddOrEdit.aspx?PK=&MAINLOG=' +  mainlog + '&DATE=' + date +'+00%3a00%3a00&DT=0.7084406246866846&Anthem_CallBack=true'
    #     data = {
    #         'Anthem_PageMethod': 'Client_Callback',
    #         'Anthem_UpdatePage': 'true',
    #         # '__CLIENTPOSTDATA': 'v_prj_worklog%7CSave%7C%7C',
    #         '__CLIENTPOSTDATA': 'v_prj_worklog|Save||',
    #         # '__VIEWSTATE': '%2FwEPDwUJMjUxNjQ3OTE1D2QWAmYPZBYCAgMPZBYCZg9kFgICAQ9kFgJmD2QWFmYPDxYCHgRUZXh0BRMyMDE3LTA2LTEzIDAwOjAwOjAwFgIeCG9uY2hhbmdlBSVqYXZhc2NyaXB0Ol9kdDJfQ2hlY2tEYXRlKHRoaXMudmFsdWUpZAIBDw8WAh8ABQkyMDE3LTYtMTMWAh8BBSVqYXZhc2NyaXB0Ol9kdDJfQ2hlY2tEYXRlKHRoaXMudmFsdWUpFgJmDw8WBh4FV2lkdGgbAAAAAAAAQUABAAAAHglNYXhMZW5ndGgCBR4EXyFTQgKAAhYCHwEFKmphdmFzY3JpcHQ6Y3RsQ2hlY2tUaW1lKHRoaXMudmFsdWUsJ2hobW0nKWQCAg8PFgIfAAUJMjAxNy02LTEzFgIfAQUlamF2YXNjcmlwdDpfZHQyX0NoZWNrRGF0ZSh0aGlzLnZhbHVlKRYCZg8PFgYfAhsAAAAAAABBQAEAAAAfAwIFHwQCgAIWAh8BBSpqYXZhc2NyaXB0OmN0bENoZWNrVGltZSh0aGlzLnZhbHVlLCdoaG1tJylkAgMPEGRkFgFmZAIEDw8WAh8AZWRkAgUPDxYCHwBlFgIeCm9uZGJsY2xpY2sF0wVjdGxTaG93Q29kZURpYWxvZyhjdGwwMF9jb250ZW50X3ZfcHJqX3dvcmtsb2dfdl9wcmpfd29ya2xvZ19lX0NVU1RPTUVSX0lELCAnQ1VTX0NVU1RPTUVSLkNvZGUsTkFNRScsICdpc3MnLCAncEtleScsICcnLCAnJywgJ1N0YXRlPVwnMVwnIGFuZCAocGtleSBpbiAoc2VsZWN0IG9iamVjdF9pZCBmcm9tIFNUX1NUQVRJT05fT0JKRUNUIHdoZXJlIFNUQVRJT05fSUQgaW4gKHNlbGVjdCBwa2V5IGZyb20gU1RfU1RBVElPTiB3aGVyZSBleGlzdHMgKHNlbGVjdCAxIGZyb20gU3RfU3RhdGlvbl9QZXJzb25fVmlldyBiIHdoZXJlIExvZ2luTmFtZT1cJ2RlYW5saXVcJyBhbmQgU3RhdGlvblR5cGU9XCcyXCcgYW5kIFNUX1NUQVRJT04uQ29kZSBsaWtlIGIuU3RhdGlvbkNvZGUlMkJcJyVcJykpKSBvciBwa2V5IGluIChzZWxlY3QgQ1VTVE9NRVJfSUQgZnJvbSBTQUxfUFJPSkVDVCB3aGVyZSBwa2V5IGluIChzZWxlY3Qgb2JqZWN0X2lkIGZyb20gU1RfU1RBVElPTl9PQkpFQ1Qgd2hlcmUgU1RBVElPTl9JRCBpbiAoc2VsZWN0IHBrZXkgZnJvbSBTVF9TVEFUSU9OIHdoZXJlIGV4aXN0cyAoc2VsZWN0IDEgZnJvbSBTdF9TdGF0aW9uX1BlcnNvbl9WaWV3IGIgd2hlcmUgTG9naW5OYW1lPVwnZGVhbmxpdVwnIGFuZCBTdGF0aW9uVHlwZT1cJzFcJyBhbmQgU1RfU1RBVElPTi5Db2RlIGxpa2UgYi5TdGF0aW9uQ29kZSUyQlwnJVwnKSkpKSknLCBmYWxzZSwgJ0NvZGUnLCBmYWxzZSkWAgIBDxYGHgV2YWx1ZQUD4oCmHgdvbmNsaWNrBdMFY3RsU2hvd0NvZGVEaWFsb2coY3RsMDBfY29udGVudF92X3Byal93b3JrbG9nX3ZfcHJqX3dvcmtsb2dfZV9DVVNUT01FUl9JRCwgJ0NVU19DVVNUT01FUi5Db2RlLE5BTUUnLCAnaXNzJywgJ3BLZXknLCAnJywgJycsICdTdGF0ZT1cJzFcJyBhbmQgKHBrZXkgaW4gKHNlbGVjdCBvYmplY3RfaWQgZnJvbSBTVF9TVEFUSU9OX09CSkVDVCB3aGVyZSBTVEFUSU9OX0lEIGluIChzZWxlY3QgcGtleSBmcm9tIFNUX1NUQVRJT04gd2hlcmUgZXhpc3RzIChzZWxlY3QgMSBmcm9tIFN0X1N0YXRpb25fUGVyc29uX1ZpZXcgYiB3aGVyZSBMb2dpbk5hbWU9XCdkZWFubGl1XCcgYW5kIFN0YXRpb25UeXBlPVwnMlwnIGFuZCBTVF9TVEFUSU9OLkNvZGUgbGlrZSBiLlN0YXRpb25Db2RlJTJCXCclXCcpKSkgb3IgcGtleSBpbiAoc2VsZWN0IENVU1RPTUVSX0lEIGZyb20gU0FMX1BST0pFQ1Qgd2hlcmUgcGtleSBpbiAoc2VsZWN0IG9iamVjdF9pZCBmcm9tIFNUX1NUQVRJT05fT0JKRUNUIHdoZXJlIFNUQVRJT05fSUQgaW4gKHNlbGVjdCBwa2V5IGZyb20gU1RfU1RBVElPTiB3aGVyZSBleGlzdHMgKHNlbGVjdCAxIGZyb20gU3RfU3RhdGlvbl9QZXJzb25fVmlldyBiIHdoZXJlIExvZ2luTmFtZT1cJ2RlYW5saXVcJyBhbmQgU3RhdGlvblR5cGU9XCcxXCcgYW5kIFNUX1NUQVRJT04uQ29kZSBsaWtlIGIuU3RhdGlvbkNvZGUlMkJcJyVcJykpKSkpJywgZmFsc2UsICdDb2RlJywgZmFsc2UpHgdWaXNpYmxlaGQCBg8PFgIfAGUWAh8FBakFY3RsU2hvd0NvZGVEaWFsb2coY3RsMDBfY29udGVudF92X3Byal93b3JrbG9nX3ZfcHJqX3dvcmtsb2dfZV9QUk9KRUNUX0lELCAnU0FMX1BST0pFQ1QuQ29kZSxOYW1lJywgJ2lzcycsICdwS2V5JywgJycsICcnLCAnQXVkaXRTdGF0ZT1cJzFcJyBhbmQgKENVU1RPTUVSX0lEIGluIChzZWxlY3Qgb2JqZWN0X2lkIGZyb20gU1RfU1RBVElPTl9PQkpFQ1Qgd2hlcmUgU1RBVElPTl9JRCBpbiAoc2VsZWN0IHBrZXkgZnJvbSBTVF9TVEFUSU9OIHdoZXJlIGV4aXN0cyAoc2VsZWN0IDEgZnJvbSBTdF9TdGF0aW9uX1BlcnNvbl9WaWV3IGIgd2hlcmUgTG9naW5OYW1lPVwnZGVhbmxpdVwnIGFuZCBTdGF0aW9uVHlwZT1cJzJcJyBhbmQgU1RfU1RBVElPTi5Db2RlIGxpa2UgYi5TdGF0aW9uQ29kZSUyQlwnJVwnKSkpIG9yIHBrZXkgaW4gKHNlbGVjdCBvYmplY3RfaWQgZnJvbSBTVF9TVEFUSU9OX09CSkVDVCB3aGVyZSBTVEFUSU9OX0lEIGluIChzZWxlY3QgcGtleSBmcm9tIFNUX1NUQVRJT04gd2hlcmUgZXhpc3RzIChzZWxlY3QgMSBmcm9tIFN0X1N0YXRpb25fUGVyc29uX1ZpZXcgYiB3aGVyZSBMb2dpbk5hbWU9XCdkZWFubGl1XCcgYW5kIFN0YXRpb25UeXBlPVwnMVwnIGFuZCBTVF9TVEFUSU9OLkNvZGUgbGlrZSBiLlN0YXRpb25Db2RlJTJCXCclXCcpKSkpJywgZmFsc2UsICdDb2RlJywgZmFsc2UpFgICAQ8WBh8GBQPigKYfBwWpBWN0bFNob3dDb2RlRGlhbG9nKGN0bDAwX2NvbnRlbnRfdl9wcmpfd29ya2xvZ192X3Byal93b3JrbG9nX2VfUFJPSkVDVF9JRCwgJ1NBTF9QUk9KRUNULkNvZGUsTmFtZScsICdpc3MnLCAncEtleScsICcnLCAnJywgJ0F1ZGl0U3RhdGU9XCcxXCcgYW5kIChDVVNUT01FUl9JRCBpbiAoc2VsZWN0IG9iamVjdF9pZCBmcm9tIFNUX1NUQVRJT05fT0JKRUNUIHdoZXJlIFNUQVRJT05fSUQgaW4gKHNlbGVjdCBwa2V5IGZyb20gU1RfU1RBVElPTiB3aGVyZSBleGlzdHMgKHNlbGVjdCAxIGZyb20gU3RfU3RhdGlvbl9QZXJzb25fVmlldyBiIHdoZXJlIExvZ2luTmFtZT1cJ2RlYW5saXVcJyBhbmQgU3RhdGlvblR5cGU9XCcyXCcgYW5kIFNUX1NUQVRJT04uQ29kZSBsaWtlIGIuU3RhdGlvbkNvZGUlMkJcJyVcJykpKSBvciBwa2V5IGluIChzZWxlY3Qgb2JqZWN0X2lkIGZyb20gU1RfU1RBVElPTl9PQkpFQ1Qgd2hlcmUgU1RBVElPTl9JRCBpbiAoc2VsZWN0IHBrZXkgZnJvbSBTVF9TVEFUSU9OIHdoZXJlIGV4aXN0cyAoc2VsZWN0IDEgZnJvbSBTdF9TdGF0aW9uX1BlcnNvbl9WaWV3IGIgd2hlcmUgTG9naW5OYW1lPVwnZGVhbmxpdVwnIGFuZCBTdGF0aW9uVHlwZT1cJzFcJyBhbmQgU1RfU1RBVElPTi5Db2RlIGxpa2UgYi5TdGF0aW9uQ29kZSUyQlwnJVwnKSkpKScsIGZhbHNlLCAnQ29kZScsIGZhbHNlKR8IaGQCBw8PFgIfAGVkZAIIDxBkZBYBAgFkAgkPDxYCHwBlZGQCCg8PFgIfAGVkZGSzzVIeLKe6V1XDP1L3WpEEFuh9NA%3D%3D',
    #         '__VIEWSTATE': '/wEPDwUJMjUxNjQ3OTE1D2QWAmYPZBYCAgMPZBYCZg9kFgICAQ9kFgJmD2QWFmYPDxYCHgRUZXh0BRMyMDE3LTA2LTEzIDAwOjAwOjAwFgIeCG9uY2hhbmdlBSVqYXZhc2NyaXB0Ol9kdDJfQ2hlY2tEYXRlKHRoaXMudmFsdWUpZAIBDw8WAh8ABQkyMDE3LTYtMTMWAh8BBSVqYXZhc2NyaXB0Ol9kdDJfQ2hlY2tEYXRlKHRoaXMudmFsdWUpFgJmDw8WBh4FV2lkdGgbAAAAAAAAQUABAAAAHglNYXhMZW5ndGgCBR4EXyFTQgKAAhYCHwEFKmphdmFzY3JpcHQ6Y3RsQ2hlY2tUaW1lKHRoaXMudmFsdWUsJ2hobW0nKWQCAg8PFgIfAAUJMjAxNy02LTEzFgIfAQUlamF2YXNjcmlwdDpfZHQyX0NoZWNrRGF0ZSh0aGlzLnZhbHVlKRYCZg8PFgYfAhsAAAAAAABBQAEAAAAfAwIFHwQCgAIWAh8BBSpqYXZhc2NyaXB0OmN0bENoZWNrVGltZSh0aGlzLnZhbHVlLCdoaG1tJylkAgMPEGRkFgFmZAIEDw8WAh8AZWRkAgUPDxYCHwBlFgIeCm9uZGJsY2xpY2sF0wVjdGxTaG93Q29kZURpYWxvZyhjdGwwMF9jb250ZW50X3ZfcHJqX3dvcmtsb2dfdl9wcmpfd29ya2xvZ19lX0NVU1RPTUVSX0lELCAnQ1VTX0NVU1RPTUVSLkNvZGUsTkFNRScsICdpc3MnLCAncEtleScsICcnLCAnJywgJ1N0YXRlPVwnMVwnIGFuZCAocGtleSBpbiAoc2VsZWN0IG9iamVjdF9pZCBmcm9tIFNUX1NUQVRJT05fT0JKRUNUIHdoZXJlIFNUQVRJT05fSUQgaW4gKHNlbGVjdCBwa2V5IGZyb20gU1RfU1RBVElPTiB3aGVyZSBleGlzdHMgKHNlbGVjdCAxIGZyb20gU3RfU3RhdGlvbl9QZXJzb25fVmlldyBiIHdoZXJlIExvZ2luTmFtZT1cJ2RlYW5saXVcJyBhbmQgU3RhdGlvblR5cGU9XCcyXCcgYW5kIFNUX1NUQVRJT04uQ29kZSBsaWtlIGIuU3RhdGlvbkNvZGUlMkJcJyVcJykpKSBvciBwa2V5IGluIChzZWxlY3QgQ1VTVE9NRVJfSUQgZnJvbSBTQUxfUFJPSkVDVCB3aGVyZSBwa2V5IGluIChzZWxlY3Qgb2JqZWN0X2lkIGZyb20gU1RfU1RBVElPTl9PQkpFQ1Qgd2hlcmUgU1RBVElPTl9JRCBpbiAoc2VsZWN0IHBrZXkgZnJvbSBTVF9TVEFUSU9OIHdoZXJlIGV4aXN0cyAoc2VsZWN0IDEgZnJvbSBTdF9TdGF0aW9uX1BlcnNvbl9WaWV3IGIgd2hlcmUgTG9naW5OYW1lPVwnZGVhbmxpdVwnIGFuZCBTdGF0aW9uVHlwZT1cJzFcJyBhbmQgU1RfU1RBVElPTi5Db2RlIGxpa2UgYi5TdGF0aW9uQ29kZSUyQlwnJVwnKSkpKSknLCBmYWxzZSwgJ0NvZGUnLCBmYWxzZSkWAgIBDxYGHgV2YWx1ZQUD4oCmHgdvbmNsaWNrBdMFY3RsU2hvd0NvZGVEaWFsb2coY3RsMDBfY29udGVudF92X3Byal93b3JrbG9nX3ZfcHJqX3dvcmtsb2dfZV9DVVNUT01FUl9JRCwgJ0NVU19DVVNUT01FUi5Db2RlLE5BTUUnLCAnaXNzJywgJ3BLZXknLCAnJywgJycsICdTdGF0ZT1cJzFcJyBhbmQgKHBrZXkgaW4gKHNlbGVjdCBvYmplY3RfaWQgZnJvbSBTVF9TVEFUSU9OX09CSkVDVCB3aGVyZSBTVEFUSU9OX0lEIGluIChzZWxlY3QgcGtleSBmcm9tIFNUX1NUQVRJT04gd2hlcmUgZXhpc3RzIChzZWxlY3QgMSBmcm9tIFN0X1N0YXRpb25fUGVyc29uX1ZpZXcgYiB3aGVyZSBMb2dpbk5hbWU9XCdkZWFubGl1XCcgYW5kIFN0YXRpb25UeXBlPVwnMlwnIGFuZCBTVF9TVEFUSU9OLkNvZGUgbGlrZSBiLlN0YXRpb25Db2RlJTJCXCclXCcpKSkgb3IgcGtleSBpbiAoc2VsZWN0IENVU1RPTUVSX0lEIGZyb20gU0FMX1BST0pFQ1Qgd2hlcmUgcGtleSBpbiAoc2VsZWN0IG9iamVjdF9pZCBmcm9tIFNUX1NUQVRJT05fT0JKRUNUIHdoZXJlIFNUQVRJT05fSUQgaW4gKHNlbGVjdCBwa2V5IGZyb20gU1RfU1RBVElPTiB3aGVyZSBleGlzdHMgKHNlbGVjdCAxIGZyb20gU3RfU3RhdGlvbl9QZXJzb25fVmlldyBiIHdoZXJlIExvZ2luTmFtZT1cJ2RlYW5saXVcJyBhbmQgU3RhdGlvblR5cGU9XCcxXCcgYW5kIFNUX1NUQVRJT04uQ29kZSBsaWtlIGIuU3RhdGlvbkNvZGUlMkJcJyVcJykpKSkpJywgZmFsc2UsICdDb2RlJywgZmFsc2UpHgdWaXNpYmxlaGQCBg8PFgIfAGUWAh8FBakFY3RsU2hvd0NvZGVEaWFsb2coY3RsMDBfY29udGVudF92X3Byal93b3JrbG9nX3ZfcHJqX3dvcmtsb2dfZV9QUk9KRUNUX0lELCAnU0FMX1BST0pFQ1QuQ29kZSxOYW1lJywgJ2lzcycsICdwS2V5JywgJycsICcnLCAnQXVkaXRTdGF0ZT1cJzFcJyBhbmQgKENVU1RPTUVSX0lEIGluIChzZWxlY3Qgb2JqZWN0X2lkIGZyb20gU1RfU1RBVElPTl9PQkpFQ1Qgd2hlcmUgU1RBVElPTl9JRCBpbiAoc2VsZWN0IHBrZXkgZnJvbSBTVF9TVEFUSU9OIHdoZXJlIGV4aXN0cyAoc2VsZWN0IDEgZnJvbSBTdF9TdGF0aW9uX1BlcnNvbl9WaWV3IGIgd2hlcmUgTG9naW5OYW1lPVwnZGVhbmxpdVwnIGFuZCBTdGF0aW9uVHlwZT1cJzJcJyBhbmQgU1RfU1RBVElPTi5Db2RlIGxpa2UgYi5TdGF0aW9uQ29kZSUyQlwnJVwnKSkpIG9yIHBrZXkgaW4gKHNlbGVjdCBvYmplY3RfaWQgZnJvbSBTVF9TVEFUSU9OX09CSkVDVCB3aGVyZSBTVEFUSU9OX0lEIGluIChzZWxlY3QgcGtleSBmcm9tIFNUX1NUQVRJT04gd2hlcmUgZXhpc3RzIChzZWxlY3QgMSBmcm9tIFN0X1N0YXRpb25fUGVyc29uX1ZpZXcgYiB3aGVyZSBMb2dpbk5hbWU9XCdkZWFubGl1XCcgYW5kIFN0YXRpb25UeXBlPVwnMVwnIGFuZCBTVF9TVEFUSU9OLkNvZGUgbGlrZSBiLlN0YXRpb25Db2RlJTJCXCclXCcpKSkpJywgZmFsc2UsICdDb2RlJywgZmFsc2UpFgICAQ8WBh8GBQPigKYfBwWpBWN0bFNob3dDb2RlRGlhbG9nKGN0bDAwX2NvbnRlbnRfdl9wcmpfd29ya2xvZ192X3Byal93b3JrbG9nX2VfUFJPSkVDVF9JRCwgJ1NBTF9QUk9KRUNULkNvZGUsTmFtZScsICdpc3MnLCAncEtleScsICcnLCAnJywgJ0F1ZGl0U3RhdGU9XCcxXCcgYW5kIChDVVNUT01FUl9JRCBpbiAoc2VsZWN0IG9iamVjdF9pZCBmcm9tIFNUX1NUQVRJT05fT0JKRUNUIHdoZXJlIFNUQVRJT05fSUQgaW4gKHNlbGVjdCBwa2V5IGZyb20gU1RfU1RBVElPTiB3aGVyZSBleGlzdHMgKHNlbGVjdCAxIGZyb20gU3RfU3RhdGlvbl9QZXJzb25fVmlldyBiIHdoZXJlIExvZ2luTmFtZT1cJ2RlYW5saXVcJyBhbmQgU3RhdGlvblR5cGU9XCcyXCcgYW5kIFNUX1NUQVRJT04uQ29kZSBsaWtlIGIuU3RhdGlvbkNvZGUlMkJcJyVcJykpKSBvciBwa2V5IGluIChzZWxlY3Qgb2JqZWN0X2lkIGZyb20gU1RfU1RBVElPTl9PQkpFQ1Qgd2hlcmUgU1RBVElPTl9JRCBpbiAoc2VsZWN0IHBrZXkgZnJvbSBTVF9TVEFUSU9OIHdoZXJlIGV4aXN0cyAoc2VsZWN0IDEgZnJvbSBTdF9TdGF0aW9uX1BlcnNvbl9WaWV3IGIgd2hlcmUgTG9naW5OYW1lPVwnZGVhbmxpdVwnIGFuZCBTdGF0aW9uVHlwZT1cJzFcJyBhbmQgU1RfU1RBVElPTi5Db2RlIGxpa2UgYi5TdGF0aW9uQ29kZSUyQlwnJVwnKSkpKScsIGZhbHNlLCAnQ29kZScsIGZhbHNlKR8IaGQCBw8PFgIfAGVkZAIIDxBkZBYBAgFkAgkPDxYCHwBlZGQCCg8PFgIfAGVkZGSzzVIeLKe6V1XDP1L3WpEEFuh9NA==',
    #         '__VIEWSTATEGENERATOR': '84FD06F3',
    #         # 'ctl00$content$v_prj_worklog$v_prj_worklog$e_DATE': '2017-06-13%2000%3A00%3A00',
    #         'ctl00$content$v_prj_worklog$v_prj_worklog$e_DATE': date + ' 00:00:00',
    #         'ctl00$content$v_prj_worklog$v_prj_worklog$sd': date,
    #         # 'ctl00$content$v_prj_worklog$v_prj_worklog$sd_time': '9%3A00',
    #         'ctl00$content$v_prj_worklog$v_prj_worklog$sd_time': start_time,
    #         'ctl00$content$v_prj_worklog$v_prj_worklog$ed': date,
    #         # 'ctl00$content$v_prj_worklog$v_prj_worklog$ed_time': '18%3A00',
    #         'ctl00$content$v_prj_worklog$v_prj_worklog$ed_time': end_time,
    #         'ctl00$content$v_prj_worklog$v_prj_worklog$e_WorkType': '211',
    #         'ctl00$content$v_prj_worklog$v_prj_worklog$e_Callno': '',
    #         # 'ctl00$content$v_prj_worklog$v_prj_worklog$e_CUSTOMER_ID': '%E4%B8%AD%E5%9B%BD%E9%82%AE%E6%94%BF%E5%82%A8%E8%93%84%E9%93%B6%E8%A1%8C%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8',
    #         'ctl00$content$v_prj_worklog$v_prj_worklog$e_CUSTOMER_ID': '中国邮政储蓄银行股份有限公司',
    #         'ctl00$content$v_prj_worklog$v_prj_worklog$e_CUSTOMER_ID_hid': 'b00ad122-3d71-4431-bb0f-4a2e7aeb7754',
    #         # 'ctl00$content$v_prj_worklog$v_prj_worklog$e_PROJECT_ID': '%E4%B8%AD%E5%9B%BD%E9%82%AE%E6%94%BF%E5%82%A8%E8%93%84%E9%93%B6%E8%A1%8C%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8-%E4%B8%AD%E5%9B%BD%E9%82%AE%E6%94%BF%E5%82%A8%E8%93%84%E9%93%B6%E8%A1%8C%E9%82%AE%E6%94%BF%E9%87%91%E8%9E%8D%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%B3%BB%E7%BB%9F%E7%A1%AC%E4%BB%B6%E8%AE%BE%E5%A4%87%E7%BB%B4%E6%8A%A4%E6%9C%8D%E5%8A%A1%E9%87%87%E8%B4%AD%E5%90%88%E5%90%8C-16-2207',
    #         'ctl00$content$v_prj_worklog$v_prj_worklog$e_PROJECT_ID': '中国邮政储蓄银行股份有限公司-中国邮政储蓄银行邮政金融计算机系统硬件设备维护服务采购合同-16-2207',
    #         'ctl00$content$v_prj_worklog$v_prj_worklog$e_PROJECT_ID_hid': '99586bd0-4ffa-4863-94a5-fb16aef24a6a',
    #         'ctl00$content$v_prj_worklog$v_prj_worklog$e_sqkh': '',
    #         'ctl00$content$v_prj_worklog$v_prj_worklog$e_sfjb': overwork,    #1为加班
    #         'ctl00$content$v_prj_worklog$v_prj_worklog$e_ADDHOUR': overwork_hour,  #加班小时
    #         # 'ctl00$content$v_prj_worklog$v_prj_worklog$e_MEMO': '%E9%A9%BB%E5%9C%BA',
    #         'ctl00$content$v_prj_worklog$v_prj_worklog$e_MEMO': content.encode('gb2312'),
    #         'ctl00$content$v_prj_worklog$v_prj_worklog$e5_hid': '',
    #         '__EVENTTARGET': '',
    #     }
    #     r = requests.post(url = url, data = data , headers = cls.headers, cookies = cls.d_cookies)

if __name__ == '__main__':
    f1 = Fuckzb()
    f1.log_local('deanliu','amber1203')
    f1.get_zblist()
    # f1.add_zb('2017-06-12')
    # f1.add_zb('2017-06-13')
    # f1.add_zb_detail('2017-06-12')
    # f1.add_zb_detail('2017-06-13')
    # f1.add_zb_detail('2017-06-14')
    # f1.add_zb_detail('2017-06-15')
    # f1.add_zb_detail('2017-06-16')
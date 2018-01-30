# -*- coding: UTF-8 -*-
import requests
from flask import session, request
import json
from bs4 import BeautifulSoup
import random
import math
from models import Model
import sys
import os

reload(sys)
sys.setdefaultencoding( "utf-8" )

path = 'data/session.txt'

def save(data):
    """
    本函数把一个 dict 或者 list 写入文件
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    # json 是一个序列化/反序列化(上课会讲这两个名词) list/dict 的库
    # indent 是缩进
    # ensure_ascii=False 用于保存中文
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+') as f:
        # log('save', path, s, data)
        # f.write(s)
        f.write(s)


def load(p):
    """
    本函数从一个文件中载入数据并转化为 dict 或者 list
    path 是保存文件的路径
    """
    with open(p, 'r') as f:
        s = f.read()
        return json.loads(s)
        # return s

class Fuckzb(Model):
    def __init__(self):
        self.s = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) '
                          'Version/10.1.1 Safari/603.2.4',
            'host': '58.30.224.47:8888',
        }
        # r = self.s.get('http://58.30.224.47:8888/platform/passport/login.aspx', headers = self.headers)
        self.d_cookies = None

    def yzm(self):
        user_list = load(path)
        code = random.randint(1000000000, 9999999999)
        url = 'http://58.30.224.47:8888/CommonPages/EOS.ValidateCode.aspx?code={}'.format(code, )
        r = self.s.post(url=url, headers=self.headers)
        self.d_cookies = requests.utils.dict_from_cookiejar(r.cookies)
        session['cookie'] = self.d_cookies
        s = session['cookie']
        s['code'] = code
        user_list.append(s)
        save(user_list)
        with open('static/img/{}.png'.format(code, ), 'wb') as f:
            f.write(r.content)
        return code

    def log(self, name, pwd, yzm, code):
        session['cookie'].pop('code')
        url = 'http://58.30.224.47:8888/platform/passport/login.aspx?Anthem_CallBack=true'
        data = {
            'Anthem_PageMethod': 'Client_Callback',
            'Anthem_UpdatePage': 'true',
            '__CLIENTPOSTDATA': 'platform_login|Login|S:;S:{};S:{}|'.format(name, pwd),
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '/wEPDwUJNTcyNDc5NTA3ZGTHE5+6kqqiPI2D8SP+xpGQ6pQaRw==',
            '__VIEWSTATEGENERATOR': 'F05B9FE7',
            'ctl00$content$platform_login$validatebox_validateInputControl': yzm,
        }

        session['userid'] = name
        session['code'] = code
        user_list = load(path)
        checked = 0
        l = []
        for i in user_list:
            if len(session['cookie']) != 0:
                if "ASP.NET_SessionId" in i:
                    if i["ASP.NET_SessionId"] == session["cookie"]["ASP.NET_SessionId"]:
                        i['userid'] = name
                        l.append(i)
                    else:
                        l.append(i)
            else:
                if len(i) == 0:
                    l.append({'userid': name})
                else:
                    l.append(i)
        save(l)

        if len(session['cookie']) == 0:
            r = self.s.post(url=url, headers=self.headers, data=data, cookies=session['cookie'])
            session['cookie'] = self.d_cookies
        else:
            r = self.s.post(url=url, headers=self.headers, data=data, cookies=session['cookie'])
        r = self.s.post(url=url, headers=self.headers, data=data)
        os.remove('static/img/{}.png'.format(code, ))
        return json.loads(r.text)['value'], code


    def get_zblist(self):
        url = 'http://58.30.224.47:8888/iss/hr_techlog/prj_mainworklogquery_List.aspx?OBJID=389012f1-384f-447c-98ee-b2d32d0e44e9'
        r = self.s.get(url=url, headers=self.headers)
        e = BeautifulSoup(r.text)
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
        session['zblist'] = all_contents

    def get_addlist(self):
        url = 'http://58.30.224.47:8888/iss/hr_techlog/prj_mainworklog_List.aspx?OBJID=5be9513b-4816-4864-952e-87779f9dcef4'
        r = self.s.get(url=url, headers=self.headers)
        e = BeautifulSoup(r.text)
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
        session['zbaddlist'] = all_contents

    def delete_zb(self, del_id):
        url = 'http://58.30.224.47:8888/iss/hr_techlog/prj_mainworklog_List.aspx?OBJID=5be9513b-4816-4864-952e-87779f9dcef4&Anthem_CallBack=true'
        data = {
            'Anthem_PageMethod': 'Execute',
            'Anthem_UpdatePage': 'true',
            '__CLIENTPOSTDATA': 'e_deletesql|Exec|S:{}'.format(del_id, ),
            '__VIEWSTATE': '/wEPDwULLTEyNzQ3NTczMzEPZBYCZg9kFgICAw9kFgQCAQ8PFgIeBUxvZ2VkZ2QWAmYPDxYCHgRUZXh0BagB5oqA5pyv5pel5b+XIC0+IDxhIGhyZWY9Ii4uLy4uL2lzcy9ocl90ZWNobG9nL3Byal9tYWlud29ya2xvZ19MaXN0LmFzcHg/T0JKSUQ9NWJlOTUxM2ItNDgxNi00ODY0LTk1MmUtODc3NzlmOWRjZWY0IiB0aXRsZT0i5pel5b+X5aGr5YaZIiB0YXJnZXQ9Il9zZWxmIj7ml6Xlv5floavlhpk8L2E+ZGQCAw9kFgRmD2QWAmYPZBYIAgEPDxYCHwFlZGQCAg8QZGQWAWZkAgMPDxYCHwFlZGQCBA8PFgIfAWVkZAIBDxYCHglQYWdlSW5kZXhmZGRKV5bYyaTfC1xX5Oji7YyIvvLE6Q==',
            '__VIEWSTATEGENERATOR': '43C509D3',
            'ctl00$content$s_prj_worklog$s_prj_worklog$dt_Date_Start': '',
            'ctl00$content$s_prj_worklog$s_prj_worklog$dt_Date_End': '',
            'ctl00$content$s_prj_worklog$s_prj_worklog$e_Name': '',
            'ctl00$content$s_prj_worklog$s_prj_worklog$e_logstate': '',
            'ctl00$content$s_prj_worklog$s_prj_worklog$e_id': '',
            'ctl00$content$s_prj_worklog$s_prj_worklog$e_prj': '',
            '__EVENTTARGET': '',
        }
        self.s.post(url=url, data=data, headers=self.headers)

    def add_zb(self, date):
        url = 'http://58.30.224.47:8888/iss/hr_techlog/prj_mainworklog_AddOrEdit.aspx?DT=0.5859502467063469&Anthem_CallBack=true'
        data = {
            'Anthem_PageMethod': 'Client_Callback',
            'Anthem_UpdatePage': 'true',
            '__CLIENTPOSTDATA': 'v_prj_worklog|Save||',
            '__VIEWSTATE': '/wEPDwUJMjM1OTQ5NDE1D2QWAmYPZBYCAgMPZBYCZg9kFgICAQ9kFgJmD2QWAmYPDxYCHgRUZXh0BQoyMDE3LTA4LTMwFgIeCG9uY2hhbmdlBSVqYXZhc2NyaXB0Ol9kdDJfQ2hlY2tEYXRlKHRoaXMudmFsdWUpZGQ0LMI21nAERYn1qUKGeCkju8CATQ==',
            '__VIEWSTATEGENERATOR': '7CD15153',
            'ctl00$content$v_prj_worklog$v_prj_worklog$sd': date,
            '__EVENTTARGET': '',
        }
        r = self.s.post(url=url, data=data, headers=self.headers)
        if r.text.startswith('{'):
            return json.loads(r.text)['value']
        else:
            e = BeautifulSoup(r.text)
            l = e.form.get_text()
            return l

    def add_zb_detail(self, date, start_time, end_time, content, mainlog, overwork = 2 , overwork_hour='',work_type='211'):
        url = 'http://58.30.224.47:8888/iss/hr_techlog/prj_SubWorklog_AddOrEdit.aspx?PK=&MAINLOG=' + mainlog + '&DATE=' + date + '+00%3a00%3a00&DT=0.7084406246866846&Anthem_CallBack=true'
        data = {
            'Anthem_PageMethod': 'Client_Callback',
            'Anthem_UpdatePage': 'true',
            '__CLIENTPOSTDATA': 'v_prj_worklog|Save||',
            '__VIEWSTATE': '/wEPDwUJMjUxNjQ3OTE1D2QWAmYPZBYCAgMPZBYCZg9kFgICAQ9kFgJmD2QWFmYPDxYCHgRUZXh0BQoyMDE4LTAxLTAzFgIeCG9uY2hhbmdlBSVqYXZhc2NyaXB0Ol9kdDJfQ2hlY2tEYXRlKHRoaXMudmFsdWUpZAIBDw8WAh8ABQgyMDE4LzEvMxYCHwEFJWphdmFzY3JpcHQ6X2R0Ml9DaGVja0RhdGUodGhpcy52YWx1ZSkWAmYPDxYGHgVXaWR0aBsAAAAAAABBQAEAAAAeCU1heExlbmd0aAIFHgRfIVNCAoACFgIfAQUqamF2YXNjcmlwdDpjdGxDaGVja1RpbWUodGhpcy52YWx1ZSwnaGhtbScpZAICDw8WAh8ABQgyMDE4LzEvMxYCHwEFJWphdmFzY3JpcHQ6X2R0Ml9DaGVja0RhdGUodGhpcy52YWx1ZSkWAmYPDxYGHwIbAAAAAAAAQUABAAAAHwMCBR8EAoACFgIfAQUqamF2YXNjcmlwdDpjdGxDaGVja1RpbWUodGhpcy52YWx1ZSwnaGhtbScpZAIDDxBkZBYBAhJkAgQPDxYCHwBlZGQCBQ8PFgIfAAUq5Lit5Zu96YKu5pS/5YKo6JOE6ZO26KGM6IKh5Lu95pyJ6ZmQ5YWs5Y+4FgIeCm9uZGJsY2xpY2sF0wVjdGxTaG93Q29kZURpYWxvZyhjdGwwMF9jb250ZW50X3ZfcHJqX3dvcmtsb2dfdl9wcmpfd29ya2xvZ19lX0NVU1RPTUVSX0lELCAnQ1VTX0NVU1RPTUVSLkNvZGUsTkFNRScsICdpc3MnLCAncEtleScsICcnLCAnJywgJ1N0YXRlPVwnMVwnIGFuZCAocGtleSBpbiAoc2VsZWN0IG9iamVjdF9pZCBmcm9tIFNUX1NUQVRJT05fT0JKRUNUIHdoZXJlIFNUQVRJT05fSUQgaW4gKHNlbGVjdCBwa2V5IGZyb20gU1RfU1RBVElPTiB3aGVyZSBleGlzdHMgKHNlbGVjdCAxIGZyb20gU3RfU3RhdGlvbl9QZXJzb25fVmlldyBiIHdoZXJlIExvZ2luTmFtZT1cJ2RlYW5saXVcJyBhbmQgU3RhdGlvblR5cGU9XCcyXCcgYW5kIFNUX1NUQVRJT04uQ29kZSBsaWtlIGIuU3RhdGlvbkNvZGUlMkJcJyVcJykpKSBvciBwa2V5IGluIChzZWxlY3QgQ1VTVE9NRVJfSUQgZnJvbSBTQUxfUFJPSkVDVCB3aGVyZSBwa2V5IGluIChzZWxlY3Qgb2JqZWN0X2lkIGZyb20gU1RfU1RBVElPTl9PQkpFQ1Qgd2hlcmUgU1RBVElPTl9JRCBpbiAoc2VsZWN0IHBrZXkgZnJvbSBTVF9TVEFUSU9OIHdoZXJlIGV4aXN0cyAoc2VsZWN0IDEgZnJvbSBTdF9TdGF0aW9uX1BlcnNvbl9WaWV3IGIgd2hlcmUgTG9naW5OYW1lPVwnZGVhbmxpdVwnIGFuZCBTdGF0aW9uVHlwZT1cJzFcJyBhbmQgU1RfU1RBVElPTi5Db2RlIGxpa2UgYi5TdGF0aW9uQ29kZSUyQlwnJVwnKSkpKSknLCBmYWxzZSwgJ0NvZGUnLCBmYWxzZSkWAgIBDxYGHgV2YWx1ZQUD4oCmHgdvbmNsaWNrBdMFY3RsU2hvd0NvZGVEaWFsb2coY3RsMDBfY29udGVudF92X3Byal93b3JrbG9nX3ZfcHJqX3dvcmtsb2dfZV9DVVNUT01FUl9JRCwgJ0NVU19DVVNUT01FUi5Db2RlLE5BTUUnLCAnaXNzJywgJ3BLZXknLCAnJywgJycsICdTdGF0ZT1cJzFcJyBhbmQgKHBrZXkgaW4gKHNlbGVjdCBvYmplY3RfaWQgZnJvbSBTVF9TVEFUSU9OX09CSkVDVCB3aGVyZSBTVEFUSU9OX0lEIGluIChzZWxlY3QgcGtleSBmcm9tIFNUX1NUQVRJT04gd2hlcmUgZXhpc3RzIChzZWxlY3QgMSBmcm9tIFN0X1N0YXRpb25fUGVyc29uX1ZpZXcgYiB3aGVyZSBMb2dpbk5hbWU9XCdkZWFubGl1XCcgYW5kIFN0YXRpb25UeXBlPVwnMlwnIGFuZCBTVF9TVEFUSU9OLkNvZGUgbGlrZSBiLlN0YXRpb25Db2RlJTJCXCclXCcpKSkgb3IgcGtleSBpbiAoc2VsZWN0IENVU1RPTUVSX0lEIGZyb20gU0FMX1BST0pFQ1Qgd2hlcmUgcGtleSBpbiAoc2VsZWN0IG9iamVjdF9pZCBmcm9tIFNUX1NUQVRJT05fT0JKRUNUIHdoZXJlIFNUQVRJT05fSUQgaW4gKHNlbGVjdCBwa2V5IGZyb20gU1RfU1RBVElPTiB3aGVyZSBleGlzdHMgKHNlbGVjdCAxIGZyb20gU3RfU3RhdGlvbl9QZXJzb25fVmlldyBiIHdoZXJlIExvZ2luTmFtZT1cJ2RlYW5saXVcJyBhbmQgU3RhdGlvblR5cGU9XCcxXCcgYW5kIFNUX1NUQVRJT04uQ29kZSBsaWtlIGIuU3RhdGlvbkNvZGUlMkJcJyVcJykpKSkpJywgZmFsc2UsICdDb2RlJywgZmFsc2UpHgdWaXNpYmxlaGQCBg8PFgIfAAU85Lit5Zu96YKu5pS/5YKo6JOE6ZO26KGM6aaW5om55Yqe5YWs55So5ZOB6YWN5Lu26YeH6LSt6aG555uuFgIfBQWpBWN0bFNob3dDb2RlRGlhbG9nKGN0bDAwX2NvbnRlbnRfdl9wcmpfd29ya2xvZ192X3Byal93b3JrbG9nX2VfUFJPSkVDVF9JRCwgJ1NBTF9QUk9KRUNULkNvZGUsTmFtZScsICdpc3MnLCAncEtleScsICcnLCAnJywgJ0F1ZGl0U3RhdGU9XCcxXCcgYW5kIChDVVNUT01FUl9JRCBpbiAoc2VsZWN0IG9iamVjdF9pZCBmcm9tIFNUX1NUQVRJT05fT0JKRUNUIHdoZXJlIFNUQVRJT05fSUQgaW4gKHNlbGVjdCBwa2V5IGZyb20gU1RfU1RBVElPTiB3aGVyZSBleGlzdHMgKHNlbGVjdCAxIGZyb20gU3RfU3RhdGlvbl9QZXJzb25fVmlldyBiIHdoZXJlIExvZ2luTmFtZT1cJ2RlYW5saXVcJyBhbmQgU3RhdGlvblR5cGU9XCcyXCcgYW5kIFNUX1NUQVRJT04uQ29kZSBsaWtlIGIuU3RhdGlvbkNvZGUlMkJcJyVcJykpKSBvciBwa2V5IGluIChzZWxlY3Qgb2JqZWN0X2lkIGZyb20gU1RfU1RBVElPTl9PQkpFQ1Qgd2hlcmUgU1RBVElPTl9JRCBpbiAoc2VsZWN0IHBrZXkgZnJvbSBTVF9TVEFUSU9OIHdoZXJlIGV4aXN0cyAoc2VsZWN0IDEgZnJvbSBTdF9TdGF0aW9uX1BlcnNvbl9WaWV3IGIgd2hlcmUgTG9naW5OYW1lPVwnZGVhbmxpdVwnIGFuZCBTdGF0aW9uVHlwZT1cJzFcJyBhbmQgU1RfU1RBVElPTi5Db2RlIGxpa2UgYi5TdGF0aW9uQ29kZSUyQlwnJVwnKSkpKScsIGZhbHNlLCAnQ29kZScsIGZhbHNlKRYCAgEPFgYfBgUD4oCmHwcFqQVjdGxTaG93Q29kZURpYWxvZyhjdGwwMF9jb250ZW50X3ZfcHJqX3dvcmtsb2dfdl9wcmpfd29ya2xvZ19lX1BST0pFQ1RfSUQsICdTQUxfUFJPSkVDVC5Db2RlLE5hbWUnLCAnaXNzJywgJ3BLZXknLCAnJywgJycsICdBdWRpdFN0YXRlPVwnMVwnIGFuZCAoQ1VTVE9NRVJfSUQgaW4gKHNlbGVjdCBvYmplY3RfaWQgZnJvbSBTVF9TVEFUSU9OX09CSkVDVCB3aGVyZSBTVEFUSU9OX0lEIGluIChzZWxlY3QgcGtleSBmcm9tIFNUX1NUQVRJT04gd2hlcmUgZXhpc3RzIChzZWxlY3QgMSBmcm9tIFN0X1N0YXRpb25fUGVyc29uX1ZpZXcgYiB3aGVyZSBMb2dpbk5hbWU9XCdkZWFubGl1XCcgYW5kIFN0YXRpb25UeXBlPVwnMlwnIGFuZCBTVF9TVEFUSU9OLkNvZGUgbGlrZSBiLlN0YXRpb25Db2RlJTJCXCclXCcpKSkgb3IgcGtleSBpbiAoc2VsZWN0IG9iamVjdF9pZCBmcm9tIFNUX1NUQVRJT05fT0JKRUNUIHdoZXJlIFNUQVRJT05fSUQgaW4gKHNlbGVjdCBwa2V5IGZyb20gU1RfU1RBVElPTiB3aGVyZSBleGlzdHMgKHNlbGVjdCAxIGZyb20gU3RfU3RhdGlvbl9QZXJzb25fVmlldyBiIHdoZXJlIExvZ2luTmFtZT1cJ2RlYW5saXVcJyBhbmQgU3RhdGlvblR5cGU9XCcxXCcgYW5kIFNUX1NUQVRJT04uQ29kZSBsaWtlIGIuU3RhdGlvbkNvZGUlMkJcJyVcJykpKSknLCBmYWxzZSwgJ0NvZGUnLCBmYWxzZSkfCGhkAgcPDxYCHwBlZGQCCA8QZGQWAQIBZAIJDw8WAh8ABQEwZGQCCg8PFgIfAAUG6am75Zy6ZGRkQk0yUbCGlwKIdvxFasUQlgJ117k=',
            '__VIEWSTATEGENERATOR': '84FD06F3',
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_DATE': date + ' 00:00:00',
            'ctl00$content$v_prj_worklog$v_prj_worklog$sd': date,
            'ctl00$content$v_prj_worklog$v_prj_worklog$sd_time': start_time,
            'ctl00$content$v_prj_worklog$v_prj_worklog$ed': date,
            'ctl00$content$v_prj_worklog$v_prj_worklog$ed_time': end_time,
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_WorkType': work_type,
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_Callno': '',
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_CUSTOMER_ID': '中国邮政储蓄银行股份有限公司',
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_CUSTOMER_ID_hid': 'b00ad122-3d71-4431-bb0f-4a2e7aeb7754',
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_PROJECT_ID': '中国邮政储蓄银行股份有限公司-国邮政储蓄银行邮政金融计算机系统硬件维保服务采购项目系统维护服务部分框架合同-18-1004',
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_PROJECT_ID_hid': '4a8f8a79-a4ed-47b4-9b29-029a6be5c00b',
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_sqkh': '',
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_sfjb': overwork,  # 1为加班
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_ADDHOUR': overwork_hour,  # 加班小时
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_MEMO': content.encode('gb2312'),
            # 'ctl00$content$v_prj_worklog$v_prj_worklog$e_MEMO': content.decode('utf8').encode('gb2312'),
            'ctl00$content$v_prj_worklog$v_prj_worklog$e5_hid': '',
            '__EVENTTARGET': '',
        }
        self.s.post(url=url, data=data, headers=self.headers)

    def submitzb(self, item):
        url = 'http://58.30.224.47:8888/iss/hr_techlog/prj_mainworklog_List.aspx?OBJID=5be9513b-4816-4864-952e-87779f9dcef4&Anthem_CallBack=true'
        data = {
            'Anthem_PageMethod': 'Execute',
            'Anthem_UpdatePage': 'true',
            '__CLIENTPOSTDATA': 'e_sql|Scalar|S:{}'.format(item,),
            '__VIEWSTATE': '/wEPDwULLTEyNzQ3NTczMzEPZBYCZg9kFgICAw9kFgQCAQ8PFgIeBUxvZ2VkZ2QWAmYPDxYCHgRUZXh0BagB5oqA5pyv5pel5b+XIC0+IDxhIGhyZWY9Ii4uLy4uL2lzcy9ocl90ZWNobG9nL3Byal9tYWlud29ya2xvZ19MaXN0LmFzcHg/T0JKSUQ9NWJlOTUxM2ItNDgxNi00ODY0LTk1MmUtODc3NzlmOWRjZWY0IiB0aXRsZT0i5pel5b+X5aGr5YaZIiB0YXJnZXQ9Il9zZWxmIj7ml6Xlv5floavlhpk8L2E+ZGQCAw9kFgJmD2QWAmYPZBYIAgEPDxYCHwFlZGQCAg8QZGQWAWZkAgMPDxYCHwFlZGQCBA8PFgIfAWVkZGSwPsw7Rf1APHwNW2elyTRXArCZFg==',
            '__VIEWSTATEGENERATOR': '43C509D3',
            'ctl00$content$s_prj_worklog$s_prj_worklog$dt_Date_Start': '',
            'ctl00$content$s_prj_worklog$s_prj_worklog$dt_Date_End': '',
            'ctl00$content$s_prj_worklog$s_prj_worklog$e_Name': '',
            'ctl00$content$s_prj_worklog$s_prj_worklog$e_logstate': '',
            'ctl00$content$s_prj_worklog$s_prj_worklog$e_id': '',
            'ctl00$content$s_prj_worklog$s_prj_worklog$e_prj': '',
            'g_prj_worklog_item': item,
            '__EVENTTARGET': '',
        }
        self.s.post(url = url , data = data, headers = self.headers)
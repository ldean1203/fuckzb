import requests
from flask import session, request
import json
from bs4 import BeautifulSoup
import random
import math
from models import Model


class Fuckzb(Model):
    def __init__(self):
        self.s = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) '
                          'Version/10.1.1 Safari/603.2.4',
        }
        # r = self.s.get('http://erp.atitech.com.cn/platform/passport/login.aspx', headers = self.headers)
        # self.d_cookies = requests.utils.dict_from_cookiejar(r.cookies)

    def yzm(self):
        code = random.randint(1000000000, 9999999999)
        url = 'http://erp.atitech.com.cn/CommonPages/EOS.ValidateCode.aspx?code={}'.format(code, )
        r = self.s.get(url=url, headers=self.headers)
        d_cookies = requests.utils.dict_from_cookiejar(r.cookies)
        session['cookie'] = d_cookies
        with open('static/img/{}.jpg'.format(session['cookie']['ASP.NET_SessionId'], ), 'wb') as f:
            f.write(r.content)
        # yzm = input(': ')
        session['ASP.NET_SessionId'] = session['cookie']['ASP.NET_SessionId']
        return session['cookie']['ASP.NET_SessionId']

    def log(self, name, pwd, yzm):
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
        print('login cookies is ++++++++++++++++', session['cookie'])
        r = self.s.post(url=url, headers=self.headers, data=data, cookies=session['cookie'])
        return json.loads(r.text)['value']

    def get_zblist(self):
        url = 'http://erp.atitech.com.cn/iss/hr_techlog/prj_mainworklogquery_List.aspx?OBJID=389012f1-384f-447c-98ee-b2d32d0e44e9'
        r = self.s.get(url=url, cookies=session['cookie'], headers=self.headers)
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
        return all_contents

    def get_addlist(self):
        url = 'http://erp.atitech.com.cn/iss/hr_techlog/prj_mainworklog_List.aspx?OBJID=5be9513b-4816-4864-952e-87779f9dcef4'
        print('get_addlist cookies is ++++++++++++++++',
              session['cookie'])
        r = self.s.get(url=url, cookies=session['cookie'], headers=self.headers)
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
        return all_contents

    def delete_zb(self, del_id):
        url = 'http://erp.atitech.com.cn/iss/hr_techlog/prj_mainworklog_List.aspx?OBJID=5be9513b-4816-4864-952e-87779f9dcef4&Anthem_CallBack=true'
        data = {
            'Anthem_PageMethod': 'Execute',
            'Anthem_UpdatePage': 'true',
            '__CLIENTPOSTDATA': 'e_deletesql|Exec|S:{}'.format(del_id, ),
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
        print('delete_zb cookies is ++++++++++++++++',
              session['cookie'])
        self.s.post(url=url, data=data, headers=self.headers, cookies=session['cookie'])

    def add_zb(self, date):
        url = 'http://erp.atitech.com.cn/iss/hr_techlog/prj_mainworklog_AddOrEdit.aspx?DT=0.5859502467063469&Anthem_CallBack=true'
        data = {
            'Anthem_PageMethod': 'Client_Callback',
            'Anthem_UpdatePage': 'true',
            '__CLIENTPOSTDATA': 'v_prj_worklog|Save||',
            '__VIEWSTATE': '/wEPDwUJMjM1OTQ5NDE1D2QWAmYPZBYCAgMPZBYCZg9kFgICAQ9kFgJmD2QWAmYPDxYCHgRUZXh0BQoyMDE3LTA2LTEzFgIeCG9uY2hhbmdlBSVqYXZhc2NyaXB0Ol9kdDJfQ2hlY2tEYXRlKHRoaXMudmFsdWUpZGT7Sxdo3jIAcW4hLdPnBzuSpanHMw==',
            '__VIEWSTATEGENERATOR': '7CD15153',
            'ctl00$content$v_prj_worklog$v_prj_worklog$sd': date,
            '__EVENTTARGET': '',
        }
        r = self.s.post(url=url, data=data, headers=self.headers, cookies=session['cookie'])
        print('add zb cookies is ++++++++++++++++',
              session['cookie'])
        print('from add_zb ------------', r.text)
        return json.loads(r.text)['value']

    def add_zb_detail(self, date, start_time, end_time, content, mainlog):
        overwork = 2
        overwork_hour = ''
        if int(end_time[0:2]) > 18:
            overwork = 1
            overwork_hour = math.ceil(int(end_time[0:2]) - 18)
        url = 'http://erp.atitech.com.cn/iss/hr_techlog/prj_SubWorklog_AddOrEdit.aspx?PK=&MAINLOG=' + mainlog + '&DATE=' + date + '+00%3a00%3a00&DT=0.7084406246866846&Anthem_CallBack=true'
        data = {
            'Anthem_PageMethod': 'Client_Callback',
            'Anthem_UpdatePage': 'true',
            '__CLIENTPOSTDATA': 'v_prj_worklog|Save||',
            '__VIEWSTATE': '/wEPDwUJMjUxNjQ3OTE1D2QWAmYPZBYCAgMPZBYCZg9kFgICAQ9kFgJmD2QWFmYPDxYCHgRUZXh0BRMyMDE3LTA2LTEzIDAwOjAwOjAwFgIeCG9uY2hhbmdlBSVqYXZhc2NyaXB0Ol9kdDJfQ2hlY2tEYXRlKHRoaXMudmFsdWUpZAIBDw8WAh8ABQkyMDE3LTYtMTMWAh8BBSVqYXZhc2NyaXB0Ol9kdDJfQ2hlY2tEYXRlKHRoaXMudmFsdWUpFgJmDw8WBh4FV2lkdGgbAAAAAAAAQUABAAAAHglNYXhMZW5ndGgCBR4EXyFTQgKAAhYCHwEFKmphdmFzY3JpcHQ6Y3RsQ2hlY2tUaW1lKHRoaXMudmFsdWUsJ2hobW0nKWQCAg8PFgIfAAUJMjAxNy02LTEzFgIfAQUlamF2YXNjcmlwdDpfZHQyX0NoZWNrRGF0ZSh0aGlzLnZhbHVlKRYCZg8PFgYfAhsAAAAAAABBQAEAAAAfAwIFHwQCgAIWAh8BBSpqYXZhc2NyaXB0OmN0bENoZWNrVGltZSh0aGlzLnZhbHVlLCdoaG1tJylkAgMPEGRkFgFmZAIEDw8WAh8AZWRkAgUPDxYCHwBlFgIeCm9uZGJsY2xpY2sF0wVjdGxTaG93Q29kZURpYWxvZyhjdGwwMF9jb250ZW50X3ZfcHJqX3dvcmtsb2dfdl9wcmpfd29ya2xvZ19lX0NVU1RPTUVSX0lELCAnQ1VTX0NVU1RPTUVSLkNvZGUsTkFNRScsICdpc3MnLCAncEtleScsICcnLCAnJywgJ1N0YXRlPVwnMVwnIGFuZCAocGtleSBpbiAoc2VsZWN0IG9iamVjdF9pZCBmcm9tIFNUX1NUQVRJT05fT0JKRUNUIHdoZXJlIFNUQVRJT05fSUQgaW4gKHNlbGVjdCBwa2V5IGZyb20gU1RfU1RBVElPTiB3aGVyZSBleGlzdHMgKHNlbGVjdCAxIGZyb20gU3RfU3RhdGlvbl9QZXJzb25fVmlldyBiIHdoZXJlIExvZ2luTmFtZT1cJ2RlYW5saXVcJyBhbmQgU3RhdGlvblR5cGU9XCcyXCcgYW5kIFNUX1NUQVRJT04uQ29kZSBsaWtlIGIuU3RhdGlvbkNvZGUlMkJcJyVcJykpKSBvciBwa2V5IGluIChzZWxlY3QgQ1VTVE9NRVJfSUQgZnJvbSBTQUxfUFJPSkVDVCB3aGVyZSBwa2V5IGluIChzZWxlY3Qgb2JqZWN0X2lkIGZyb20gU1RfU1RBVElPTl9PQkpFQ1Qgd2hlcmUgU1RBVElPTl9JRCBpbiAoc2VsZWN0IHBrZXkgZnJvbSBTVF9TVEFUSU9OIHdoZXJlIGV4aXN0cyAoc2VsZWN0IDEgZnJvbSBTdF9TdGF0aW9uX1BlcnNvbl9WaWV3IGIgd2hlcmUgTG9naW5OYW1lPVwnZGVhbmxpdVwnIGFuZCBTdGF0aW9uVHlwZT1cJzFcJyBhbmQgU1RfU1RBVElPTi5Db2RlIGxpa2UgYi5TdGF0aW9uQ29kZSUyQlwnJVwnKSkpKSknLCBmYWxzZSwgJ0NvZGUnLCBmYWxzZSkWAgIBDxYGHgV2YWx1ZQUD4oCmHgdvbmNsaWNrBdMFY3RsU2hvd0NvZGVEaWFsb2coY3RsMDBfY29udGVudF92X3Byal93b3JrbG9nX3ZfcHJqX3dvcmtsb2dfZV9DVVNUT01FUl9JRCwgJ0NVU19DVVNUT01FUi5Db2RlLE5BTUUnLCAnaXNzJywgJ3BLZXknLCAnJywgJycsICdTdGF0ZT1cJzFcJyBhbmQgKHBrZXkgaW4gKHNlbGVjdCBvYmplY3RfaWQgZnJvbSBTVF9TVEFUSU9OX09CSkVDVCB3aGVyZSBTVEFUSU9OX0lEIGluIChzZWxlY3QgcGtleSBmcm9tIFNUX1NUQVRJT04gd2hlcmUgZXhpc3RzIChzZWxlY3QgMSBmcm9tIFN0X1N0YXRpb25fUGVyc29uX1ZpZXcgYiB3aGVyZSBMb2dpbk5hbWU9XCdkZWFubGl1XCcgYW5kIFN0YXRpb25UeXBlPVwnMlwnIGFuZCBTVF9TVEFUSU9OLkNvZGUgbGlrZSBiLlN0YXRpb25Db2RlJTJCXCclXCcpKSkgb3IgcGtleSBpbiAoc2VsZWN0IENVU1RPTUVSX0lEIGZyb20gU0FMX1BST0pFQ1Qgd2hlcmUgcGtleSBpbiAoc2VsZWN0IG9iamVjdF9pZCBmcm9tIFNUX1NUQVRJT05fT0JKRUNUIHdoZXJlIFNUQVRJT05fSUQgaW4gKHNlbGVjdCBwa2V5IGZyb20gU1RfU1RBVElPTiB3aGVyZSBleGlzdHMgKHNlbGVjdCAxIGZyb20gU3RfU3RhdGlvbl9QZXJzb25fVmlldyBiIHdoZXJlIExvZ2luTmFtZT1cJ2RlYW5saXVcJyBhbmQgU3RhdGlvblR5cGU9XCcxXCcgYW5kIFNUX1NUQVRJT04uQ29kZSBsaWtlIGIuU3RhdGlvbkNvZGUlMkJcJyVcJykpKSkpJywgZmFsc2UsICdDb2RlJywgZmFsc2UpHgdWaXNpYmxlaGQCBg8PFgIfAGUWAh8FBakFY3RsU2hvd0NvZGVEaWFsb2coY3RsMDBfY29udGVudF92X3Byal93b3JrbG9nX3ZfcHJqX3dvcmtsb2dfZV9QUk9KRUNUX0lELCAnU0FMX1BST0pFQ1QuQ29kZSxOYW1lJywgJ2lzcycsICdwS2V5JywgJycsICcnLCAnQXVkaXRTdGF0ZT1cJzFcJyBhbmQgKENVU1RPTUVSX0lEIGluIChzZWxlY3Qgb2JqZWN0X2lkIGZyb20gU1RfU1RBVElPTl9PQkpFQ1Qgd2hlcmUgU1RBVElPTl9JRCBpbiAoc2VsZWN0IHBrZXkgZnJvbSBTVF9TVEFUSU9OIHdoZXJlIGV4aXN0cyAoc2VsZWN0IDEgZnJvbSBTdF9TdGF0aW9uX1BlcnNvbl9WaWV3IGIgd2hlcmUgTG9naW5OYW1lPVwnZGVhbmxpdVwnIGFuZCBTdGF0aW9uVHlwZT1cJzJcJyBhbmQgU1RfU1RBVElPTi5Db2RlIGxpa2UgYi5TdGF0aW9uQ29kZSUyQlwnJVwnKSkpIG9yIHBrZXkgaW4gKHNlbGVjdCBvYmplY3RfaWQgZnJvbSBTVF9TVEFUSU9OX09CSkVDVCB3aGVyZSBTVEFUSU9OX0lEIGluIChzZWxlY3QgcGtleSBmcm9tIFNUX1NUQVRJT04gd2hlcmUgZXhpc3RzIChzZWxlY3QgMSBmcm9tIFN0X1N0YXRpb25fUGVyc29uX1ZpZXcgYiB3aGVyZSBMb2dpbk5hbWU9XCdkZWFubGl1XCcgYW5kIFN0YXRpb25UeXBlPVwnMVwnIGFuZCBTVF9TVEFUSU9OLkNvZGUgbGlrZSBiLlN0YXRpb25Db2RlJTJCXCclXCcpKSkpJywgZmFsc2UsICdDb2RlJywgZmFsc2UpFgICAQ8WBh8GBQPigKYfBwWpBWN0bFNob3dDb2RlRGlhbG9nKGN0bDAwX2NvbnRlbnRfdl9wcmpfd29ya2xvZ192X3Byal93b3JrbG9nX2VfUFJPSkVDVF9JRCwgJ1NBTF9QUk9KRUNULkNvZGUsTmFtZScsICdpc3MnLCAncEtleScsICcnLCAnJywgJ0F1ZGl0U3RhdGU9XCcxXCcgYW5kIChDVVNUT01FUl9JRCBpbiAoc2VsZWN0IG9iamVjdF9pZCBmcm9tIFNUX1NUQVRJT05fT0JKRUNUIHdoZXJlIFNUQVRJT05fSUQgaW4gKHNlbGVjdCBwa2V5IGZyb20gU1RfU1RBVElPTiB3aGVyZSBleGlzdHMgKHNlbGVjdCAxIGZyb20gU3RfU3RhdGlvbl9QZXJzb25fVmlldyBiIHdoZXJlIExvZ2luTmFtZT1cJ2RlYW5saXVcJyBhbmQgU3RhdGlvblR5cGU9XCcyXCcgYW5kIFNUX1NUQVRJT04uQ29kZSBsaWtlIGIuU3RhdGlvbkNvZGUlMkJcJyVcJykpKSBvciBwa2V5IGluIChzZWxlY3Qgb2JqZWN0X2lkIGZyb20gU1RfU1RBVElPTl9PQkpFQ1Qgd2hlcmUgU1RBVElPTl9JRCBpbiAoc2VsZWN0IHBrZXkgZnJvbSBTVF9TVEFUSU9OIHdoZXJlIGV4aXN0cyAoc2VsZWN0IDEgZnJvbSBTdF9TdGF0aW9uX1BlcnNvbl9WaWV3IGIgd2hlcmUgTG9naW5OYW1lPVwnZGVhbmxpdVwnIGFuZCBTdGF0aW9uVHlwZT1cJzFcJyBhbmQgU1RfU1RBVElPTi5Db2RlIGxpa2UgYi5TdGF0aW9uQ29kZSUyQlwnJVwnKSkpKScsIGZhbHNlLCAnQ29kZScsIGZhbHNlKR8IaGQCBw8PFgIfAGVkZAIIDxBkZBYBAgFkAgkPDxYCHwBlZGQCCg8PFgIfAGVkZGSzzVIeLKe6V1XDP1L3WpEEFuh9NA==',
            '__VIEWSTATEGENERATOR': '84FD06F3',
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_DATE': date + ' 00:00:00',
            'ctl00$content$v_prj_worklog$v_prj_worklog$sd': date,
            'ctl00$content$v_prj_worklog$v_prj_worklog$sd_time': start_time,
            'ctl00$content$v_prj_worklog$v_prj_worklog$ed': date,
            'ctl00$content$v_prj_worklog$v_prj_worklog$ed_time': end_time,
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_WorkType': '211',
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_Callno': '',
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_CUSTOMER_ID': '中国邮政储蓄银行股份有限公司',
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_CUSTOMER_ID_hid': 'b00ad122-3d71-4431-bb0f-4a2e7aeb7754',
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_PROJECT_ID': '中国邮政储蓄银行股份有限公司-中国邮政储蓄银行邮政金融计算机系统硬件设备维护服务采购合同-16-2207',
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_PROJECT_ID_hid': '99586bd0-4ffa-4863-94a5-fb16aef24a6a',
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_sqkh': '',
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_sfjb': overwork,  # 1为加班
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_ADDHOUR': overwork_hour,  # 加班小时
            'ctl00$content$v_prj_worklog$v_prj_worklog$e_MEMO': content.encode('gb2312'),
            'ctl00$content$v_prj_worklog$v_prj_worklog$e5_hid': '',
            '__EVENTTARGET': '',
        }
        print('add zb detail cookies is ++++++++++++++++',
              session['cookie'])
        r = self.s.post(url=url, data=data, headers=self.headers, cookies=session['cookie'])

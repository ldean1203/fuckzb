#!/usr/bin/python
import socket
import ssl
import requests
import os
import sys
from selenium import webdriver
import time
from pyquery import PyQuery as pq
import random
import json
driver = webdriver.Ie()


class fuckzb():
    def __init__(self):
        self.cookies = ''
        self.code = ''
        self.set_cookies()

    # 获取cookies
    def set_cookies(self):
        url = 'http://58.30.224.47/platform/passport/login.aspx'
        # self.cookies = self.get(url)
        # driver.get(url)
        driver.get(url)
        co = driver.get_cookies()
        # print('cookies is :', co)
        driver.add_cookie(co[0])
        driver.get_screenshot_as_file('cookie.jpg')
        # print('cookies is ---- :', self.cookies)

    def con(self):
        self.code = self.yzm_new()
        username = 'deanliu'
        passwd = 'amber1203'
        posturl = 'http://58.30.224.47/platform/passport/login.aspx?Anthem_CallBack=true'
        driver.get(posturl)
        listcookies = driver.get_cookies()
        for s_cookie in listcookies:
            c = driver.add_cookie(s_cookie)
            print('add_cookies -----', c)

        # 构造header，一般header至少要包含一下两项。这两项是从抓到的包里分析得出的。
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Referer': 'http://58.30.224.47/platform/passport/login.aspx',
            'X-Requested-With': 'XMLHttpRequest',
            'Host': '58.30.224.47',
            'Cookie': self.cookies,
        }
        # 构造Post数据，他也是从抓大的包里分析得出的。
        postdata = {
            'Anthem_PageMethod': 'Client_Callback',
            'Anthem_UpdatePage': 'true',
            '__CLIENTPOSTDATA': 'platform_login|Login|S:;S:' + username + ';S:' + passwd + '|',
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '/wEPDwUJNTcyNDc5NTA3ZGSz3AtbmMvyRZeJPN43n2iVgAUaMg==',
            '__VIEWSTATEGENERATOR': 'F05B9FE7',
            'ctl00$content$platform_login$validatebox_validateInputControl': self.code,
                    }
        r = requests.post(posturl, data=postdata, headers=headers)
        # text = r.content
        # print(text.decode('raw_unicode_escape'))
        print(r.status_code)

    def login(self):
        driver.get('http://58.30.224.47/platform/passport/login.aspx')

        uid = driver.find_element_by_id('uid')
        uid.send_keys('deanliu')
        pwd = driver.find_element_by_id('pwd')
        pwd.send_keys('amber1203')
        yz = driver.find_element_by_id('ctl00_content_platform_login_validatebox_validateInputControl')
        yzm = self.yzm_new()
        print(yzm)
        yz.send_keys(yzm)
        login = driver.find_element_by_id('log')
        login.click()
        driver.get_screenshot_as_file('login.jpg')

    def yzm(self):
        # self.set_cookies()
        url = 'http://58.30.224.47/CommonPages/EOS.ValidateCode.aspx'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Accept': 'image/png, image/svg+xml, image/*;q=0.8, */*;q=0.5',
            'Referer': 'http://58.30.224.47/platform/passport/login.aspx',
            'X-Requested-With': 'XMLHttpRequest',
            'Host': '58.30.224.47',
            'DNT': '1',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip,deflate',
            'Cookie': self.cookies,
        }
        r = requests.get(url, headers=headers)
        path = os.getcwd() + '/yzm.jpg'
        with open(path, 'wb') as f:
            f.write(r.content)
        if sys.platform.find('darwin') >= 0:
            os.system('open %s' % path)
        elif sys.platform.find('linux') >= 0:
            os.system('xdg-open %s' % path)
        else:
            os.system('call %s' % path)
        code = input("input your yzm:")
        return code

    def yzm_new(self):
        url = 'http://58.30.224.47/CommonPages/EOS.ValidateCode.aspx'
        driver.get(url)
        # pic = driver.get_screenshot_as_png()
        pic = driver.page_source.encode('gb2312')
        # pic = pic.encode('utf-8')
        with open('d://image.png', 'w') as f:
            f.write(pic)
        # im = Image.open('img/image.jpg')
        # im.show()
        code = input("input your yzm:")
        return code

    def yzm_new1(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Accept': 'image/png, image/svg+xml, image/*;q=0.8, */*;q=0.5',
            'Referer': 'http://58.30.224.47/platform/passport/login.aspx',
            'X-Requested-With': 'XMLHttpRequest',
            'Host': '58.30.224.47',
            'DNT': '1',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip,deflate',
            'Cookie': self.cookies,
        }
        for k, v in enumerate(headers):
            webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(k)] = v
        url = 'http://58.30.224.47/CommonPages/EOS.ValidateCode.aspx'
        driver.get(url)
        path = os.getcwd() + '/yzm.jpg'
        with open(path, 'wb') as f:
            f.write(driver.page_source.encode('utf-8'))
        if sys.platform.find('darwin') >= 0:
            os.system('open %s' % path)
        elif sys.platform.find('linux') >= 0:
            os.system('xdg-open %s' % path)
        else:
            os.system('call %s' % path)
        code = input("input your yzm:")
        return code

    def get_zblist(self):
        posturl = 'http://58.30.224.47/iss/hr_techlog/prj_mainworklogquery_List.aspx?OBJID=389012f1-384f-447c-98ee-b2d32d0e44e9'
        # 构造header，一般header至少要包含一下两项。这两项是从抓到的包里分析得出的。
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Referer': 'http://58.30.224.47/platform/portal2/index.aspx',
            'Accept': 'text/html,application/xhtml+xml,*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'Host': '58.30.224.47',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip,deflate',
             'Cookie': self.cookies,
        }
        # 通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程
        r = requests.get(posturl, headers=headers)
        text = r.content
        # print(text.decode('gb2312'))
        print(r.status_code)

    # def pre_zbadd(self):
    #     posturl = 'http://58.30.224.47/iss/hr_techlog/prj_mainworklog_List.aspx?OBJID=5be9513b-4816-4864-952e-87779f9dcef4'
    #     headers = {
    #         'User-Agent': 'Mozilla/5.0 (MSIE 9.0; Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    #         'Host': '58.30.224.47',
    #         'Accept-Language': 'zh-cn',
    #         'Accept-Encoding': 'gzip, deflate',
    #         'Referer': 'http: // 58.30.224.47/platform/portal2/index.aspx',
    #         'Connection': 'Keep-Alive',
    #         'DNT': '1',
    #         'Cookie': self.cookies,
    #     }
    #     # # 需要给Post数据编码
    #     r = requests.get(posturl, headers=headers)
    #     text = r.content
    #     e = pq(text)
    #     print('e aspnetForm ', e('#aspnetForm'))
    #     print('e action  ', e('#aspnetForm').attr('action'))
    #     print('e ?  ', e('#aspnetForm').attr('action').split('?'))
    #     item = e('#aspnetForm').attr('action').split('?')[1].split('=')[1]
    #     print(item)
    #     print('dt is =====: ', self.dt)

    def test_ph(self):
        posturl = 'http://58.30.224.47/iss/hr_techlog/prj_mainworklog_List.aspx?OBJID=5be9513b-4816-4864-952e-87779f9dcef4'
        driver.get(posturl)
        add = driver.find_element_by_xpath("//a[@href='javascript:AddCheck()']")
        add.click()
        print(driver.current_url)

    def zbadd(self, date):
        dt = random.random()
        print('dt is : ', dt)
        posturl = 'http://58.30.224.47/iss/hr_techlog/prj_mainworklog_AddOrEdit.aspx?DT={}&Anthem_CallBack=true'.format(dt)
        # 构造header，一般header至少要包含一下两项。这两项是从抓到的包里分析得出的。
        headers = {
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            'Referer': 'http://58.30.224.47/iss/hr_techlog/prj_mainworklog_AddOrEdit.aspx?DT={}'.format(dt),
            'Accept-Language': 'zh-CN',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/5.0 (MSIE 9.0; Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Connection': 'Keep-Alive',
            'Content-Length': '412',
            'DNT': '1',
            'Host': '58.30.224.47',
            'Pragma': 'no-cache',
            'Cookie':  self.cookies,
        }
        # 构造Post数据，他也是从抓大的包里分析得出的。
        postdata = {'Anthem_PageMethod': 'Client_Callback',
                    'Anthem_UpdatePage': 'true',
                    '__CLIENTPOSTDATA': 'v_prj_worklog%7CSave%7C%7C',
                    '__VIEWSTATE': '%2FwEPDwUJMjM1OTQ5NDE1D2QWAmYPZBYCAgMPZBYCZg9kFgICAQ9kFgJmD2QWAmYPDxYCHgRUZXh0BQoyMDE2LTEwLTI3FgIeCG9uY2hhbmdlBSVqYXZhc2NyaXB0Ol9kdDJfQ2hlY2tEYXRlKHRoaXMudmFsdWUpZGTFB%2BG5CKJMfzTeWy%2F1xbw%2F3v5KeQ%3D%3D',
                    '__VIEWSTATEGENERATOR': '7CD15153',
                    'ctl00$content$v_prj_worklog$v_prj_worklog$sd': date,
                    '__EVENTTARGET': '',
                    }
        # 需要给Post数据编码
        r = requests.post(posturl, data=postdata, headers=headers, hooks=dict(response=self.print_url))
        # time.sleep(10)
        text = r.content
        # print(text.decode('gb2312'))
        print(r.status_code)

    def sub_add(self):
        dt = random.random()
        print('dt is : ', dt)
        posturl = 'http://58.30.224.47/iss/hr_techlog/prj_SubWorklog_AddOrEdit.aspx?PK=&MAINLOG=607bfae5-5514-45dd-b5d1-6110ff5cb0d9&DATE=2017-04-12+00%3a00%3a00&DT={}&Anthem_CallBack=true'.format(dt)
        # 构造header，一般header至少要包含一下两项。这两项是从抓到的包里分析得出的。
        headers = {
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            'Referer': 'http://58.30.224.47/iss/hr_techlog/prj_SubWorklog_AddOrEdit.aspx?PK=&MAINLOG=607bfae5-5514-45dd-b5d1-6110ff5cb0d9&DATE=2017-04-12 00:00:00&DT={}'.format(dt),
            'Accept-Language': 'zh-CN',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/5.0 (MSIE 9.0; Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Connection': 'Keep-Alive',
            'Content-Length': '6253',
            'DNT': '1',
            'Host': '58.30.224.47',
            'Pragma': 'no-cache',
            'Cookie':  self.cookies,
        }
        # 构造Post数据，他也是从抓大的包里分析得出的。
        postdata = {"Anthem_PageMethod":"Client_Callback",
                    "Anthem_UpdatePage":"true",
                    "__CLIENTPOSTDATA":"v_prj_worklog%7CSave%7C%7C",
                    "__VIEWSTATE":"%2FwEPDwUJMjUxNjQ3OTE1D2QWAmYPZBYCAgMPZBYCZg9kFgICAQ9kFgJmD2QWFmYPDxYCHgRUZXh0BRMyMDE3LTA0LTEyIDAwOjAwOjAwFgIeCG9uY2hhbmdlBSVqYXZhc2NyaXB0Ol9kdDJfQ2hlY2tEYXRlKHRoaXMudmFsdWUpZAIBDw8WAh8ABQkyMDE3LTQtMTIWAh8BBSVqYXZhc2NyaXB0Ol9kdDJfQ2hlY2tEYXRlKHRoaXMudmFsdWUpFgJmDw8WBh4FV2lkdGgbAAAAAAAAQUABAAAAHglNYXhMZW5ndGgCBR4EXyFTQgKAAhYCHwEFKmphdmFzY3JpcHQ6Y3RsQ2hlY2tUaW1lKHRoaXMudmFsdWUsJ2hobW0nKWQCAg8PFgIfAAUJMjAxNy00LTEyFgIfAQUlamF2YXNjcmlwdDpfZHQyX0NoZWNrRGF0ZSh0aGlzLnZhbHVlKRYCZg8PFgYfAhsAAAAAAABBQAEAAAAfAwIFHwQCgAIWAh8BBSpqYXZhc2NyaXB0OmN0bENoZWNrVGltZSh0aGlzLnZhbHVlLCdoaG1tJylkAgMPEGRkFgFmZAIEDw8WAh8AZWRkAgUPDxYCHwBlFgIeCm9uZGJsY2xpY2sF0wVjdGxTaG93Q29kZURpYWxvZyhjdGwwMF9jb250ZW50X3ZfcHJqX3dvcmtsb2dfdl9wcmpfd29ya2xvZ19lX0NVU1RPTUVSX0lELCAnQ1VTX0NVU1RPTUVSLkNvZGUsTkFNRScsICdpc3MnLCAncEtleScsICcnLCAnJywgJ1N0YXRlPVwnMVwnIGFuZCAocGtleSBpbiAoc2VsZWN0IG9iamVjdF9pZCBmcm9tIFNUX1NUQVRJT05fT0JKRUNUIHdoZXJlIFNUQVRJT05fSUQgaW4gKHNlbGVjdCBwa2V5IGZyb20gU1RfU1RBVElPTiB3aGVyZSBleGlzdHMgKHNlbGVjdCAxIGZyb20gU3RfU3RhdGlvbl9QZXJzb25fVmlldyBiIHdoZXJlIExvZ2luTmFtZT1cJ2RlYW5saXVcJyBhbmQgU3RhdGlvblR5cGU9XCcyXCcgYW5kIFNUX1NUQVRJT04uQ29kZSBsaWtlIGIuU3RhdGlvbkNvZGUlMkJcJyVcJykpKSBvciBwa2V5IGluIChzZWxlY3QgQ1VTVE9NRVJfSUQgZnJvbSBTQUxfUFJPSkVDVCB3aGVyZSBwa2V5IGluIChzZWxlY3Qgb2JqZWN0X2lkIGZyb20gU1RfU1RBVElPTl9PQkpFQ1Qgd2hlcmUgU1RBVElPTl9JRCBpbiAoc2VsZWN0IHBrZXkgZnJvbSBTVF9TVEFUSU9OIHdoZXJlIGV4aXN0cyAoc2VsZWN0IDEgZnJvbSBTdF9TdGF0aW9uX1BlcnNvbl9WaWV3IGIgd2hlcmUgTG9naW5OYW1lPVwnZGVhbmxpdVwnIGFuZCBTdGF0aW9uVHlwZT1cJzFcJyBhbmQgU1RfU1RBVElPTi5Db2RlIGxpa2UgYi5TdGF0aW9uQ29kZSUyQlwnJVwnKSkpKSknLCBmYWxzZSwgJ0NvZGUnLCBmYWxzZSkWAgIBDxYGHgV2YWx1ZQUD4oCmHgdvbmNsaWNrBdMFY3RsU2hvd0NvZGVEaWFsb2coY3RsMDBfY29udGVudF92X3Byal93b3JrbG9nX3ZfcHJqX3dvcmtsb2dfZV9DVVNUT01FUl9JRCwgJ0NVU19DVVNUT01FUi5Db2RlLE5BTUUnLCAnaXNzJywgJ3BLZXknLCAnJywgJycsICdTdGF0ZT1cJzFcJyBhbmQgKHBrZXkgaW4gKHNlbGVjdCBvYmplY3RfaWQgZnJvbSBTVF9TVEFUSU9OX09CSkVDVCB3aGVyZSBTVEFUSU9OX0lEIGluIChzZWxlY3QgcGtleSBmcm9tIFNUX1NUQVRJT04gd2hlcmUgZXhpc3RzIChzZWxlY3QgMSBmcm9tIFN0X1N0YXRpb25fUGVyc29uX1ZpZXcgYiB3aGVyZSBMb2dpbk5hbWU9XCdkZWFubGl1XCcgYW5kIFN0YXRpb25UeXBlPVwnMlwnIGFuZCBTVF9TVEFUSU9OLkNvZGUgbGlrZSBiLlN0YXRpb25Db2RlJTJCXCclXCcpKSkgb3IgcGtleSBpbiAoc2VsZWN0IENVU1RPTUVSX0lEIGZyb20gU0FMX1BST0pFQ1Qgd2hlcmUgcGtleSBpbiAoc2VsZWN0IG9iamVjdF9pZCBmcm9tIFNUX1NUQVRJT05fT0JKRUNUIHdoZXJlIFNUQVRJT05fSUQgaW4gKHNlbGVjdCBwa2V5IGZyb20gU1RfU1RBVElPTiB3aGVyZSBleGlzdHMgKHNlbGVjdCAxIGZyb20gU3RfU3RhdGlvbl9QZXJzb25fVmlldyBiIHdoZXJlIExvZ2luTmFtZT1cJ2RlYW5saXVcJyBhbmQgU3RhdGlvblR5cGU9XCcxXCcgYW5kIFNUX1NUQVRJT04uQ29kZSBsaWtlIGIuU3RhdGlvbkNvZGUlMkJcJyVcJykpKSkpJywgZmFsc2UsICdDb2RlJywgZmFsc2UpHgdWaXNpYmxlaGQCBg8PFgIfAGUWAh8FBakFY3RsU2hvd0NvZGVEaWFsb2coY3RsMDBfY29udGVudF92X3Byal93b3JrbG9nX3ZfcHJqX3dvcmtsb2dfZV9QUk9KRUNUX0lELCAnU0FMX1BST0pFQ1QuQ29kZSxOYW1lJywgJ2lzcycsICdwS2V5JywgJycsICcnLCAnQXVkaXRTdGF0ZT1cJzFcJyBhbmQgKENVU1RPTUVSX0lEIGluIChzZWxlY3Qgb2JqZWN0X2lkIGZyb20gU1RfU1RBVElPTl9PQkpFQ1Qgd2hlcmUgU1RBVElPTl9JRCBpbiAoc2VsZWN0IHBrZXkgZnJvbSBTVF9TVEFUSU9OIHdoZXJlIGV4aXN0cyAoc2VsZWN0IDEgZnJvbSBTdF9TdGF0aW9uX1BlcnNvbl9WaWV3IGIgd2hlcmUgTG9naW5OYW1lPVwnZGVhbmxpdVwnIGFuZCBTdGF0aW9uVHlwZT1cJzJcJyBhbmQgU1RfU1RBVElPTi5Db2RlIGxpa2UgYi5TdGF0aW9uQ29kZSUyQlwnJVwnKSkpIG9yIHBrZXkgaW4gKHNlbGVjdCBvYmplY3RfaWQgZnJvbSBTVF9TVEFUSU9OX09CSkVDVCB3aGVyZSBTVEFUSU9OX0lEIGluIChzZWxlY3QgcGtleSBmcm9tIFNUX1NUQVRJT04gd2hlcmUgZXhpc3RzIChzZWxlY3QgMSBmcm9tIFN0X1N0YXRpb25fUGVyc29uX1ZpZXcgYiB3aGVyZSBMb2dpbk5hbWU9XCdkZWFubGl1XCcgYW5kIFN0YXRpb25UeXBlPVwnMVwnIGFuZCBTVF9TVEFUSU9OLkNvZGUgbGlrZSBiLlN0YXRpb25Db2RlJTJCXCclXCcpKSkpJywgZmFsc2UsICdDb2RlJywgZmFsc2UpFgICAQ8WBh8GBQPigKYfBwWpBWN0bFNob3dDb2RlRGlhbG9nKGN0bDAwX2NvbnRlbnRfdl9wcmpfd29ya2xvZ192X3Byal93b3JrbG9nX2VfUFJPSkVDVF9JRCwgJ1NBTF9QUk9KRUNULkNvZGUsTmFtZScsICdpc3MnLCAncEtleScsICcnLCAnJywgJ0F1ZGl0U3RhdGU9XCcxXCcgYW5kIChDVVNUT01FUl9JRCBpbiAoc2VsZWN0IG9iamVjdF9pZCBmcm9tIFNUX1NUQVRJT05fT0JKRUNUIHdoZXJlIFNUQVRJT05fSUQgaW4gKHNlbGVjdCBwa2V5IGZyb20gU1RfU1RBVElPTiB3aGVyZSBleGlzdHMgKHNlbGVjdCAxIGZyb20gU3RfU3RhdGlvbl9QZXJzb25fVmlldyBiIHdoZXJlIExvZ2luTmFtZT1cJ2RlYW5saXVcJyBhbmQgU3RhdGlvblR5cGU9XCcyXCcgYW5kIFNUX1NUQVRJT04uQ29kZSBsaWtlIGIuU3RhdGlvbkNvZGUlMkJcJyVcJykpKSBvciBwa2V5IGluIChzZWxlY3Qgb2JqZWN0X2lkIGZyb20gU1RfU1RBVElPTl9PQkpFQ1Qgd2hlcmUgU1RBVElPTl9JRCBpbiAoc2VsZWN0IHBrZXkgZnJvbSBTVF9TVEFUSU9OIHdoZXJlIGV4aXN0cyAoc2VsZWN0IDEgZnJvbSBTdF9TdGF0aW9uX1BlcnNvbl9WaWV3IGIgd2hlcmUgTG9naW5OYW1lPVwnZGVhbmxpdVwnIGFuZCBTdGF0aW9uVHlwZT1cJzFcJyBhbmQgU1RfU1RBVElPTi5Db2RlIGxpa2UgYi5TdGF0aW9uQ29kZSUyQlwnJVwnKSkpKScsIGZhbHNlLCAnQ29kZScsIGZhbHNlKR8IaGQCBw8PFgIfAGVkZAIIDxBkZBYBAgFkAgkPDxYCHwBlZGQCCg8PFgIfAGVkZGTFJ98c2b1wiiIn3OcDQD5Pua8yQA%3D%3D",
                    "__VIEWSTATEGENERATOR":"84FD06F3",
                    "ctl00$content$v_prj_worklog$v_prj_worklog$e_DATE":"2017-04-12%2000%3A00%3A00",
                    "ctl00$content$v_prj_worklog$v_prj_worklog$sd":"2017-4-12",
                    "ctl00$content$v_prj_worklog$v_prj_worklog$sd_time":"9%3A00",
                    "ctl00$content$v_prj_worklog$v_prj_worklog$ed":"2017-4-12",
                    "ctl00$content$v_prj_worklog$v_prj_worklog$ed_time":"18%3A00",
                    "ctl00$content$v_prj_worklog$v_prj_worklog$e_WorkType":"211",
                    "ctl00$content$v_prj_worklog$v_prj_worklog$e_Callno":"",
                    "ctl00$content$v_prj_worklog$v_prj_worklog$e_CUSTOMER_ID":"%E4%B8%AD%E5%9B%BD%E9%82%AE%E6%94%BF%E5%82%A8%E8%93%84%E9%93%B6%E8%A1%8C%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8",
                    "ctl00$content$v_prj_worklog$v_prj_worklog$e_CUSTOMER_ID_hid":"b00ad122-3d71-4431-bb0f-4a2e7aeb7754",
                    "ctl00$content$v_prj_worklog$v_prj_worklog$e_PROJECT_ID":"%E4%B8%AD%E5%9B%BD%E9%82%AE%E6%94%BF%E5%82%A8%E8%93%84%E9%93%B6%E8%A1%8C%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8-%E4%B8%AD%E5%9B%BD%E9%82%AE%E6%94%BF%E5%82%A8%E8%93%84%E9%93%B6%E8%A1%8C%E9%82%AE%E6%94%BF%E9%87%91%E8%9E%8D%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%B3%BB%E7%BB%9F%E7%A1%AC%E4%BB%B6%E8%AE%BE%E5%A4%87%E7%BB%B4%E6%8A%A4%E6%9C%8D%E5%8A%A1%E9%87%87%E8%B4%AD%E5%90%88%E5%90%8C-16-2207",
                    "ctl00$content$v_prj_worklog$v_prj_worklog$e_PROJECT_ID_hid":"99586bd0-4ffa-4863-94a5-fb16aef24a6a",
                    "ctl00$content$v_prj_worklog$v_prj_worklog$e_sqkh":"",
                    "ctl00$content$v_prj_worklog$v_prj_worklog$e_sfjb":"2",
                    "ctl00$content$v_prj_worklog$v_prj_worklog$e_ADDHOUR":"",
                    "ctl00$content$v_prj_worklog$v_prj_worklog$e_MEMO":"%E9%A9%BB%E5%9C%BA",
                    "ctl00$content$v_prj_worklog$v_prj_worklog$e5_hid":"",
                    "__EVENTTARGET":"",
                    }
        # 需要给Post数据编码
        r = requests.post(posturl, data=postdata, headers=headers)
        # time.sleep(10)
        text = r.content
        print(r.status_code)
        # print(text.decode('gb2312'))
if __name__ == '__main__':
    zb = fuckzb()
    zb.login()
    print('已连接')
    # zb.yzm_new()
    # zb.test_ph()
    zb.get_zblist()
    # zb.sub_add()
    # zb.zbadd('2017-04-13')
    # zb.zbadd('2017-04-11')
    # zb.zbadd('2017-04-10')


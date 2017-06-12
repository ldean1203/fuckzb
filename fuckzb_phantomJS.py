from selenium import webdriver
import requests
import sys
import os
driver = webdriver.PhantomJS()


class FuckZB(object):
    def __init__(self, user, pwd):
        self.user = user
        self.pwd = pwd

    def yzm(self):
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
            # 'Cookie': self.cookies,
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

    def yzm_js(self):
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

    def login(self):
        driver.get('http://58.30.224.47/platform/passport/login.aspx')
        cookie_list = driver.get_cookies()
        for cookie in cookie_list:
            driver.add_cookie(cookie)
        uid = driver.find_element_by_id('uid')
        uid.send_keys(self.user)
        pwd = driver.find_element_by_id('pwd')
        pwd.send_keys(self.pwd)
        yz = driver.find_element_by_name('ctl00$content$platform_login$validatebox_validateInputControl')
        yz.send_keys(self.yzm())
        login = driver.find_element_by_id('log')
        login.click()
        print(driver.get_cookies())
        driver.get_screenshot_as_file('login.jpg')

    def get_list(self):
        driver.get('http://erp.atitech.com.cn/iss/hr_techlog/prj_mainworklogquery_List.aspx?OBJID=389012f1-384f-447c-98ee-b2d32d0e44e9')
        print(driver.page_source)

if __name__ == '__main__':
    zb = FuckZB('deanliu', 'amber1203')
    zb.login()
    zb.get_list()

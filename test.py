# from bs4 import BeautifulSoup
# import random
# import datetime
# import math
# import time
# e = BeautifulSoup(open('1.html'), "lxml")
# # l =e.find("div", class_='x-panel-body x-panel-body-noheader x-panel-body-noborder')
# l =e.find('td',style='padding-left:6px;padding-top:2px').font.string
# #
# # for i in l:
# #     # print(i.find_all('td').value())
# #     # print(i.contents)
# #     node = [j for j in i.contents]
# #
# # all_contents = []
# # for i in l:
# #     content = []
# #     for j in range(len(i.contents)):
# #         if j == 1 and i.contents[j].input == None:
# #             break
# #         if j == 1 and i.contents[j].input != None:
# #             content.append(i.contents[j].input['value'])
# #         else:
# #             content.append(i.contents[j].string)
# #     if len(content) > 5:
# #         all_contents.append(content)
# #
# # for i in all_contents:
# #     print(i)
# #     print()
#
# # print(datetime.datetime.now().weekday())
# # print(datetime.datetime.now())
# # print(time.strftime('%Y-%m-%d',time.localtime(time.time())))
#
# a = l
# print(a)
#


import datetime
# today = datetime.date.today()
# # today = datetime.datetime.strptime("2017-06-06","%Y-%m-%d")
# sunday = today + datetime.timedelta(6 - today.weekday() + 1) - datetime.timedelta(3)
# print(sunday)
# print(today.weekday())
# s = sunday.strftime("%Y-%m-%d")
# # print(s)
# # print(type(s))
today = datetime.date.today()
for i in range(3, 7):
    sunday = today + datetime.timedelta(6 - today.weekday() + 1) - datetime.timedelta(i)
    date = sunday.strftime("%Y-%m-%d")
    print(date)
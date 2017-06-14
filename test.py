from bs4 import BeautifulSoup
import random
import datetime
import math
import time
# e = BeautifulSoup(open('1.html'))
# l =e.find_all("tr", class_='eosAjaxGridItem')
#
# for i in l:
#     # print(i.find_all('td').value())
#     # print(i.contents)
#     node = [j for j in i.contents]
#
# all_contents = []
# for i in l:
#     content = []
#     for j in range(len(i.contents)):
#         if j == 1 and i.contents[j].input == None:
#             break
#         if j == 1 and i.contents[j].input != None:
#             content.append(i.contents[j].input['value'])
#         else:
#             content.append(i.contents[j].string)
#     if len(content) > 5:
#         all_contents.append(content)
#
# for i in all_contents:
#     print(i)
#     print()

# print(datetime.datetime.now().weekday())
print(datetime.datetime.now())
print(time.strftime('%Y-%m-%d',time.localtime(time.time())))


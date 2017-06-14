from bs4 import BeautifulSoup
import random
import datetime
e = BeautifulSoup(open('1.html'))
l =e.find_all("tr", class_='eosAjaxGridItem')
#
# for i in l:
#     # print(i.find_all('td').value())
#     # print(i.contents)
#     node = [j for j in i.contents]
#
all_contents = []
# all_contents = [[i.contents[j].string for j in range(len(i.contents)) ] for i in l]
for i in l:
    for  j in range(len(i.contents)):
        if j == 1 and i.contents[j].input != None:
            all_contents.append(i.contents[j].input['value'])
        else:
            all_contents.append(i.contents[j].string)
print(all_contents)

# print(datetime.datetime.now().weekday())
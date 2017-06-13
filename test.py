from bs4 import BeautifulSoup
import random

e = BeautifulSoup(open('1.html'))
l =e.find_all("tr", class_='eosAjaxGridItem')
#
# for i in l:
#     # print(i.find_all('td').value())
#     # print(i.contents)
#     node = [j for j in i.contents]
#

all_contents = [[j.string for j in i.contents][2:-1] for i in l]
print(all_contents)
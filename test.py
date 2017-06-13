from bs4 import BeautifulSoup
import random

e = BeautifulSoup(open('1.html'))
l =e.find_all("tr", class_='eosAjaxGridItem')



print(random.randint(1000000000,9999999999))


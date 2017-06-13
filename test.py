from bs4 import BeautifulSoup


e = BeautifulSoup(open('1.html'))
l =e.find_all("tr", class_='eosAjaxGridItem')
print(l)

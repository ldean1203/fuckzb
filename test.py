from bs4 import BeautifulSoup
f = open('1.html')
e = BeautifulSoup(f, "lxml")
# l = e.find_all("tr", class_='eosAjaxGridItem')
l = e.form.get_text()

print(l)
# print(type(l))
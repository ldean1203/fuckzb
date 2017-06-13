from pyquery import PyQuery as pq

e = pq(filename='1.html')

for i in e('.eosAjaxGridItem'):
    s = [j for j in i]

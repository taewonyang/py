import urllib.request
from bs4 import BeautifulSoup
import csv

hdr = {'User-Agent' : 'Mozilla/5.0'}
url = 'https://www.melon.com/chart/index.htm'

req = urllib.request.Request(url, headers=hdr)
html = urllib.request.urlopen(req).read()
soup = BeautifulSoup(html, 'html.parser')

chart = soup.select('.lst50,.lst100')
rank = 1
melonlist =[]

for i in chart :
    temp=[]
    temp.append(rank)
    temp.append(i.select_one('.ellipsis.rank01').a.text)
    temp.append(i.select_one('.ellipsis.rank02').a.text)
    temp.append(i.select_one('.ellipsis.rank03').a.text)
    rank +=1
    melonlist.append(temp)

with open('melon100.csv', 'w', encoding='utf8', newline='') as f :
    writer = csv.writer(f)
    writer.writerow(['순위','곡명','아티스트','앨범'])
    writer.writerows(melonlist)
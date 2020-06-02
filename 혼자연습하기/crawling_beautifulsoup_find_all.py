import urllib.request as req
import urllib.parse #아스키코드로 변환시키기 위해 필요한 모듈
from bs4 import BeautifulSoup

base_url = 'https://search.naver.   com/search.naver?where=post&sm=tab_jum&query='
plus_url = input('검색어를 입력하세요 : ')
url = base_url + urllib.parse.quote_plus(plus_url) # 이부분을 통해 한글->아스키코드로 변환

html = req.urlopen(url).read()
soup = BeautifulSoup (html,'html.parser')
result = soup.find_all(class_='sh_blog_title')

for i in result :
    print(i.attrs['title']) #속성을 가져오기 위하여 -> attrs['속셩명']
    print(i.attrs['href'])
    print('')
import urllib.request as req
from bs4 import BeautifulSoup
import urllib.parse

plus_url = urllib.parse.quote_plus(input('검색어를 입력해 주세요 : '))
page_num = 1

count = 1
q = input('몇페이지를 크롤링 할까요? ')
last_page = 10 * int(q) -9

while page_num < last_page + 1:
    url = f"https://search.naver.com/search.naver?date_from=&date_option=0&date_to=&dup_remove=1&nso=&post_blogurl=&post_blogurl_without=&query=%{plus_url}&sm=tab_pge&srchby=all&st=sim&where=post&start={page_num}"
    html = req.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    blog = soup.find_all(class_='sh_blog_title')

    print(f'---{count}페이지 크롤링 결과입니다.--')
    for i in blog :
        print(i.attrs['title'])
        print(i.attrs['href'])
    print()
    page_num += 10
    count += 1
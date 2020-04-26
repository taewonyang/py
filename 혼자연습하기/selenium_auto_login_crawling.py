from selenium import webdriver
import time

driver = webdriver.Chrome()
url = 'https://www.naver.com'
driver.get(url)

driver.maximize_window()  # 1.창을 최대화 해준다.

# 2.네이버로그인
driver.find_element_by_css_selector('.ico_local_login.lang_ko').click()
time.sleep(2)
driver.find_element_by_css_selector('#id').send_keys('아이디')
time.sleep(2)
driver.find_element_by_css_selector('#pw').send_keys('비밀번호')
time.sleep(2)
driver.find_element_by_css_selector('.btn_global').click()

# 3. 크롤링
from bs4 import BeautifulSoup

driver.get('https://mail.naver.com')
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
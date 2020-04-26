from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

driver = webdriver.Chrome()
url = 'http://google.com'
driver.get(url)
driver.maximize_window() #창 크기 최대화

action = ActionChains(driver)

#네이버 검색 및 사이트 들어가기
input_box = driver.find_element_by_css_selector('.gLFyf.gsfi')
input_box.send_keys('충북과학고등학교')
input_box.send_keys(Keys.ENTER)   #'ENTER'키보드 누르기
driver.find_element_by_css_selector('.LC20lb.DKV0Md').click()

print(driver.window_handles)  # 열려있는 창 확인

#제어권 팝업창으로 전환
driver.switch_to.window(driver.window_handles[1])
driver.close()
time.sleep(2)

#제어권을 메인페이지로
driver.switch_to.window(driver.window_handles[0])

time.sleep(2)

driver.find_element_by_css_selector('#rso > div:nth-child(1) > div > div.r > a').click()
driver.find_element_by_css_selector('.usm-top-login').click()
time.sleep(1)
driver.find_element_by_css_selector('#id입력')

# alert = driver.switch_to.alert
# alert.dismiss()



# driver.quit()  창종료
import requests
import pandas as pd
from io import BytesIO
import re

api_key = '6857589812391b1d3e7094df2c034d8d08b392db'
crp_cd = '00126380' #삼성전자의 기업코드
api_url = f'https://opendart.fss.or.kr/api/list.xml?crtfc_key={api_key}&corp_code={crp_cd}&bgn_de=19990101&end_de=20200117&corp_cls=Y&page_no=1&page_count=100&pblntf_detail_ty=A001&pblntf_detail_ty=A002&pblntf_detail_ty=A003'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

#rcept_no_list 추출하기
#period_list 추출하기
res = requests.get(api_url, headers=headers)
html = res.content.decode('utf8')
rcept_no_list = re.findall('<rcept_no>(.*?)</rcept_no>', html)  #정규식표현(추출)
period_list = re.findall('<report_nm>(.*?)</report_nm>', html) #정규식표현(추출)

#dcm_no_list 추출하기
dcm_no_list = []
for rcept_no in rcept_no_list :
    view_url = f'http://dart.fss.or.kr/dsaf001/main.do?rcpNo={rcept_no}'
    res = requests.get(view_url)
    html = res.content.decode('utf8')
    dcm_no = re.findall(f"{rcept_no}', '(.*?)',", html)[0]
    dcm_no_list.append(dcm_no)


# download_excel 이란 이름의 함수를 정의하여, 자동 다운로드 하는 코드
def download_excel(period, rcept_no, dcm_no, company):
    down_url = f'http://dart.fss.or.kr/pdf/download/excel.do?rcp_no={rcept_no}&dcm_no={dcm_no}&lang=ko'
    res = requests.get(down_url, headers=headers)
    table = BytesIO(res.content)
    sheet_name = ['연결 재무상태표', '연결 손익계산서', '연결 포괄손익계산서']
    for sheet in sheet_name :
        data = pd.read_excel(table, sheet_name=sheet, skiprows=5)
        data.to_csv(period + company + sheet + '.csv', encoding='euc-kr')


for period, rcept_no, dcm_no in zip(period_list, rcept_no_list, dcm_no_list) :
    download_excel(period, rcept_no, dcm_no, '삼성전자')
import requests
import re
import folium

# part1,좌표 얻어오기(도로명주소 이용)

api_key = '340094C7-00E9-3582-9DDE-6566D6A8605C'
addr = input('도로명주소를 입력해주세요 : ')  #주소입력부분
api_url =f'http://api.vworld.kr/req/address?service=address&request=getcoord&version=2.0&crs=epsg:4326&address={addr}&refine=true&simple=false&format=json&type=ROAD&key={api_key}'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

res = requests.get(api_url, headers=headers)
html = res.content.decode('utf8')
x_code = re.findall('"x" : "(.*?)", "y', html)
y_code = re.findall('"y" : "(.*?)"}', html)


# part2.지도화 하기

latitude = x_code
longitude = y_code

# def map_view(#위도, #경도, #업체명) :
#      m = folium.Map(location=[latitude,longitude], zoom_start=12)
#      folium.Marker(location=[latitude,longitude], popup="신진다이아몬드공업',
#          icon=folium.Icon(color ="red", icon="star")).add_to(m)
#      m.save('map.html')
#
#
# for #위도, #경도, #상호명 in zip(#위도_list, #경도_list, #상호명_list) :
#      map_view()
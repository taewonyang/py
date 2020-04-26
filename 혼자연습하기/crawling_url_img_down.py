import urllib.request as req
import re
rep = req.urlopen('https://daum.net')

# print(rep.getheaders())
# print(rep.status)

data = rep.read().decode('utf8')
result = re.findall('https://[./-_\w]+.jpg', data)

for link in result:
    idx = link.rfind('/')
    with open(link[idx+1:], 'wb') as f:
        pic = req.urlopen(link)
        f.write(pic.read())
from openpyxl import load_workbook
wb = load_workbook("station.xlsx", data_only=True)
excel = wb['Sheet2']

temp=[]
for i in excel.rows :
    temp.append(i)

station = []
for row in temp :
    name = row[0].value
    station.append(name)

print(station)

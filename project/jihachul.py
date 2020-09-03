from openpyxl import load_workbook

wb = load_workbook("station.xlsx", data_only=True)
excel = wb['Sheet2']

temp = []
for i in excel.rows:
    temp.append(i)

temp1 = []
for row in temp:
    name = row[0].value
    temp1.append(name)

print('건대입구' not in temp1)

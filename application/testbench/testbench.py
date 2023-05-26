from application.core.parsers.parseCsv import parseCsv

data = open('application/assets/mockdata/test.csv', 'r')

content = data.read()

dataColumns = parseCsv(content)

print(dataColumns[0].name)
print(dataColumns[0].reference)
print(dataColumns[0].geometry)
print(dataColumns[0].point)

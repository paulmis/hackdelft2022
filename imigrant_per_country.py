import pandas as pd
import cbsodata
import re
import jsonlines
import numpy as np
import matplotlib.pyplot as plt
import datetime
import calendar

metadata = pd.DataFrame(cbsodata.get_meta('83102ENG', 'DataProperties'))
print(metadata[['Key','Title']])

data_all = []
with jsonlines.open('test123/data.jl') as reader:
    for obj in reader:
        data_all.append(obj)
         
data = [[entry['TotalAsylumRequests_1'], entry['Periods'], entry['Nationality']] for entry in data_all
     if  re.match("^(\w*) (\w*)$", entry['Periods'])
         and entry['Age'] == 'Total'
         and entry['Sex'] == 'Total male and female ']

countries = np.unique(np.asarray(([[entry['Nationality']] for entry in data_all])))

print(type(data_all))
print(countries)
months = list(calendar.month_name)

temp = [[entry[0], re.split("^(\w*) (\w*)$", entry[1])[1:3], entry[2]] for entry in data]
temp = [[entry[2], int(entry[1][0]), months.index(entry[1][1]), entry[0]] for entry in temp]
print(temp)
avg_im_month = dict()
year = dict()

for x in temp:
    if not ((x[0], x[1]) in year):
        year[(x[0], x[1])] = np.zeros(12)
    year[(x[0], x[1])][x[2]-1] = x[3]
    

for x in year:
    if np.linalg.norm(year[x]) == 0:
        print(x)
    year[x] = year[x] / np.linalg.norm(year[x])
# print(year)

sth = [(k, v) for k, v in year.items() if k[0] == 'Afghan']
# print(sth)
# xs = [x[0] for x in sth]
# ys = [x[1] for x in sth]
# plt.plot(xs, ys)
# plt.show()







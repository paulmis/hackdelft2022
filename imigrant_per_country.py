import pandas as pd
import cbsodata
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
import jsonlines
import numpy as np
import matplotlib.pyplot as plt

# Verify properties
metadata = pd.DataFrame(cbsodata.get_meta('83102ENG', 'DataProperties'))
print(metadata[['Key','Title']])

# Read data
data_all = []
with jsonlines.open('test123/data.jl') as reader:
    for obj in reader:
        data_all.append(obj)

# Filter data
data = [[entry['TotalAsylumRequests_1'], entry['Periods'], entry['Nationality']] for entry in data_all
     if  re.match("^(\w*) (\w*)$", entry['Periods'])
         and datetime.strptime(entry['Periods'], "%Y %B") >= datetime.now() - relativedelta(years = 6)
         and datetime.strptime(entry["Periods"], "%Y %B") <= datetime.now() - relativedelta(years = 1)
         and entry['Age'] == 'Total'
         and entry['Sex'] == 'Total male and female ']


temp = [[entry[0], re.split("^(\w*) (\w*)$", entry[1])[1:3], entry[2]] for entry in data]

avg_im_month = dict()

for x in temp:
    if not ((x[2], x[1][1]) in avg_im_month):
        avg_im_month[(x[2], x[1][1])] = []
    avg_im_month[(x[2], x[1][1])].append(x[0])


for x in avg_im_month:
    avg_im_month[x] = np.average(np.asarray(avg_im_month[x]))
    
    
countries = np.unique(np.asarray(([[entry['Nationality']] for entry in data_all])))
print(countries)

# Print Afghan numbers
sth = [(k[1], v) for k, v in avg_im_month.items() if k[0] == 'Afghan']
print(sth)
xs = [x[0] for x in sth]
ys = [x[1] for x in sth]
plt.plot(xs, ys)
plt.show()







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

print(countries)
months = list(calendar.month_name)

temp = [[entry[0], re.split("^(\w*) (\w*)$", entry[1])[1:3], entry[2]] for entry in data]
temp1 = [[entry[2], datetime.datetime(int(entry[1][0]), months.index(entry[1][1]), 1), entry[0]] for entry in temp]

country_name = 'Afghan'
country_data = [entry[2]for entry in temp1
         if entry[0] == country_name]
dates = [entry[1]for entry in temp1
         if entry[0] == country_name]
# print(afgan, dates)
country_series = pd.Series(data = country_data, index = dates)
# print(afgan_series)

from statsmodels.tsa.seasonal import seasonal_decompose
from dateutil.parser import parse


# Multiplicative Decomposition 
result_mul = seasonal_decompose(country_series, model='multiplicative', extrapolate_trend='freq')

# Additive Decomposition
result_add = seasonal_decompose(country_series, model='additive', extrapolate_trend='freq')

# Plot
plt.rcParams.update({'figure.figsize': (10,10)})
result_mul.plot().suptitle('Multiplicative Decompose', fontsize=22)
result_add.plot().suptitle('Additive Decompose', fontsize=22)
plt.show()
# plt.show()

from scipy import signal
detrended2 = signal.detrend(country_series.values)
plt.plot(detrended2)
plt.title('2 Detrend ' + country_name, fontsize=16)
plt.show()

d = np.arange(len(dates))
A = np.vstack([d, np.ones(len(dates))])
a, b = np.linalg.lstsq(A.T, country_data, rcond=None)[0]

plt.plot(d, country_data)
plt.plot(d, a*d + b, 'r')
plt.title("Base line")
plt.xlabel("Date")
plt.ylabel("Applications")
plt.show()

print(a)





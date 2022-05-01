from time import strptime
import pandas as pd
import cbsodata
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
import jsonlines
import numpy as np
import matplotlib.pyplot as plt

# Read data
dataset = []
with jsonlines.open('test123/data.jl') as reader:
    for pt in reader:
        dataset.append(pt)

# Filter data
# Filter dataset
data = [[entry['TotalAsylumRequests_1'], datetime.strptime(entry['Periods'], "%Y %B").strftime("%y/%m"), entry['Nationality']] for entry in dataset
     if re.match("^(\w*) (\w*)$", entry['Periods'])
         and entry['Age'] == 'Total'
         and entry['Sex'] == 'Total male and female ']

# Remove outliers
# Get requests by nationality and total requests
df = pd.DataFrame(data, columns = ['requests', 'period', 'nationality']);
req_by_nat = df.groupby(['nationality']).sum()
total = req_by_nat.loc['Total']['requests']

# Get countries that account for at least 2% of the total requests
req_by_nat = req_by_nat.loc[req_by_nat['requests'] > total / 50] 
countries = set(req_by_nat.index)

# Plot the data
# Plot the general graph
pdf = df.loc[df['nationality'].isin(countries)]
pdf = pdf.pivot(index='period',columns='nationality',values='requests')
pdf.plot.line(figsize=(16,9))
plt.ylabel("# of asylum requests")
plt.xlabel("Time")
plt.title("Asylum requests in the Netherlands  by nationality from 2013 to 2022")
plt.savefig("data/global.jpg")

# Plot individual graphs
for country in countries:
    if country != "Total":
        pdf = df.loc[df['nationality'] == country]
        pdf = pdf.pivot(index='period',columns='nationality',values='requests')
        pdf.plot.line(figsize=(10,5))
        plt.ylabel("# of asylum requests")
        plt.xlabel("Time")
        plt.title(country + " asylum requests in the Netherlands from 2013 to 2022")
        plt.savefig("data/nl-past-applications/" + country + ".jpg")
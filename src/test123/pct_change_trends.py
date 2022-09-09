import datetime
import re
import calendar
import matplotlib.pyplot as plt
import numpy
import pandas as pd
from pytrends.request import TrendReq
import seaborn as sn
import numpy as np
import math


month_to_nr = list(calendar.month_name)


def trends(gov, eng_term, lang, term, country, nationality):
    pytrends = TrendReq()
    kw_list = [term]

    # print(eng_term, lang, country)
    pytrends.build_payload(kw_list, cat=0, timeframe='2013-01-01 2022-03-31', geo=country, gprop='')
    google = pytrends.interest_over_time()[term]
    google = google.rename("searches").pct_change().rolling(7).sum()

    gov_2 = [[entry['TotalAsylumRequests_1'], entry['Periods']] for entry in gov
             if entry['Nationality'] == nationality
             and re.match("^(\w*) (\w*)$", entry['Periods'])
             and entry['Age'] == 'Total'
             and entry['Sex'] == 'Total male and female ']
    gov_3 = [[entry[0], re.split("^(\w*) (\w*)$", entry[1])[1:3]] for entry in gov_2]
    gov_4 = [[entry[0], [int(entry[1][0]), month_to_nr.index(entry[1][1])]] for entry in gov_3]
    gov_5no = [entry[0] for entry in gov_4]
    gov_5date = [(datetime.datetime(entry[1][0], entry[1][1], 1) - datetime.timedelta(days=1)).replace(day=1) for entry in gov_4]
    gov_pd = pd.Series(data=gov_5no, index=gov_5date, name='requests')
    gov_pd_change = gov_pd.pct_change().rolling(7).sum()
    
    d = np.arange(len(gov_pd))
    A = np.vstack([d, np.ones(len(gov_pd))])
    a, b = np.linalg.lstsq(A.T, gov_pd.values, rcond=None)[0]
    
    
    buildup = []
    prev = a*d[0] + b
    maxi = 0
    for (i, x) in enumerate(google.values):
        if math.isnan(prev):
            prev = 0
        curr = a * d[i] + b + x * prev
        maxi = max(maxi, curr)
        buildup.append(curr)
        prev = curr
    # arr = (a*d + np.full(d.shape, b))*(google.values+1)
    # print("the array!!!!!!!!!!!! ", buildup, google.values)
    
    plt.plot(gov_5date, gov_pd.values, label = 'CBSO data')
    plt.plot(gov_5date, buildup, 'r', label = 'predicted')
    plt.ylim(-5, maxi)
    plt.title(eng_term + " " + lang + " " + " search in " + nationality)
    plt.xlabel("Date")
    plt.ylabel("Applications")
    plt.legend()
    plt.show()
    
    

    info_string = eng_term + " " + lang + " " + " " + nationality
    
    predicted = pd.Series(data = buildup, index = gov_5date, name='predicted')

    data_all = pd.concat([predicted, gov_pd], axis=1)
    norma_all = (data_all - data_all.mean()) / data_all.std()
    # norma_all.plot().set_xlabel(info_string)
    # plt.savefig("graphs/" + info_string + ".jpg")
    # plt.close()

    return norma_all.corr().predicted.requests
import datetime
import re
import calendar
import matplotlib.pyplot as plt
import pandas as pd
from pytrends.request import TrendReq


month_to_nr = list(calendar.month_name)


def trends(gov, term, country, nationality):
    pytrends = TrendReq()
    kw_list = [term]

    pytrends.build_payload(kw_list, cat=0, timeframe='2013-01-01 2022-03-01', geo=country, gprop='')
    google = pytrends.interest_over_time()[term]
    google = google.rename("searches")

    gov_2 = [[entry['TotalAsylumRequests_1'], entry['Periods']] for entry in gov
             if entry['Nationality'] == nationality
             and re.match("^(\w*) (\w*)$", entry['Periods'])
             and entry['Age'] == 'Total'
             and entry['Sex'] == 'Total male and female ']
    gov_3 = [[entry[0], re.split("^(\w*) (\w*)$", entry[1])[1:3]] for entry in gov_2]
    gov_4 = [[entry[0], [int(entry[1][0]), month_to_nr.index(entry[1][1])]] for entry in gov_3]
    gov_5no = [entry[0] for entry in gov_4]
    gov_5date = [datetime.datetime(entry[1][0], entry[1][1], 1) for entry in gov_4]
    gov_pd = pd.Series(data=gov_5no, index=gov_5date, name='requests')

    data_all = pd.concat([google, gov_pd], axis=1)
    norma_all = (data_all - data_all.mean()) / data_all.std()
    norma_all.plot()
    plt.show()

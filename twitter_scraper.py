import requests
import os
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

bearer_token = os.environ.get("BEARER_TOKEN")

search_url = "https://api.twitter.com/2/tweets/counts/recent"

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FullArchiveTweetCountsPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", search_url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def make_plot(name, dates, number_of_tweets, a, b):
    plt.plot(dates, number_of_tweets, 'o')
    plt.plot(dates, a*dates + b, 'r')
    plt.title(name)
    plt.xlabel("Date")
    plt.ylabel("# of #war")
    plt.savefig(name + ".png")
    plt.close()


def get_data():

    result = {}
    data = pd.read_csv('./data/countries.csv')
    for country in data['country']:
        query_string = "#war #" + country
        query_params = {
        'query': query_string,
        'granularity': 'hour'
        }
        json_response = connect_to_endpoint(search_url, query_params) 
        #print(json.dumps(json_response, indent=4, sort_keys=True))

        number_of_tweets = []
        dates = []
        parsed_json = json.loads(json.dumps(json_response, indent=4, sort_keys=True))
        for lol in parsed_json['data']:
            parsed_lol = json.loads(json.dumps(lol, indent=4, sort_keys=True))
            number_of_tweets.append(parsed_lol['tweet_count'])
            dates.append(parsed_lol['start'][8:13])

        #make_plot(country, dates, number_of_tweets)
        result.update({country: number_of_tweets})

    return result, dates    

def main():
    twitter_data, dates = get_data()
    result = {}
    data = pd.read_csv('./data/countries.csv')
    dates_array = np.arange(0, len(dates))

    for country in data['country']:
        array = np.asarray(twitter_data[country])
        A = np.vstack([dates_array, np.ones(len(dates))])
        # a represnets steepnes of the linear aproximation of number of tweets 
        # therefore represents a trend that we could use to add to exisiting data
        a, b = np.linalg.lstsq(A.T, array, rcond=None)[0]
        #make_plot(country, dates_array, twitter_data[country], a, b)
    

if __name__ == "__main__":
    main()
import requests
import os
import json
import matplotlib.pyplot as plt
import pandas as pd

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
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def make_plot(name, dates, number_of_tweets):
    plt.plot(dates, number_of_tweets)
    plt.title(name)
    plt.xlabel("Date")
    plt.ylabel("# of #war")
    plt.savefig(name + ".png")
    plt.close()


def main():

    data = pd.read_csv('./data/countries.csv')
    for country in data['country']:
        query_string = "#war #" + country
        query_params = {
        'query': query_string,
        'granularity': 'day'
        }
        print(country) 
        json_response = connect_to_endpoint(search_url, query_params) 
        #print(json.dumps(json_response, indent=4, sort_keys=True))

        number_of_tweets = []
        dates = []
        parsed_json = json.loads(json.dumps(json_response, indent=4, sort_keys=True))
        for lol in parsed_json['data']:
            parsed_lol = json.loads(json.dumps(lol, indent=4, sort_keys=True))
            number_of_tweets.append(parsed_lol['tweet_count'])
            dates.append(parsed_lol['start'][5:10])

        make_plot(country, dates, number_of_tweets)
        

if __name__ == "__main__":
    main()
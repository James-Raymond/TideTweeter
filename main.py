import json
import time
import requests
from bs4 import BeautifulSoup
import json
from dotenv import load_dotenv
import os
from datetime import datetime
import tweepy
from pprint import pprint as pprint
from keys import *

def get_times(url):
    """

    function to get the tide data from the locations file

    """
    # print('Getting Times')
    # blank list to store details
    location_details=[]

    # get the webpage
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    # page_contents = soup.contents
    content = soup.find('table', 'tide-day-tides')

    # for data in content:
    child = list(content.children)
    for items in child:
        location_details.append(items.get_text())
    return location_details

def extract_details(details_list):

    """

    This function normalises the data from what was returned 
    from the get_times function
    
    """

    # print("extract details")
    details = {}
    
 
     # we dont need " def get_times(url,title)" so just delete it
    del details_list[0]

    for item in details_list:

        items = {} 

        #split on spaces 
        list_of_splits = item.split(' ')
        try:
            # clean up the data in this split
            cleanup_am_or_pm = list_of_splits[3]
            am_or_pm = cleanup_am_or_pm.split('(')
            cleanup_height = list_of_splits[5]
            # add the data to a key value pairs
            pprint(list_of_splits)
            print(cleanup_height)
            items['height'] = cleanup_height.split(')')[1]
            time = convert24((f'{list_of_splits[2]}{am_or_pm[0]}'))
            items['time'] = time
            items['high_or_low'] = list_of_splits[0] 
        except(IndexError):
            tide_split = list_of_splits[1].split('Tide')
            # clean up the data in this split
            cleanup_am_or_pm = list_of_splits[2]
            am_or_pm = cleanup_am_or_pm.split('(')
            cleanup_height = list_of_splits[4]

            # add the data to a key value pairs
            pprint(tide_split)

            items['height'] = cleanup_height.split(')')[1]
            time = convert24((f'{tide_split[1]}{am_or_pm[0]}'))
            items['time'] = time
            items['high_or_low'] = list_of_splits[0] 


        details[f'tide{details_list.index(item)}'] = items

    return details

def organise_data(urls_list):
    tide_times = {}

    for locations in urls_list:
        for items in urls_list[locations]:
            try:
                time = urls_list[locations][items]['time']
                tide_times [time] = {}
                tide_times [time]['height'] = urls_list[locations][items]['height']
                tide_times [time]['high_or_low'] = urls_list[locations][items]['high_or_low']
                tide_times [time]['location'] = locations
                tide_times [time]['title'] = urls_list[locations]['title']
            except:
                pass

    return(tide_times)

def convert24(time):
    # Parse the time string into a datetime object
    try:
        t = datetime.strptime(time, '%I:%M%p')

    except(ValueError):
        # does not like 00:00 - 00:59 so this had to fixed

        t =  datetime.strptime(time.split('AM')[0], '%H:%M')

    # Format the datetime object into a 24-hour time string
    return t.strftime('%H:%M')

def write_to_file(data):
    with open('./tide_time_details.json', 'w+') as data_file:
        data_file.write(json.dumps(data))

def check_times():
    with open('./tide_time_details.json','r') as file:
        times_file = json.load(file)
        file.close()

    for times in times_file:
        now = datetime.now()
        current_time = now.strftime("%H:%M")

        if times == current_time:
            #print( f'Sending Tweet for {times_file[times]}')
            tweet_tides(times_file[times])


def tweet_tides(data):

    tweet = (
        f"{data['title']}\nIt is currently {data['high_or_low']} tide in {data['location']}.\n"
        f"It is {data['height']} meter tide\n #irishtides #tidetimes #{data['location']}tide "
        )
    print(tweet)

    client = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret,
    access_token=access_token, access_token_secret=access_token_secret)
    # update the status
    print(client.create_tweet(text = tweet))
        
def run_get_tides():

    tide_information = []
    with open('./tidelocations', 'r') as f:
        urls_list = json.load(f)
        f.close()
    with open('tidetimes.json', 'w+') as f:
        f.close()

    # run for each tide location
    for urls in urls_list:
        tide_details = get_times(urls_list[urls]['url'])
        print(urls)
        pprint(tide_details)
        details = extract_details(tide_details)

        # add the details extracted eg time, hight etc to the url list
        for detail in details:

            urls_list[urls][detail] = details[detail]

    # convert the data to a dict where the key is the time
    write_to_file(organise_data(urls_list))

if __name__ == "__main__":
    while(1):
        print('get tide info')
        run_get_tides()
        while (datetime.now().strftime("%H:%M") != '00:00'):
            print('checking time')
            check_times()
            time.sleep(60)
    """
extract the data using the time as the key,
sort the list
when the time matches tweet and once theres a 200 returned or equivelent delte the row. 
then at 00:00 run the program again


    """
import json
import requests
from bs4 import BeautifulSoup
import json
from dotenv import load_dotenv
import os
import datetime
from pprint import pprint as pprint

def get_times(url):
    print('Getting Times')
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

    print("extract details")
    details = {}
    
 
     # we dont need " def get_times(url,title)" so just delete it
    del details_list[0]

    for item in details_list:
        height = {}
        time = {}
        high_or_low = {}

        #split on spaces 
        list_of_splits = item.split(' ')
        # clean up the data in this split
        cleanup_am_or_pm = list_of_splits[3]
        am_or_pm = cleanup_am_or_pm.split('(')
        cleanup_height = list_of_splits[5]

        height['height'] = cleanup_height.split(')')[1]
        time['time'] = ((f'{list_of_splits[2]}{am_or_pm[0]}'))
        high_or_low['high_or_low'] = list_of_splits[0] 

        details[f'tide{details_list.index(item)}'] = (height, time, high_or_low)

    return details

if __name__ == "__main__":
    tide_information = []
    with open('./tidelocations', 'r') as f:
        urls_list = json.load(f)
        f.close()
    with open('tidetimes.txt', 'w+') as f:
        f.close()

    for urls in urls_list:
        tide_details = get_times(urls_list[urls]['url'])
        details = extract_details(tide_details)

        for detail in details:

            urls_list[urls][detail] = details[detail]

        pprint(urls_list)
        

        break;


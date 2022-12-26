import json
import requests
from bs4 import BeautifulSoup
import json
from dotenv import load_dotenv
import os
import datetime

def get_times(url,title):
	print('Getting Times')
	# blank list to store details
	location_details=[]

	# get the webpage
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	print(title)
	# page_contents = soup.contents
	content = soup.find('table', 'tide-day-tides')

	# for data in content:
	child = list(content.children)
	for items in child:
		location_details.append(items.get_text())
	return location_details

def sort_times(details_list):
	details=[]
	print("Sorting Times")

	 # we dont need " def get_times(url,title)" so just delete it
	del details_list[0]

	for item in details_list:

		#split on spaces 
		list_of_splits = item.split(' ')
		# clean up the data in this split
		cleanup_am_or_pm = list_of_splits[3]
		am_or_pm = cleanup_am_or_pm.split('(')

		details.append(str(f'{list_of_splits[2]}{am_or_pm[0]}'))

	return details

if __name__ == "__main__":
	with open('./tidelocations', 'r') as f:
		urls_list = json.load(f)
		f.close()
	with open('tidetimes.txt', 'w+') as f:
		f.close()

	for urls in urls_list:
		detials = get_times(urls_list[urls]['url'],urls_list[urls]['title'])
		print(detials)
		times = sort_times(detials)


		break;


import requests
import json
from bs4 import BeautifulSoup

from slimit import ast
from slimit.parser import Parser
from slimit.visitors import nodevisitor

import time

def get_data(url):
	# Structure results
	result = dict()
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate, br"}
	page = requests.get(url, headers=headers)
	soup = BeautifulSoup(page.content, 'html.parser')

	# Get milage (hard one)
	script = str(soup.find_all("script", {"type": "text/javascript"})[4])
	bracket_count = 0
	started = False
	json_string = ""
	for char in script:
		if (char == '{'):
			if not started:
				if bracket_count == 1:
					started = True
			bracket_count += 1
		elif (char == '}'):
			if started:
				bracket_count -= 1
		if (char == ";"):
			if (bracket_count == 1 and started):
				break
		if (started):
			json_string += char

	json_detailed = json.loads(json_string)
	result["raw"] = json_detailed
	json_hero = json_detailed["hero"]
	result["mileage"] = json_hero["mileage"]
	result["make"] = json_hero["make"]
	result["model"] = json_hero["model"]
	result["year"] = json_hero["year"]
	result["price"] = json_hero["price"]
	result["location"] = json_hero["location"]

	# Get ad description
	result["description"] = str(soup.find("meta", {"property": "og:description"})["content"])
	return result






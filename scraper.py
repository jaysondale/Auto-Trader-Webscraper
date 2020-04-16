
import requests
from lxml import html
import time
import math
import json
from bs4 import BeautifulSoup

from slimit import ast
from slimit.parser import Parser
from slimit.visitors import nodevisitor

def scraper(url):
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
			bracket_count -= 1
		if (char == ";"):
			if (bracket_count == 1 and started):
				break
		if (started):
			json_string += char

	json_detailed = json.loads(json_string)
	result["mileage"] = json_detailed["hero"]["mileage"]

	# Get ad description
	result["description"] = str(soup.find("meta", {"property": "og:description"})["content"])

	# Get other ad details
	ad_id_tag = soup.find("div", {"class": "container container-main"})
	ad_id = ad_id_tag["data-fdmid"]
	base_url = "https://payments.autotrader.ca/Payment/PaymentOptionsSettings/?adId="

	data_url = base_url + str(ad_id) + "&lang=en"
	data_page = requests.get(data_url, headers=headers)
	data_soup = BeautifulSoup(data_page.content, 'html.parser')
	json_content = json.loads(data_page.content.decode('utf-8'))
	
	result["raw"] = json_content
	result["make"] = json_content["adMake"]
	result["model"] = json_content["adModel"]
	result["year"] = json_content["adTitleYMM"][:4]
	result["price"] = json_content["dealerPrice"]
	result["salesTax"] = json_content["salesTax"]
	result["isUsed"] = json_content["isUsed"]
	return result



content = scraper("https://www.autotrader.ca/a/ferrari/488%20spider/thornhill/ontario/5_48038210_on20090112102238078?showcpo=ShowCpo&ncse=no&ursrc=hl&orup=1_10_10&pc=M5N%202R2&sprx=100")
print("You searched for a " + content["year"] + " " + content["make"] + " " + content["model"] + " with " + content["mileage"])
print(content["isUsed"])









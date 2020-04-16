
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
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate, br"}
	page = requests.get(url, headers=headers)
	soup = BeautifulSoup(page.content, 'html.parser')
	scripts = soup.find_all("script")
	for script in range(len(scripts)):
		print("SCRIPT " + str(script) + ": " + str(scripts[script]))


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate, br"}
page = requests.get("https://www.autotrader.ca/a/chevrolet/cruze/bolton/ontario/5_46060815_20111011113201778?showcpo=ShowCpo&ncse=no&ursrc=ts&pc=M5N%202R2&sprx=100", headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
ad_id_tag = soup.find("div", {"class": "container container-main"})
ad_id = ad_id_tag["data-fdmid"]
base_url = "https://payments.autotrader.ca/Payment/PaymentOptionsSettings/?adId="

data_url = base_url + str(ad_id) + "&lang=en"
data_page = requests.get(data_url, headers=headers)
data_soup = BeautifulSoup(data_page.content, 'html.parser')
# print(data_soup)
json_content = json.loads(data_page.content.decode('utf-8'))
print(json_content)



#print(scraper("https://www.autotrader.ca/a/porsche/911/mississauga/ontario/5_47435092_on20090105094745219?showcpo=ShowCpo&ncse=no&ursrc=ppl&pc=M5N%202R2&sprx=50"))









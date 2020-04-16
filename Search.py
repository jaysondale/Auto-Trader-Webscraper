from Scraper import get_data
from bs4 import BeautifulSoup

import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate, br"}
url = "https://www.autotrader.ca/cars/bmw/3%20series/on/toronto/?rcp=100&rcs=0&srt=9&prx=250&prv=Ontario&loc=M5N%202R2&hprc=True&wcp=True&sts=New-Used&inMarket=advancedSearch"
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, "html.parser")
listings = soup.find_all("a", {"class": "result-title click"})
listing_urls = [listing["href"] for listing in listings]

base_url = "https://www.autotrader.ca"

for url in listing_urls:
	full_url = base_url + url
	result = get_data(full_url)
	print(result["year"] + " " + result["make"] + " " + result["model"] + " with " + result["mileage"] + " located in " + result["location"])
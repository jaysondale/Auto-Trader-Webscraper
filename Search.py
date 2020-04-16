from Scraper import get_data
from bs4 import BeautifulSoup
import string

import requests

# Parameters
make = "mazda"
model = "cx-5"
province = "on"
city = "london"
radius = "100"
num_results = "100"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate, br"}
url = f"https://www.autotrader.ca/cars/{make}/{model}/{province}/{city}/?rcp={num_results}&rcs=0&srt=9&prx={radius}&hprc=True&wcp=True&sts=New-Used&inMarket=advancedSearch"
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, "html.parser")
listings = soup.find_all("a", {"class": "result-title click"})
listing_urls = [listing["href"] for listing in listings]

base_url = "https://www.autotrader.ca"

results = []
avg_price = 0
avg_mileage = 0
avg_year = 0

print("Found Listings:")
for url in listing_urls:
	full_url = base_url + url
	try:
		result = get_data(full_url)
		results.append({"url": full_url, "data": result})
		avg_price += int(result["price"].replace("$", "").replace(",", ""))
		avg_mileage += int(result["mileage"].strip(string.ascii_letters).replace(",", ""))
		avg_year += int(result["year"].replace(",", ""))
		print(result["year"] + " " + result["make"] + " " + result["model"] + " with " + result["mileage"] + " located in " + result["location"])
	except:
		print("ERROR: " + full_url)

avg_mileage /= len(results)
avg_price /= len(results)
avg_year /= len(results)

# Find the best deal
best_result = {"score": 0, "result": None}
for result in results:
	# Determine score
	data = result["data"]
	mileage_delta_frac = (avg_mileage - int(data["mileage"].strip(string.ascii_letters).replace(",", "")))/avg_mileage
	price_delta_frac = (avg_price - int(data["price"].replace("$", "").replace(",", "")))/avg_price
	year_delta_frac = (int(data["year"].replace(",", "")) - avg_year)/avg_year

	score = year_delta_frac*mileage_delta_frac*price_delta_frac
	if score > best_result["score"]:
		best_result["result"] = result

data = best_result["result"]["data"]
print("****RESULTS****")
print(f"Based on {str(len(results))} listings. Average year: {str(avg_year)}, Average price: {str(avg_price)}, Average mileage: {str(avg_mileage)}")
print("The best deal is a " + data["year"] + " " + data["make"] + " " + data["model"] + " with " + data["mileage"] + " located in " + data["location"] + " for $" + data["price"])
print(best_result["result"]["url"])


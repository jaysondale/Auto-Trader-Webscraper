# Auto-Trader-Webscraper
The goal of this project is to scrape Autotrader.ca for listing data and compile a list of the best deals available.
## Ranking System
The system ranks listings based on the following formula:
```
vehicle_score = (mileage/average_mileage) * (price/average_price) * ((year-average_year)/average_year)
```
The highest scored vehicle is recommended.

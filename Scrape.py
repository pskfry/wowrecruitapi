from datetime import datetime
import requests
import json

class Scrape:
    def __init__(self, start_time):
        self.scrape_start = datetime.now()
        self.scrape_end = None
        self.char_count = 0
        self.min_ilvl = 0.0
        self.pages_scraped = 0

    @classmethod
    def post_to_api(self, url, headers):
        headers = {"Content-Type": "application/json"}
        scrape_json = json.dumps(self.__dict__,default=str)

        return requests.post(url=url+"/scrapelog", json=scrape_json, headers=headers)

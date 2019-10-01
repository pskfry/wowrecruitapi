from datetime import datetime
import requests
from urllib.error import HTTPError
import json
import re
from dateutil.parser import parse

class Scrape:
    def __init__(self, start_time):
        self.scrape_start = datetime.now()
        self.scrape_end = None
        self.char_count = 0
        self.min_ilvl = 0.0
        self.pages_scraped = 0

    def post_to_api(self, url, headers):
        try:
            scrape_json = json.dumps(vars(self),default=str)

            resp = requests.post(url=url+"/scrapelog", data=scrape_json, headers=headers)
            resp.raise_for_status()

        except HTTPError as http_err:
            print(f'Http error occurred on scrapelog post: {http_err}')
            return

        except Exception as err:
            print(f'Other error occurred on scrapelog post: {err}')
            return
        
        else:
            return resp



class ScrapedChar:
    def __init__(self, tds):
        for id, td in enumerate(tds):
            if id == 0:
                # parse name column
                p = re.compile(r'<td.*?a[^>]*character (?P<CLASS>[^"]*)')
                m = p.search(repr(td))
                self.char_class = m.group('CLASS')
                p = re.compile(r'<td.*?a[^>]*>(?P<NAME>[^<]*)')
                m = p.search(repr(td))
                self.char_name = m.group('NAME')
            if id == 1:
                # parse guild column
                p = re.compile(r'<td.*?a[^>]*&lt;(?P<GUILD>[A-z ]*)&')
                m = p.search(repr(td))
                if m:
                    self.guild = m.group('GUILD')
                else:
                    self.guild = ''
            if id == 3:
                # parse realm column
                p = re.compile(r'<td.*?a[^>]*>(?P<SERVER>[^<]*)')
                m = p.search(repr(td))
                if m:
                    self.realm_name = m.group('SERVER')
                else:
                    self.realm_name = ''
            if id == 4:
                # parse ilvl column
                p = re.compile(r'<td[^>]*>(?P<ILVL>[^<]*)')
                m = p.search(repr(td))
                if m:
                    self.item_level = float(m.group('ILVL'))
                else:
                    self.item_level = ''
            if id == 5:
                # parse last updated column
                p = re.compile(
                    r'<td[^>].*?<span[^>]*label="(?P<LASTUPDATED>[^"]*)')
                m = p.search(repr(td))
                if m:
                    last_update = m.group('LASTUPDATED')
                    last_update_pydate = parse(last_update)
                    self.last_update = last_update_pydate.strftime(
                        "%m-%d-%Y %H:%M:%S")
                else:
                    self.last_update = ''

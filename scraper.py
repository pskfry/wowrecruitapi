import requests
import urllib.request
from urllib.error import HTTPError
import time
import os
import re
import json
from scrapermodels import ScrapedChar, Scrape
from datetime import datetime
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from dateutil.parser import parse

def cut_the_bull(page_text):
    table_start = page_text.find(r'<table class="rating')
    rows_start = page_text.find(r'<td', table_start)-10
    table_end = page_text.find(r'</table>', rows_start)
    table_data = page_text[rows_start: table_end]

    return table_data

def get_next_url(page_text):
    table_start = page_text.find(r'class="prevNextTable"')
    table_end = page_text.find(r'</div>', table_start)
    table_text = page_text[table_start: table_end]

    p = re.compile('.*?<a[^>]*class="navNext[^>]*href="(?P<NEXTPAGEURL>[^"]*)')
    m = p.search(table_text)

    if m:
        return "http://wowprogress.com%s" % (m.group('NEXTPAGEURL'))
    else:
        return False

def get_tds_from_row(row_text):
    row_soup = BeautifulSoup(row_text, 'html.parser')
    first_field = row_soup.find('td')
    fields = []
    fields.append(first_field)

    for field in row_soup.find('td').next_siblings:
        fields.append(field)

    return fields

def scrape():
    new_scrape = Scrape(datetime.now())
    new_scrape.min_ilvl = 450.0

    min_item_level_found = False
    no_next_url = False

    char_list = []
    next_url = 'https://www.wowprogress.com/gearscore/us?lfg=1'
    pages_scraped = 0

    print("New scrape started @ %s" % datetime.now())

    while not min_item_level_found and not no_next_url:
        # get the html data
        print("Scraping page: %s" % next_url)
        response = requests.get(next_url)
        page_text = response.text

        # cut out the character list table
        table_data = cut_the_bull(page_text)

        # get the next page url
        next_url = get_next_url(page_text)

        # create the soup
        soup = BeautifulSoup(table_data, 'html.parser')

        pre_page_list_length = len(char_list)

        # loop through the rows
        for row in soup.find_all('tr'):
            tds = get_tds_from_row(repr(row))

            # create a char for each row
            new_char = ScrapedChar(tds)

            # add it to the char list
            char_list.append(new_char)

        post_page_list_length = len(char_list)
        list_len_delta = post_page_list_length - pre_page_list_length

        print("Found %s characters on page" % list_len_delta)

        if new_char.item_level < new_scrape.min_ilvl:
            min_item_level_found = True

        if not next_url:
            no_next_url = True

        pages_scraped += 1

        # wait 2 seconds before sending another get request
        # we're nice here
        time.sleep(2)

    print("Scrape end @ %s" % datetime.now())
    print("%s pages scraped" % pages_scraped)

    # build new chars json for api request
    add_chars_json = {'char_list': []}
    add_chars_json['char_list'].extend([char.__dict__ for char in char_list])

    # set api url
    api_url = os.environ.get("API_URL")

    # get api login pw from env vars
    username = os.environ.get("SCRAPER_USERNAME")
    password = os.environ.get("SCRAPER_PASSWORD")
    login = {"user_name": username, "password": password}
    login_json = json.dumps(login)
    print(api_url)

    # get token
    try:
        headers = {"Content-Type": "application/json"}
        resp = requests.post(url=api_url+"/login", data=login_json, headers=headers)

        response.raise_for_status()

    except HTTPError as http_err:
        print(f'Http error occurred on login: {http_err}')
        return

    except Exception as err:
        print(f'Other error occurred on login: {err}')
        return

    else:
        resp_data = resp.json()
        jwt_token = resp_data["access_token"]

    new_scrape.pages_scraped = pages_scraped
    new_scrape.scrape_end = datetime.now()
    new_scrape.char_count = len(char_list)

    # add token to headers
    headers['Authorization'] = 'Bearer ' + jwt_token

    # try post chars
    try:
        resp = requests.post(url=api_url+"/char", data=add_chars_json, headers=headers)
        resp.raise_for_status()

    except HTTPError as http_err:
        print(f'Http error occurred on chars post: {http_err}')

    except Exception as err:
        print(f'Other error occurred on chars post: {err}')

    resp = new_scrape.post_to_api(url=api_url, headers=headers)
    print("New scrape post response: %s" % resp.status_code)

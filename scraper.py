import itertools
from functools import partial

import requests
from bs4 import BeautifulSoup

from bulk_utils import write_to_csv
from parallel_processing import ioBoundMap


def get_text_from_element(element):
  if element is not None:
    return element.text

def get_attributed_from_app_card(app_card_element):
    link = app_card_element["data-target-href"]
    name = get_text_from_element(app_card_element.find("h4",{"class":"ui-app-card__name"}))
    by_line = get_text_from_element(app_card_element.find("div",{"class":"ui-app-card__by-line"}))
    price_line = get_text_from_element(app_card_element.find("div",{"class":"ui-app-pricing"}))
    details = get_text_from_element(app_card_element.find("p",{"class":"ui-app-card__details"}))
    rating = get_text_from_element(app_card_element.find("div",{"class":"ui-star-rating"}))
    return {"name":name,"by_line":by_line,"price_line":price_line,"details":details,"rating":rating,"link":link}


def get_html_for_each_app(soup:BeautifulSoup):
    elements = soup.find_all("div",{"class":"ui-app-card"})
    return list(map(get_attributed_from_app_card,elements))



def get_shopify_apps(url):
    html_response = requests.get(url)
    soup = BeautifulSoup(html_response.content, 'html.parser')
    return soup

def get_data_for_page(url,page):
    print(f"crawling page {url.format(page)}")
    try:
      soup = get_shopify_apps(url.format(page))
      data = get_html_for_each_app(soup)
    except:
      print(f"failed for {page}")
      data = []
    return data

def get_for_pages(url,num_pages):
    mlist = []
    for page in range(1,num_pages):
      print(f"crawling page {url.format(page)}")
      try:
        soup = get_shopify_apps(url.format(page))
        data = get_html_for_each_app(soup)
      except:
        print(f"failed for {page}")
        data = []
      mlist.append(data)
    return list(itertools.chain(*mlist))

def get_category(url):
    html_response = requests.get(url)
    soup = BeautifulSoup(html_response.content, 'html.parser')
    element = soup.find("div",{"class":"heading--5"})
    return element.text

def enrich_with_category(data):
    print(f"fetching category for {data['link']}")
    try:
      data.update({"category": get_category(data["link"])})
    except:
      data.update({"category": "not_found"})
    return data

def create_csv_for_search_term(search_term,num_pages):
    url = f"https://apps.shopify.com/search?q={search_term}&page={{}}"
    # data = get_for_pages("https://apps.shopify.com/search?q=product&page={}",154)
    list_data = ioBoundMap(partial(get_data_for_page, url), range(1, num_pages))
    datas = list(itertools.chain(*list_data))
    enriched_data = ioBoundMap(enrich_with_category, datas)
    write_to_csv(enriched_data, enriched_data[0].keys())


if __name__ == '__main__':
  create_csv_for_search_term("product",156)

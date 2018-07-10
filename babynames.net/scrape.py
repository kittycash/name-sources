#!/usr/bin/python3

import sys
from bs4 import BeautifulSoup
from time import sleep
import requests
import urllib.parse
import json

def make_name_handler(original_url, output_filename):
    f = open(output_filename, 'w')
    def handle(name_info):
        f.write("insert into names values(%(alphabet)s, %(source)s, %(name)s, false);\n" % {
                'name': json.dumps(name_info['name']),
                'source': json.dumps(original_url),
                'alphabet': json.dumps("Chinese")
            })
        f.flush()
    return handle

def get_html(url=None):
    result = requests.get(url)
    if result.status_code != 200:
        raise Exception("Failed to fetch URL: %(url)s", {'url': url})
    return result.text

def get_page_number(url):
    parsed = urllib.parse.urlparse(url)
    parts = urllib.parse.parse_qs(parsed.query)

    if 'page' in parts:
        return int(parts['page'][0])

    return 1

def url_with_page_number(url, num):
    parsed = urllib.parse.urlparse(url)
    return urllib.parse.urlunparse(
        (parsed[0],
         parsed[1],
         parsed[2],
         parsed[3],
         'page=%(page)d' % {'page': num},
         parsed[5]))

def soup_page_numbers(soup):
    pagination_links = soup.find_all('section', 'pagination')[0].find_all('a')
    def link_page_number(link):
        return get_page_number(link.attrs['href'])
    return map(link_page_number, pagination_links)

def soup_names(soup):
    names = soup.find_all('span', 'result-name')
    def get_name(item):
        gender_span = item.parent.find_all('span', 'result-gender')
        gender = None
        if len(gender_span) > 0 and 'class' in gender_span[0].attrs and 'boy' in gender_span[0].attrs['class']:
            gender = 'male'
        if len(gender_span) > 0 and 'class' in gender_span[0].attrs and 'girl' in gender_span[0].attrs['class']:
            gender = 'female'
        return {
            'name': item.text,
            'gender': gender
        }
    return map(get_name, names)

def scrape_onward(url=None, name_handler=None, sleep_sec=0.3):

    print("scanning url: %(url)s" % {'url': url})

    current_page_num = get_page_number(url)

    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')

    for name in soup_names(soup):
        name_handler(name)

    if (current_page_num + 1) in soup_page_numbers(soup):
        sleep(sleep_sec)
        scrape_onward(
            url=url_with_page_number(url, (current_page_num + 1)),
            name_handler=name_handler, sleep_sec=sleep_sec)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Bad args")
        print("")
        print("Usage: %(base)s base_url start_url output_file" % {
            'base': sys.argv[0]
        })
        exit(1)
    prog_name, base_url, start_url, output_filename = sys.argv
    scrape_onward(
        start_url,
        name_handler = make_name_handler(base_url, output_filename)
    )


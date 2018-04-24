##
## Author: Randy Burrell
##
## Date: Fri Apr 20 16:45:34 EST 2018
##
## Description:
##
##
##

from bs4 import BeautifulSoup
from time import sleep
import requests

def scraper(url=None, params=None, element=None, attrs=None, sleep_sec=0.3):
    if url is None or element is None or attrs is None:
        print('All function parameters are required')
        return None
    elif type(url) is not str or type(element) is not str or type(attrs) is not dict:
        print('Usage url and element must be type string and attrs must be type dict')
        return None

    html = get_html(url, params)
    soup = BeautifulSoup(html, 'html.parser')
    sleep(sleep_sec)
    return soup.find_all(element, attrs)

def get_html(url=None, params=None):
    if url is None or params is None:
        print('Usage: get_html(url, params={})')
        return None
    result = requests.get(url, params)
    if result.status_code != 200:
        print('Status code was {} for url {}?page={}'.format(result.status_code, url, params['page']))
        return None
    return result.text

def main(start=1, stop=724, url = 'http://babynames.net/names', element = 'ul'):
    names   = []
    for i in range(start, stop):
        names += scraper(url=url, params={'page': i}, element=element, attrs={'class': 'names-results'})
    return names

if __name__ == '__main__':
    main(10, 20)


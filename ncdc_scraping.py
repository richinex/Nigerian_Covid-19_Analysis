# function to scrape data and parse into a Pandas DataFrame
from bs4 import BeautifulSoup
from collections import defaultdict
import matplotlib.pyplot as plt
import requests
import pandas as pd
import re

url = 'https://covid19.ncdc.gov.ng/'
def parse_ncdc(url):
    country_list = []
    record = defaultdict(list)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find_all('table', class_ = 'table table-responsive')
    for tr in table:
        states = tr('p')
        for item in states:
            country_list.append(item.text)
    pattern = re.compile(r'(\w+).(\d+).(\d+).(\d+).(\d+)')
    cases = pattern.findall(' '.join(country_list))
    for i in range(0, len(cases)-1):
        record['states_affected'].append(str(cases[i][0]))
        record['lab_confirmed_cases'].append(int(cases[i][1]))
        record['active_cases'].append(int(cases[i][2]))
        record['discharged'].append(int(cases[i][3]))
        record['deaths'].append(int(cases[i][4]))
    return pd.DataFrame.from_dict(record)
    

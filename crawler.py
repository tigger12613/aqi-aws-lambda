import requests
import time
from bs4 import BeautifulSoup
import os
import re
import urllib.request
import json

import datetime
from datetime import timedelta

#擷取網站
def get_web_page(url):    
    resp = requests.get(
        url=url,
        #cookies={'over18': '1'}
    )
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text

def get_data():
    url="http://opendata.epa.gov.tw/webapi/Data/REWIQA/?$orderby=SiteName&$skip=0&$top=1000&format=json"
    page=get_web_page(url)
    return json.loads(page)
def get_data_index(r):
    index={}
    for i in range(len(r)):
        index[r[i]["SiteName"]]=i
    return index

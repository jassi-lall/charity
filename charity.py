import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from time import sleep
import random

def crawl_delay():
    sleep(1 + random.uniform(0,1))
    return None

def scrape_page(page_no):
    """
    scrape_page(page_no) -> DataFrame

    Throws exception for empty/non-existant page

    Organisation example:

    {
    'ID': '693',
    'organizationName': '100 Black Men of Middle Tennessee',
    'category': 'Youth Development',
    'additionalOrgDonateCondition': True,
    'donateLink': 'index.php?section=organizations&action=newDonation_org&fwID=693',
    'viewLink': 'the100BlackMenMiddleTN',
    'missionStatement': 'To nurture and enhance the growth, development and opportunities for young Black males of Middle Tennessee.',
    'region': False,
    'logo': 'https://ddb9l06w3jzip.cloudfront.net/uploadedFiles/giving_cfmt/organizations/logo/693?thumbnail=1&maxWidth=290&maxHeight=164'
    }
    """

    url = f'https://givingmatters.civicore.com/nonprofits?page={page_no}'
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')

    # Find the script that contains organisations in JSON format
    scripts = soup.find_all('script')
    script = scripts[-4]
    script = script.decode_contents().strip()

    # Remove parts of the script we don't need to be left with just the JSON data
    start_index = script.find('"orgResults":') + len('"orgResults":')
    end_index = script.rfind('"resultsCount":') - 1
    script = script[start_index : end_index]

    # Parse data into a list of organisations as dicts
    org_data = json.loads(script)

    # Avoid out of bound index
    if org_data == []:
        raise Exception(f"No data on page {page_no}")

    # Rearrange data into dict of the form: {col1 : [v1, v2, v3, ..], col2 : [v1, v2, v3, ...], ...}
    data = {}
    columns = [key for key in org_data[0]]
    for key in columns:
        vals = []
        for org in org_data:
            try:
                vals.append(org[key])
            except(KeyError):
                vals.append("")
        data[key] = vals
    
    return pd.DataFrame(data=data).set_index('ID')

def scrape_entire_site():
    # for testing only. in production delete this line:
    return pd.read_csv("scrape_simul.csv")

    """
    scrape_entire_site() -> DataFrame
    """
    data = pd.DataFrame()
    page_no = 1
    while True:
        crawl_delay()        
        try:
            data = pd.concat([data, scrape_page(page_no)])
            print(f"scanned page {page_no}")
        except:
            # Page is empty or non-existant
            break
        page_no += 1
    
    return data

#data = scrape_entire_site()
#data.to_csv("charity_data.csv")

def new_orgs():
    """
    Returns any new orgs as DataFrame
    """
    new_data = scrape_entire_site()
    old_data = pd.read_csv("charity_data.csv")
    new_orgs_list = []

    # Just comparing organisation names
    for index, org_name in enumerate(new_data.loc[:,'organizationName']):
        if org_name not in (old_data.loc[:,'organizationName']).values:
            new_orgs_list.append(index)

    return new_data.loc[new_orgs_list]

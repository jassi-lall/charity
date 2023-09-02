"""
Demonstrates how you can execute JavaScript code embedded in HTML responses using selenium and headless chromemium driver
Useful for scraping content that requires js.

Not needed for the project.

Just a reference for future projects
"""


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


def executeJS(url):
    options = Options()
    options.add_argument('--headless=new') 
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    page_source = driver.page_source
    driver.close()
    return page_source

page_source = executeJS('https://givingmatters.civicore.com/nonprofits')
soup = BeautifulSoup(page_source, 'html.parser')
m = soup.find(id='main')

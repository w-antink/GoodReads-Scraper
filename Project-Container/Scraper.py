#IMPORTS==================================
import selenium # type: ignore
import re #Necessary for the conv_names function
import time
import json
import configparser
from selenium import webdriver  
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
import requests
from bs4 import BeautifulSoup
#=========================================

#SCRAPER==================================    
options = Options()
options.headless = False  # don't trust the user to not mess with the slides
driver = webdriver.Firefox()

# Read config file
config = configparser.ConfigParser()
config.read('config.ini')

def scrape_book(driver, type): #Grabs all of the data from a given book's page.

    link = 'https://www.goodreads.com/book/show/42135029-city-of-girls'
    page = requests.get(link, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(page.content, "html.parser")
    
    #results = soup.find(id="content-container")
    recipe_cards = results.find_all("div", class_="cell small-6 medium-3 large-2")

    title = soup.find("h1", class_="Text__title1").get_text(strip=True)
    print(title)
    #Grabs just the author name. Very dirty and not built for edge cases yet.
    authors = []
    for auth_element in driver.find_elements(By.CLASS_NAME, 'ContributorLink__name'):
        authors.append(auth_element.text)
        
    author = authors[0]
    

    addtl_authors = authors[1:-1]
    

    shelf_location = type
  

    #genres = '' #Not sure how to implement this.

    publish_date = (driver.find_element(By.CLASS_NAME, 'FeaturedDetails').text).split("\n")[-1].replace("First published ", "")
    

    try:
        series = (driver.find_element(By.CLASS_NAME, 'Text__title3').text).split('#')[0].strip()
        number_in_series = int(re.search(r'#(\d+)', driver.find_element(By.CLASS_NAME, 'Text__title3').text).group(1))

    except:
        pass
    reading_start = ''
    reading_end = ''

    printem=False
    if printem==True:
        print(title)
        print(author)
        print(addtl_authors)
        print(shelf_location)
        print(publish_date)
        print(series, number_in_series)
        print('\n//////\n')

def run_scraper(driver):
    driver.get('https://www.goodreads.com/ap/signin?language=en_US&openid.assoc_handle=amzn_goodreads_web_na&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.goodreads.com%2Fap-handler%2Fsign-in&siteState=eyJyZXR1cm5fdXJsIjoiaHR0cHM6Ly93d3cuZ29vZHJlYWRzLmNvbS8ifQ%3D%3D')
    
    try: #Try to get credentials from config.ini

        if 'credentials' in config and 'username' in config['credentials'] and 'password' in config['credentials']:
            username = str(config['credentials']['username'])
            password = str(config['credentials']['password'])
            print("Credentials loaded from config.ini.")
        else: #If credentials are not in the config, prompt the user for input
            #Need to make it so they can actually do this. Need to adjust so multiple attempts possible.
            print("Credentials not found in config.ini. Please enter them manually. If you don't know how to do this, reach out to me.")
    except:
        pass


    try:
        #Pass in login credentials
        driver.find_element(By.ID, 'ap_email').send_keys(f'{username}')
        driver.find_element(By.ID, 'ap_password').send_keys(f'{password}')
        driver.find_element(By.ID, 'signInSubmit').click()
    except:
        print("\nSorry, something went wrong.\n")
    
    #Iterate through shelves
    shelf_types = ['read', 'currently-reading', 'to-read']
    for type in shelf_types:
        driver.get(f'https://www.goodreads.com/review/list/102007809-jeannette-antink?shelf={type}')
        time.sleep(0.1)
        p=1
        print(f'Scraping page {p} of {type}')
        while True:
            try:       
                #Iterate through books with url builder.
                book_links = [book.find_element(By.CSS_SELECTOR, "a[href]").get_attribute("href") for book in driver.find_elements(By.CLASS_NAME, 'bookalike')]
                print(f'Captured {len(book_links)} titles')
                
                if len(book_links) == 0:
                            print('No more books found, ending scrape.')
                            break

                for link in book_links:
                    driver.get(link)
                    scrape_book(driver, type)
                driver.get(f'https://www.goodreads.com/review/list/102007809-jeannette-antink?page={p}&shelf=read')
            
            except:
                pass
#=========================================
run_scraper(driver)
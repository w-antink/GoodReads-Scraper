#IMPORTS==================================
import selenium # type: ignore
import re #Necessary for the conv_names function
import time
import json
from selenium import webdriver  
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
#=========================================

#SCRAPER==================================    
options = Options()
options.headless = False  # don't trust the user to not mess with the slides
driver = webdriver.Firefox()

def run_scraper(driver):
    driver.get('https://www.goodreads.com/ap/signin?language=en_US&openid.assoc_handle=amzn_goodreads_web_na&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.goodreads.com%2Fap-handler%2Fsign-in&siteState=eyJyZXR1cm5fdXJsIjoiaHR0cHM6Ly93d3cuZ29vZHJlYWRzLmNvbS8ifQ%3D%3D')
    
    #Enter login credentials (Need to adjust so multiple attempts possible.)
    try:
        driver.find_element(By.ID, 'ap_email').send_keys(f'{input("What's your username?\n")}')
        driver.find_element(By.ID, 'ap_password').send_keys(f'{input("What's your password?\n")}')
        driver.find_element(By.ID, 'signInSubmit').click()
    except:
        print("\nSorry, something went wrong.\n")
    
    #Scraping shelf contents
    shelf_types = ['read', 'currently-reading', 'to-read']
    for type in shelf_types:
        driver.get(f'https://www.goodreads.com/review/list/102007809-jeannette-antink?shelf={type}')
        print(f'Scraping for {type}')

        #Below is grabbing all of the data on each book.
        title = driver.find_element(By.CLASS_NAME, 'Text__title1').text
        print(title)

        #Grabs just the author name. Very dirty and not built for edge cases yet.
        authors = []
        for auth_element in driver.find_elements(By.CLASS_NAME, 'ContributorLink__name'):
            authors.append(auth_element.text)
        
        author = authors[0]
        print(author)

        addtl_authors = authors[1:-1]
        print(addtl_authors)

        shelf_location = type
        print(shelf_location)

        #genres = '' #Not sure how to implement this.

        publish_date = (driver.find_element(By.CLASS_NAME, 'FeaturedDetails').text).split("\n")[-1].replace("First published ", "")
        print(publish_date)

        try:
            series = (driver.find_element(By.CLASS_NAME, 'Text__title3').text).split("in the")[-1].strip().rsplit("series", 1)[0].strip()
            number_in_series = int((driver.find_element(By.CLASS_NAME, 'Text__title3').text).split()[1])
            print(series, number_in_series)
        except:
            pass
        reading_start = ''
        reading_end = ''
        print('\n//////\n')
    
    

#=========================================
run_scraper(driver)
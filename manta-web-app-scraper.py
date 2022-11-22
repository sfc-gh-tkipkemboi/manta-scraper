import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup

import undetected_chromedriver as uc
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless') # for a headless browser
options.add_argument('--disable-gpu')

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager" # to make the page load faster

def scrape(category, city, state, pages):
    st.text('Loading and downloading the driver')
    driver = uc.Chrome(desired_capabilities=caps, options=options)
    st.text('Browser loaded')

    items_list = []
    for x in range(1, int(pages)): # you can change the number of pages
        driver.get(f'https://www.manta.com/search?search_source=nav&search={category}&city={city}&state={state}&device=desktop&screenResolution=2400x1300&pg={x}')
        st.text(f'Page {x}')
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mapid"]')))
        soup = BeautifulSoup(driver.page_source, 'lxml')
        cards = soup.select('.md\:mt-4')

        for card in cards:
            try:
                name = card.select_one('.hover\:text-primary-v1').text
            except:
                name = None
            try:
                address_card = card.select('.ml-4 div')
                address = address_card[0].text + ',' + ' ' + address_card[1].text
            except:
                address = None
            try:
                phone = card.select_one('.mt-2 div').text
            except:
                phone = None
            try:
                website = card.select_one('.hover\:underline')['href']
                website = website.replace('/urlverify?redirect=https%3A%2F%2F', '')
                if '/urlverify?redirect' in website:
                    website = website.replace('/urlverify?redirect=http%3A%2F%2F', '')
                else:
                    pass
                website = website.replace(website[website.index('%'):], '')
            except:
                website = None

            items = {
                'Name': name,
                'Address': address,
                'Phone': phone,
                'Website': website
            }

            items_list.append(items)

    df = pd.DataFrame(items_list)
    st.dataframe(df)

st.title('Manta.com Buisness Directory Scraper')
with st.form('Scraper'):
    st.text('If you get any error make sure you choose a valid category, state, city and number of page as well.')
    st.text('So before you click on the scrape button, I will advice you go to the site (https://www.manta.com/business-directory) to test the parameters before inputing them here')
    st.text('Check the page limit as well. Because the site is very sensitive to this parameters.')
    category = st.text_input('Category EX: Restuarants')
    city = st.text_input('City EX: Miami')
    state = st.text_input('State EX: Florida')
    pages = st.number_input(f'Number of pages to scrape? NB: Each page has 35 listings')
    button = st.form_submit_button('scrape')
    if button:
        scrape(category, city, state, pages)

import pandas as pd
from bs4 import BeautifulSoup

import undetected_chromedriver as uc
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager" # to make the page load faster

print('Loading and downloading the driver')
driver = uc.Chrome(desired_capabilities=caps, options=options)
print('Browser loaded')

items_list = []
for x in range(1, 10): # you can change the number of pages
    driver.get(f'https://www.manta.com/search?search_source=nav&search=Restaurants&city=New&state=york&device=desktop&screenResolution=2400x1300&pg={x}')
    print(f'Page {x}')
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
df.to_csv('Restaurants.csv', index=False)
print(df)
driver.quit()
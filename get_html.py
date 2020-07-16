
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

PATH = "/Applications/chromedriver"
driver = webdriver.Chrome(PATH)

def scrapPage(webpage):
    """
    takes a webpage url as input and scraps all relevant data
    """
    #faire une boucle pour all categories
    driver.get(webpage)
    #driver.get('http://80breakfasts.com/category/breakfast/')

    main = driver.find_element(By.TAG_NAME, 'main')
    href = main.find_elements(By.CLASS_NAME, 'more-link')

    all_links = []
    for el in href:
        link = el.get_attribute('href')
        all_links.append(link)

    for link in all_links:
        print(link)
        driver.get(link)
        try:
            html = driver.page_source
            title = driver.title.replace(' ', '_').replace('/', '_')
            with open(f"clean_recipes/recipe_{title}.html", "w") as file:
                file.write(html)
                file.close()
        except Exception as e:
            print("got error", e)
            time.sleep(10)
            driver.quit()

    driver.get(webpage)

    try: 
        next_url = driver.find_element(By.CLASS_NAME, 'pagination-next').find_element(By.TAG_NAME, 'a').get_attribute('href')
    except Exception:
        return

    try:
        scrapPage(next_url)
    except Exception as e:
        print("got error", e)
        driver.quit()

    
if __name__ == '__main__':
    #scrapPage('http://80breakfasts.com/category/breakfast/')
    #scrapPage('http://80breakfasts.com/category/chicken/')
    #scrapPage('http://80breakfasts.com/category/beef/')
    #scrapPage('http://80breakfasts.com/category/veggies/')
    #scrapPage('http://80breakfasts.com/category/sweets/')
    driver.quit()


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

    #main = driver.find_elements(By.TAG_NAME, 'div')
    list_groups = driver.find_elements(By.CLASS_NAME, 'list-group')

    all_links = []
    for group in list_groups:
        main = group.find_elements(By.CLASS_NAME, 'archiverecipe')
        for element in main: 
            link = element.find_element(By.TAG_NAME, 'a').get_attribute('href')
            all_links.append(link)

    for link in all_links:
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

if __name__ == '__main__':
    scrapPage('https://www.101cookbooks.com/archives.html')
    driver.quit()

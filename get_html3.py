
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
    main = driver.find_element(By.CLASS_NAME, 'wprm-recipe-buttons').find_element(By.LINK_TEXT, 'PRINT RECIPE')
    link = main.get_attribute('href')
    
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
    all_pages = ['https://www.ambitiouskitchen.com/chicken-green-bean-stir-fry/',
    'https://www.ambitiouskitchen.com/salmon-taco-bowls/',
    'https://www.ambitiouskitchen.com/slow-cooker-yellow-chicken-curry/',
    'https://www.ambitiouskitchen.com/healthy-slow-cooker-chicken-tikka-masala/',
    'https://www.ambitiouskitchen.com/best-vegetarian-chili-recipe/',
    'https://www.ambitiouskitchen.com/coconut-tomato-lentil-soup/',
    'https://www.ambitiouskitchen.com/the-easiest-chopped-chickpea-greek-salad/',
    'https://www.ambitiouskitchen.com/nourishing-yellow-chickpea-pumpkin-curry/',
    'https://www.ambitiouskitchen.com/saucy-baked-pumpkin-pasta/',
    'https://www.ambitiouskitchen.com/spicy-thai-peanut-chicken-sweet-potato-noodle-stir-fry/',
    'https://www.ambitiouskitchen.com/vegetarian-tofu-cashew-coconut-curry/',
    'https://www.ambitiouskitchen.com/20-minute-garlic-parmesan-rigatoni-chicken-sausage-broccoli/',
    'https://www.ambitiouskitchen.com/caramelized-onion-fig-goat-cheese-pizza-arugula-video/',
    'https://www.ambitiouskitchen.com/vegan-sweet-potato-buddha-bowl-almond-butter-dressing/',
    'https://www.ambitiouskitchen.com/thai-peanut-chicken-edamame-quinoa-stir-fry/',
    'https://www.ambitiouskitchen.com/sweet-potato-quinoa-salad-with-cherries-goat-cheese-candied-walnuts/',
    'https://www.ambitiouskitchen.com/sesame-chicken-stir-fry-with-coconut-ginger-brown-rice-crushed-cashews/',
    'https://www.ambitiouskitchen.com/turkey-bacon-avocado-mozzarella-grilled-cheese-artisan-tomato-soup/',
    'https://www.ambitiouskitchen.com/dark-chocolate-raspberry-and-brie-grilled-cheese/',
    'https://www.ambitiouskitchen.com/pinto-bean-chicken-chili/',
    'https://www.ambitiouskitchen.com/stuffed-sweet-potatoes-with-turkey-caramelized-onions-apple/',
    'https://www.ambitiouskitchen.com/turkey-meatballs-in-spicy-tomato-basil-sauce-with-burrata/',
    'https://www.ambitiouskitchen.com/sheet-pan-honey-mustard-chicken/',
    'https://www.ambitiouskitchen.com/healthy-slow-cooker-chicken-tikka-masala/',
    'https://www.ambitiouskitchen.com/vegetarian-spinach-pumpkin-lasagna/',
    'https://www.ambitiouskitchen.com/healthy-low-carb-zucchini-lasagna-spicy-turkey-meat-sauce/',
    'https://www.ambitiouskitchen.com/how-to-grill-pizza/',
    'https://www.ambitiouskitchen.com/low-carb-chicken-zucchini-enchilada-bake/',
    'https://www.ambitiouskitchen.com/moms-mayan-sweet-potato-polenta-bake/'
    ]
    for page in all_pages:
        scrapPage(page)
    driver.quit()

import os
from random import randint
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Updating PATH environment variable to include Firefox WebDriver location
os.environ["PATH"] += r"/usr/local/bin/geckodriver"

# Last ENTITITES_MAP update: December 24th, 2022
ENTITIES_MAP = {
    "next_page": "_1bfat5l",
    "current_page": "_u60i7ub",
    "listed_property": "cy5jw6o dir dir-ltr",
    "title": "t1jojoys dir dir-ltr",
    "description": "t6mzqp7 dir dir-ltr"
}

BASE_URL = "https://www.airbnb.com.br/s"

# Initializing selenium webdriver
driver = webdriver.Firefox()


def main_page_parser(soup):
    """
    This function receives a BeautifulSoup object with html content from a
    Airbnb search results page and returns a Python dictionary containing id, title
    and description for all properties within the page
    """
    res = {}
    properties = soup.find_all("div", {"class":
                                       ENTITIES_MAP["listed_property"]})
    print(f"Page {soup.find('button', {'class': ENTITIES_MAP['current_page']}).text} " +
          f"- Properties in this page: {len(properties)}")

    for property in properties:
        href = property.find("a").get("href").split("?")[0].split("/")[-1]
        title = property.find("div", {"class": ENTITIES_MAP["title"]}).text
        description = property.find("span", {"class": ENTITIES_MAP["description"]})
        if description is not None:
            description = description.text
        else:
            description = ""
        res[href] = {"title": title, "description": description}

    return res


def scrap_main_page(driver, city_name, sleep_time=[3, 4]):
    """
    This function receives a selenium webdriver and a city_name and returns a JSON
    file with id, title and description for all available properties in the city
    """
    res = {}
    driver.get(f"{BASE_URL}/{city_name}/homes")  # Gets first page of results for city_name
    sleep(randint(sleep_time[0], sleep_time[1]))
    soup = BeautifulSoup(driver.page_source, "html.parser")
    res.update(main_page_parser(soup))
    sleep(randint(sleep_time[0], sleep_time[1]))

    for i in range(14):
        element = driver.find_element(By.CLASS_NAME, ENTITIES_MAP["next_page"])
        element.click()
        sleep(randint(sleep_time[0], sleep_time[1]))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        res.update(main_page_parser(soup))

    return res

city = "Sao Paulo"
res = scrap_main_page(driver, city)
print(res)
print(len(res))

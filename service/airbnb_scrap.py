from random import randint
from time import sleep
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Last ENTITITES_MAP update: December 24th, 2022
ENTITIES_MAP = {
    "next_page": "_1bfat5l",
    "current_page": "_u60i7ub",
    "listed_property": "cy5jw6o dir dir-ltr",
    "title": "t1jojoys dir dir-ltr",
    "description": "t6mzqp7 dir dir-ltr"
}

BASE_URL = "https://www.airbnb.com.br"


def main_page_parser(soup):
    """
    This function receives a BeautifulSoup object with html content from a
    Airbnb search results page and returns a Python list containing ids
    for all properties within the page
    """
    res = []
    properties = soup.find_all("div", {"class":
                                       ENTITIES_MAP["listed_property"]})

    for property in properties:
        href = property.find("a").get("href").split("?")[0].split("/")[-1]
        res.append(href)

    return res


def scrap_main_page(driver, city_name, sleep_time=[3, 4], pages=15):
    """
    This function receives a selenium webdriver and a city_name and returns a Python
    dictionary containing page numbers and BeautifulSoup objects with html content

    Optional arguments:
    sleep_time: minimum and maximum sleep time between clicking 'next page' and
    retrieving html content

    pages: number of result pages to be scrapped
    """
    res = {}
    driver.get(f"{BASE_URL}/s/{city_name}/homes")  # Gets first page of results for city_name
    sleep(randint(sleep_time[0], sleep_time[1]))
    soup = BeautifulSoup(driver.page_source, "html.parser")
    res[soup.find('button', {'class': ENTITIES_MAP['current_page']}).text] = soup

    for i in range(pages):
        element = driver.find_element(By.CLASS_NAME, ENTITIES_MAP["next_page"])
        element.click()
        sleep(randint(sleep_time[0], sleep_time[1]))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        res[soup.find('button', {'class': ENTITIES_MAP['current_page']}).text] = soup

    return res

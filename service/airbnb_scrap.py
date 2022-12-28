from random import randint
from time import sleep
import warnings
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Last update: December 24th, 2022
ENTITIES_MAP = {
    "next_page": "_1bfat5l",
    "current_page": "_u60i7ub",
    "listed_property": "cy5jw6o dir dir-ltr",
}

# Last update: December 28th, 2022
PROPERTY_ATTRIBUTES_MAP = {
    "title": ["h1", {"class": "_fecoyn4"}],
    "city": ["span", {"class": "_9xiloll"}],
    "rating": ["span", {"class": "_17p6nbba"}],
    "comments_qty": ["span", {"class": "_s65ijh7"}],
    "price_per_night": ["span", {"class": "_tyxjp1"}],
    "fees": ["span", {"class": "_1k4xcdh"}],
    "main_ammenities": ["div", {"class": "iikjzje i10xc1ab dir dir-ltr"}],
    "max_guests": ["li", {"class": "l7n4lsf dir dir-ltr"}]
}


def main_page_parser(soup):
    """
    This function receives a BeautifulSoup object with html content from an
    Airbnb search results page and returns a Python list containing ids
    for all properties within the page
    """
    if type(soup) is not BeautifulSoup:
        raise TypeError("main_page_parser argument must be a BeautifulSoup object")

    res = []
    properties = soup.find_all("div", {"class":
                                       ENTITIES_MAP["listed_property"]})

    for property in properties:
        href = int(property.find("a").get("href").split("?")[0].split("/")[-1])
        res.append(href)

    if len(res) < 18:
        warnings.warn("The webpage has less than 18 listed properties." +
                      "You might want to check soup argument", Warning)

    return res


def detail_parser(soup):
    """
    This function receives a BeautifulSoup object with html content from an
    Airbnb property page and returns a Python dictionary with property attributes
    The dictionary DETAILS_MAP works as an attribute list
    """
    if type(soup) is not BeautifulSoup:
        raise TypeError("main_page_parser argument must be a BeautifulSoup object")

    res = {}

    for attribute, location in PROPERTY_ATTRIBUTES_MAP.items():
        res[attribute] = [item.text for item in soup.find_all(location[0], location[1])]

    return res


def scrap_main_page(driver, city_name, sleep_time=[3, 4], pages=15):
    """
    This function receives a selenium webdriver and a city_name and returns a Python
    dictionary containing page numbers and BeautifulSoup objects with html content

    Optional arguments:
    sleep_time: minimum and maximum sleep time between clicking 'next page' and
    retrieving html content. This allows for time to page to load.

    pages: number of result pages to be scrapped. The maximum number of pages
    returned in a search is 15.
    """
    if type(driver) is not webdriver.Firefox:
        raise TypeError("driver argument must be a selenium.webdriver.Firefox object")

    if type(city_name) is not str:
        raise TypeError("city_name argument must be a string")

    if type(sleep_time) is not list:
        raise TypeError("sleep_time argument must be a list with two int or float elements")

    if len(sleep_time) != 2:
        raise TypeError("sleep_time arument must have exactly two elements (int or float)")

    for sec in sleep_time:
        if type(sec) is not int:
            raise TypeError(" argument must be a BeautifulSoup object")

    if type(pages) is not int:
        raise TypeError("pages argument must be an integer")

    if pages < 1:
        raise ValueError("pages value must be greater than 1")

    BASE_URL = "https://www.airbnb.com.br"
    res = {}

    driver.get(f"{BASE_URL}/s/{city_name}/homes")  # Gets first page of results for city_name
    sleep(randint(sleep_time[0], sleep_time[1]))
    soup = BeautifulSoup(driver.page_source, "html.parser")
    res[int(soup.find('button', {'class': ENTITIES_MAP['current_page']}).text)] = soup

    for i in range(pages - 1):
        element = driver.find_element(By.CLASS_NAME, ENTITIES_MAP["next_page"])
        element.click()
        sleep(randint(sleep_time[0], sleep_time[1]))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        res[int(soup.find('button', {'class': ENTITIES_MAP['current_page']}).text)] = soup

    if len(res) < pages:
        warnings.warn("The number of search pages loaded is smaller than user specified" +
                      "pages argument. You might want to review pages and sleep_time arguments", Warning)

    return res

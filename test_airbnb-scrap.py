from unittest import TestCase
import os
from random import choice
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from service.airbnb_scrap import main_page_parser, scrap_main_page

driver = webdriver.Firefox()  # opens webdriver

######################################################################
#             M O D E L   T E S T   C A S E S
######################################################################


class TestAccount(TestCase):
    """Test Cases for Account Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        os.environ["PATH"] += r"/usr/local/bin/geckodriver"

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        driver.close()  # closes webdriver

    def setUp(self):
        """This runs before each test"""

    def tearDown(self):
        """This runs after each test"""

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_parser_return_type(self):
        """ It should return a list of integers"""
        cities = ["Sao Paulo", "Campos do Jordao", "Monte Verde", "Visconde de Maua"]
        city = choice(cities)
        soup = BeautifulSoup(requests.get(f"https://www.airbnb.com.br/s/{city}/homes").content, "html.parser")

        ids = main_page_parser(soup)

        for id in ids:
            self.assertIsInstance(id, int)

    def test_parser_input_type(self):
        """ It should return a TypeError for inputs that are not BeautifulSoup objects """
        self.assertRaises(TypeError, main_page_parser, 1)
        self.assertRaises(TypeError, main_page_parser, 'test')

    def test_scrapper_return_type(self):
        """ It should return a dictionary whose keys are integers and values are BeautifulSoup objects"""
        cities = ["Sao Paulo", "Campos do Jordao", "Monte Verde", "Visconde de Maua"]
        city = choice(cities)
        res = scrap_main_page(driver, city)

        self.assertIsInstance(res, dict)

        for key in res.keys():
            self.assertIsInstance(key, int)

        for value in res.values():
            self.assertIsInstance(value, BeautifulSoup)

    def test_scrapper_input_type(self):
        """ It should return a Type error if input types are different from function specifications """
        self.assertRaises(TypeError, scrap_main_page, 1, "Sao Paulo")
        self.assertRaises(TypeError, scrap_main_page, driver, 1)
        self.assertRaises(TypeError, scrap_main_page, driver, "Sao Paulo", sleep_time=["Hello", "World"])
        self.assertRaises(TypeError, scrap_main_page, driver, "Sao Paulo", pages="Sao Paulo")

    def test_scrapper_warning(self):
        """ It should return a Warning if the specified number of pages is bigger than the quantity of scrapped pages """
        self.assertWarns(Warning, scrap_main_page, driver, "Sao Paulo", pages=20)

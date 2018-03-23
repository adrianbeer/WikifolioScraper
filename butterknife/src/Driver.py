from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait

import time

from selenium.common.exceptions import NoSuchElementException
from configparser import ConfigParser


class Driver:

    def __init__(self, config, implicit_wait=0):
        parser = ConfigParser()
        parser.read(config)
        self._dict = parser['butterknife']
        binary = FirefoxBinary(self._dict['foxbin'])
        gecko = self._dict['gecko']
        self.driver = webdriver.Firefox(executable_path=gecko, firefox_binary=binary)
        self.wait = WebDriverWait(self.driver, implicit_wait)
        self.driver.implicitly_wait(implicit_wait)
        self._current_website = None

    @property    
    def current_website(self):
        return self._current_website

    @current_website.setter    
    def current_website(self, value):
        self._current_website = value
        self.driver.get(value)
    
    def get_text_by_class(class_args):
        """Returns the inner text of a class element."""
        try:
            raw_value = self.driver.find_element_by_class_name(class_args)
            return raw_value.text
        except NoSuchElementException as e:
            print(e)
    
    def scrape_links(self, link, name, amount, cap=50):
        self.current_website = link
        links = []
        _cap = cap #max. number of scroll downs
        counter = 1
        while (len(links) < amount) and (counter < _cap):
            #scrolls down until `amount` of links have been obtained
            counter += 1
            self.scroll_down()
            elements = self.driver.find_elements_by_class_name(name)
            for element in elements:
                try:
                    links.append(element.get_attribute('href'))
                except AttributeError as e:
                    print(e)
        return links[0:amount]
    
    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.quit()

    def quit(self):
        self.driver.quit()
                                                      
    

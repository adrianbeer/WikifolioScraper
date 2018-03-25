from configparser import ConfigParser
from random import uniform
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait


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
        self._locating_elements = dict(
                By.CLASS_NAME = self.driver.find_elements_by_class_name,
                By.CSS_SELECTOR = self.driver.find_elements_by_css_selector,
                By.ID = self.driver.find_elements_by_id,
                By.LINK_TEXT = self.driver.find_elements_by_link_text,
                By.NAME = self.driver.find_elements_by_name,
                By.PARTIAL_LINK_TEXT = self.driver.find_elements_by_partial_link_text,
                By.TAG_NAME = self.driver.find_elements_by_tag_name,
                By.XPATH = self.driver.find_elements_by_xpath,
            )

    @property    
    def current_website(self):
        return self._current_website

    @current_website.setter    
    def current_website(self, value):
        self._current_website = value
        self.driver.get(value)
    
    def get_website_elements(by, identifier, attribute=None):
        elements = self._locating_elements.[by](identifier)
        if attribute is None:
            return elements
        elif attribute == 'text':
            return [e.text for e in elements]
        else:
            raise KeyError("Requested attribute doesn't exist")

    
    def get_links(self, source, class_name, amount):
        self.current_website = source
        links = []
        while (len(links) < amount):
            self.scroll_down() #Scroll down to get access to more links
            elements = self.driver.find_elements_by_class_name(class_name)
            for element in elements:
                try:
                    links.append(element.get_attribute('href'))
                except AttributeError as e:
                    print(e)
        return links[0:amount]
    
    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(uniform(1,2))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.quit()

    def quit(self):
        self.driver.quit()
                                                      
    

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

    @property    
    def current_website(self):
        return self._current_website

    @current_website.setter    
    def current_website(self, value):
        self._current_website = value
        self.driver.get(value)

    def get_links(self, source, class_name, amount):
        self.current_website = source
        previous_amount = -1
        links = []
        #End loop when desired amount has been reached or no further progress
        #can be made.
        while (len(links) < amount and len(links) > previous_amount):
            previous_amount = len(links)
            self.scroll_down() #Scroll down to get access to more links
            links.extend(self.get_website_elements(By.CLASS_NAME, class_name, 'href'))
        return links[0:amount]

    def get_website_elements(self, by, identifier, desired_attribute=None):
        elements = self._find_elements(by, identifier)
        if desired_attribute == 'text':
            elements =  [e.text for e in elements]
        elif desired_attribute is None:
            pass
        else:
            elements =  [e.get_attribute(desired_attribute) for e in elements]
        assert elements is not None
        assert len(elements) >= 1
        return elements

    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(uniform(1,2))

    def _find_elements(self, by, identifier):
        elements = None
        if by == By.CLASS_NAME:
            elements = self.driver.find_elements_by_class_name(identifier)
        elif by == By.XPATH: 
            elements = self.driver.find_elements_by_xpath(identifier)
        elif by == By.NAME:
            elements = self.driver.find_elements_by_name(identifier)
        elif by == By.CSS_SELECTOR:
            elements = self.driver.find_elements_by_css_selector(identifier)
        elif by == By.ID:
            elements = self.driver.find_elements_by_id(identifier)
        elif by == By.LINK_TEXT:
            elements = self.driver.find_elements_by_link_text(identifier)
        elif by == By.PARTIAL_LINK_TEXT:
            elements = self.driver.find_elements_by_partial_link_text(identifier)
        elif by == By.TAG_NAME:
            elements = self.driver.find_elements_by_tag_name(identifier)
        else:
            raise NoSuchElementException
        return elements

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.quit()

    def quit(self):
        self.driver.quit()



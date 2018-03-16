from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert

from seleniim.common.exceptions import NoSuchElementException
from configparser import ConfigParser


class Driver:

    def __init__(self, config, implicit_wait=0):
        config = ConfigParser()
        config.read(config)
        self._dict = config._sections['butterknife']
        self.driver = webdriver.PhantomJS(executable_path = self._dict['phantomjs'])
        self.driver.implicit_wait(implicit_wait)
        self.current_website = None

    @property    
    def current_website(self):
        return self.current_website

    @current_website.setter    
    def current_website(self, value):
        self.current_website = value
        self.driver.get(value)
    
    def get_text_by_class(class_args):
        """Returns the inner text of a class element."""
        try:
            raw_value = self.driver.find_element_by_class_name(class_args)
            return raw_value.text
        except NoSuchElementException as e:
            print(e)
    
    def scrape_links(self, name, amount, cap=50):
        links = []
        _cap = cap #max. number of scroll downs
        counter = 1
        while (links < amount) and (counter < _cap):
            #scrolls down until `amount` of links have been obtained
            counter++
            scroll_down()
            elements = self.driver.find_elements_by_class_name(name)
            for element in elements:
                try:
                    links.append(element.get_attribute('href'))
                except AttributeError as e:
                    print(e)
        return links
    
    def _scroll_down(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.quit()
                                                      
    

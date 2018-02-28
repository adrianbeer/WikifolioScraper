from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert

from seleniim.common.exceptions import NoSuchElementException
from configparser import ConfigParser

class Driver:

    def __init__(self, config):
        self._driver = webdriver.PhantomJS(executable_path = "C:\\Users\\Adrian\\Documents\\Python\\phantomjs-2.1.1-windows\\bin\\phantomjs")
        self._current_website
        config = ConfigParser()
        config.read(config)
        self._dict = config._sections['butterknife']

    @property    
    def current_website(self):
        return self._current_website

    @current_website.setter    
    def current_website(self, value):
        self._current_website = value
        self._driver.get(value)
    
    def get_text_by_class(class_args):
        """Returns the inner text of a class element."""
        try:
            raw_value = self.driver.find_element_by_class_name(class_args)
            return raw_value.text
        except NoSuchElementException as e:
            print(e)
    
    '@return [equities, cash, etf, structured]'
    def scrape_weighting(self, soup):
        try:
            equities = soup.find('td', attrs={'data-title':'Aktien'}).text
            cash = soup.find('tr', class_="underlyingGroupHeader table-group-row cash")
            cash = cash.find('td', class_='numeric').text
            etf = soup.find('td', attrs={'data-title':'ETFs'}).text
            structured = soup.find('td', attrs={'data-title':'Strukturierte Produkte'}).text
            weighting = [equities, cash, etf, structured]
            for i, value in enumerate(weighting):
                weighting[i] = value.strip(' \t\r\n').strip('"')
        except Exception as e:
            print("ERROR AT WEIGHTING")
            print(e)
        else:
            return weighting

    def login(self):
        self.driver.get('https://www.wikifolio.com/de/de/home')
        self.driver.maximize_window()
        # accept select-country-query
        element = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, 'js-change-country-mode-btn')))
        self.chainz.click(element).perform()
        time.sleep(2)
        element = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'js-login-button')))
        self.chainz.click(element).perform() # initiate Login-Pop-Up
        try:
            element = self.wait.until(EC.element_to_be_clickable((By.ID, 'Username')))
            element.send_keys(username)
            element = self.wait.until(EC.element_to_be_clickable((By.ID, 'Password')))
            element.send_keys(pwd)
            self.driver.find_element_by_class_name('margin-top-30').click()
            time.sleep(2)
            return True
        except: 
            return False
            
    def scrape_links(self, value):
        links = []
        elements = self._driver.find_elements_by_class(value)
        for element in elements:
            try:
                links.append(element.get_attribute('href'))
            except AttributeError as e:
                print(e)
        self.scroll_down(amount)
        links = []
        for link in raw_links:
            links.append(link['href'])
        return links
    
    # THIS IS A PRIVATE METHOD - DO NOT USE IN MAIN
    # get the list of a decent amount of folio links
    # condition: driver has to be on given website
    def scroll_down(self, amount):
        for i in range(amount):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(6)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.quit()
                                                      
    

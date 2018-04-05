from collections import namedtuple
from configparser import ConfigParser
from random import uniform
from time import sleep

from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from .Driver import Driver


Quarry = namedtuple('Quarry', ['title', 'amount', 'class_name', 'link'])


class WikifolioDriver(Driver):

    def __init__(self, config, implicit_wait):
        super().__init__(config, implicit_wait)
        self.username = self._dict['username']
        self.password = self._dict['password']
        self.quarries = []
        self.blocks = dict()

    def parse_quarries(self, config):
        """
        Variable description:

        :var quarries: list of 4-tuples (title, amount, class_name, link) to provide who, 
                            where and what information (RECONNAISSANCE).
        :var blocks: dict with `titles` as keys and a list of links, which were gained 
                    from the quarries.
        """
        parser = ConfigParser()
        parser.read(config)
        for key in parser['Quarries']:
            args = [key]
            args.extend(parser['Quarries'][key].split(' '))
            quarry = Quarry(
                    title=args[0], 
                    amount=int(args[1]), 
                    class_name=args[2],
                    link = args[3],
                    )
            self.quarries.append(quarry)

    def make_blocks_from_quarries(self):
        #Get links, which are to be harvested by `scrape_content` later on.
        #Currently links can only be harvested by the class_name attribute.
        for quarry in self.quarries:
            self.blocks[quarry.title] = super().get_links(
                    source=quarry.link,
                    class_name=quarry.class_name,
                    amount=quarry.amount
                ) 

    def login(self):
        """
        :returns: Cookies obtained by the login
        """
        t_trigger = "//h1[@class='c-ao-wikis__title']"
        b_accept_law = "//div[@class='c-button c-button--bold c-button--cursor-pointer js-disclaimer__change ']"
        b_anmelden = "//a[@class='c-button c-button--ghost-grey o-header-pre__buttons--equalwidth o-header-pre__login-button js-login-button']"
        f_username_name = 'Username'
        f_password_name = 'Password'
        b_login = "//button[@type='submit']"
        
        #GOTO Website
        self.current_website = 'https://www.wikifolio.com/de/de/home'
        self.driver.maximize_window()

        #Activate Eventviewer to trigger law query
        try:
            self.find_and_click(By.XPATH, t_trigger)
        except ElementClickInterceptedException:
            pass

        #Accept law query
        self.driver.switch_to.active_element
        element = self.find_and_click(By.XPATH, b_accept_law)

        self.find_and_click(By.XPATH, b_anmelden)

        element = self.find_and_click(By.NAME, f_username_name)
        element.send_keys(self.username)

        element = self.find_and_click(By.NAME, f_password_name)
        element.send_keys(self.password)

        self.driver.switch_to.active_element
        self.find_and_click(By.XPATH, b_login)

        cookies = self.driver.get_cookies()
        return cookies

    def scrape_content(self, link):
        """---------------------
        :returns: List of values

        .. warning:: Order of returned values to be harmonized w/ `.csv` files. 
        ------------------------"""
        self.current_website = link
        price = self._get_price()
        isin = self._get_isin()
        capital = self._get_capital
        cash = self._get_cash_ratio()
        return [isin, capital, price, cash]

    def find_and_click(self, by, identifier):
        element = self.wait.until(EC.element_to_be_clickable((by, identifier)))
        self._click(element)
        return element

    def _get_isin(self):
        e_isin = "//div[@class='c-certificate__item-value js-copy-isin']"
        return super().get_website_elements(By.XPATH, e_isin, 'text')[0]
        
    def _get_capital(self):
        e_capital = "//div[@class='c-certificate__item-value']"
        capital = super().get_website_elements(By.XPATH, e_capital, 'text')[0]
        # u20AC is the euro sign
        return capital.replace('.','').strip(' ', u"\u20AC")

    def _get_price(self):
        sell = "//div[@class='c-certificate__price-value js-certificate__sell']"
        buy = "//div[@class='c-certificate__price-value js-certificate__buy']"
        mid = "//div[@class='c-certificate__price-value js-certificate__mid']"

        try:
            sell = super().get_website_elements(By.XPATH, sell, 'text')[0]
            buy = super().get_website_elements(By.XPATH, buy, 'text')[0]
            sell = float(sell.replace(',','.'))
            buy = float(buy.replace(',', '.'))
            if sell.contains('-') or buy.contains('-'):
                raise NoSuchElementException
            else:
                price = ((sell+buy) / 2) 
        except (IndexError, NoSuchElementException):
            mid = super().get_website_elements(By.XPATH, mid, 'text')[0]
            price = float(mid.replace(',','.'))
        return price

    def _get_cash_ratio(self):
        e_portfolio = "//ul[@class='c-wfdetail__tabs-list']/li[2]"
        e_stock = "//span[@class='c-portfolio__head-label']"

        self.find_and_click(By.XPATH, e_portfolio)
        shares = super().get_website_elements(By.XPATH, e_stock, 'text')
        return WikifolioDriver._extract_cash(shares)

    def _click(self, element):
        # Tries to appear more human, by first moving to the element with
        # the cursor.
        try:
            ActionChains(self.driver).move_to_element(element).perform()
        except Exception as e:
            print(e)
        element.click()
        sleep(uniform(1, 2))

    @staticmethod
    def _extract_cash(shares):
        return round(float(shares[-1].strip(' %').replace(',','.'))/100, 2)


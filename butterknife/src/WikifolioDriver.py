from collections import namedtuple
from configparser import ConfigParser
from random import uniform
from time import sleep

from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
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
        #Scraping links: currently only available by class (html element)!
        for quarry in self.quarries:
            self.blocks[quarry.title] = super().get_links(
                    source=quarry.link,
                    class_name=quarry.class_name,
                    amount=quarry.amount
                ) 

    def scrape_content(self, link):
        """---------------------
        :returns: List of values

        .. warning:: Order of returned values to be harmonized w/ `.csv` files. 
        ------------------------"""
        self.current_website = link
        invested, cash = self._get_commitment_ratio()
        isin = self._get_isin()
        capital = self._get_capital
        return [isin, capital, invested, cash]

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

    def find_and_click(self, by, identifier):
        element = self.wait.until(EC.element_to_be_clickable((by, identifier)))
        self._click(element)
        return element

    def _click(self, element):
        # Tries to perform a more realistic click, than standard implementation
        try:
            ActionChains(self.driver).move_to_element(element).perform()
        except Exception as e:
            print(e)
        element.click()
        sleep(uniform(1, 2))

    def _get_commitment_ratio(self):
        # Get invested-to-cash ratio
        # Note: Xpath lists start at 1.
        e_portfolio = "//ul[@class='c-wfdetail__tabs-list']/li[2]"
        self.find_and_click(By.XPATH, e_portfolio)
        e_stock = "//span[@class='c-portfolio__head-label']"
        shares = super().get_website_elements(By.XPATH, e_stock, 'text')
        assert len(shares) == 2
        return [round(float(x.strip(' %').replace(',','.'))/100, 2) for x in shares]

    def _get_isin(self):
        # Get ISIN
        e_isin = "//div[@class='c-certificate__item-value js-copy-isin']"
        return super().get_website_elements(By.XPATH, e_isin, 'text')
        
    def _get_capital(self):
        # Get capital
        e_capital = "//dic[@class='c-certificate__item-value']"
        capital = super().get_website_elements(By.XPATH, e_capital, 'text')
        # u20AC is the euro sign
        return capital.replace('.','').strip(' ', u"\u20AC")


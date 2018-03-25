from random import uniform
from time import sleep
from collections import namedtuple
from configparser import ConfigParser

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

    def read_quarries(self, config):
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

    def get_links(self):
        #Scraping links: currently only available by class (html element)!
        for quarry in self.quarries:
            self.blocks[quarry.title] = super().get_links(
                    source=quarry.link,
                    class_name=quarry.class_name,
                    amount=quarry.amount
                    ) 

    def scrape_content(self, link):
        """---------------------"""
        """Initialize variables

        :returns: List of values

        .. warning:: 

        Order of returned values must be harmonized w/ the `.csv` files.
        

        Legende:
        e -> element
        ------------------------"""
        self.current_website = link
       
        # Get invested-to-cash ratio
        e_portfolio = "//ul[@class='c-wfdetail__tabs-list']/li[1]"
        element = self.driver.find_element_by_xpath(e_portfolio)
        self.click(element)
        e_stock = "//span[@class='c-portfolio__head-label']"
        shares = self.driver.get_website_elements(By.XPATH, e_stock, 'text')
        assert len(shares) == 2
        invested, cash = [round(x.strip([' ', '%']).replace(',','.')/100, 2) for x in shares]

        # Get ISIN
        e_isin = "//div[@class='c-certificate__item-value js-copy-isin']"
        isin = self.driver.get_website_elements(By.XPATH, e_stock, 'text')
        
        # Get capital
        e_capital = "//dic[@class='c-certificate__item-value']"
        capital = self.driver.get_website_elements(By.XPATH, e_stock, 'text')
        # u20AC is the euro sign
        capital = capital.replace('.','').strip(' ', u"\u20AC")
        return [isin, capital, invested, cash]

    def click(self, element):
        try:
            ActionChains(self.driver).move_to_element(element).perform()
        except Exception as e:
            print(e)
        element.click()
        sleep(uniform(1, 2))

    def login(self):
        """
        :returns: Cookies obtained by the login

        Initialize variables used for locating elements throughout the login
        routine.
        Legend:
          q -> query/question
          s -> selector; answers `q`
          b -> button
          f -> field of a form
          t -> trigger
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
        element = self.driver.find_element_by_xpath(t_trigger)
        try:
            self.click(element)
        except ElementClickInterceptedException:
            pass

        #Accept law query
        self.driver.switch_to.active_element
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, b_accept_law)))
        self.click(element)

        #Click "Anmelden"
        element = self.driver.find_element_by_xpath(b_anmelden)
        self.click(element)

        element = self.driver.find_element_by_name(f_username_name)
        self.click(element)
        element.send_keys(self.username)

        element = self.driver.find_element_by_name(f_password_name)
        self.click(element)
        element.send_keys(self.password)

        self.driver.switch_to.active_element
        element = self.driver.find_element_by_xpath(b_login)
        self.click(element)

        cookies = self.driver.get_cookies()
        return cookies


#    '@return [equities, cash, etf, structured]'
#    def scrape_weighting(self, soup):
#        try:
#            equities = soup.find('td', attrs={'data-title':'Aktien'}).text
#            cash = soup.find('tr', class_="underlyingGroupHeader table-group-row cash")
#            cash = cash.find('td', class_='numeric').text
#            etf = soup.find('td', attrs={'data-title':'ETFs'}).text
#            structured = soup.find('td', attrs={'data-title':'Strukturierte Produkte'}).text
#            weighting = [equities, cash, etf, structured]
#            for i, value in enumerate(weighting):
#                weighting[i] = value.strip(' \t\r\n').strip('"')
#        except Exception as e:
#            print("ERROR AT WEIGHTING")
#            print(e)
#        else:
#            return weighting

#    def add_cookie_from_config(self, config):
#        parser = ConfigParser()
#        parser.read(config)
#        cookie = dict()
#        for key in parser['cookies']:
#            cookie[key] = parser['cookies'][key]
#        self.driver.add_cookie(cookie)

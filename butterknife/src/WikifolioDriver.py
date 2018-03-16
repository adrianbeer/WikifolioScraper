from random import uniform
from time import sleep

from . import Driver


class WikifolioDriver(Driver):

     def __init__(self, config, implicit_wait):
        super().__init__(config, implicit_wait)
        self.username = self._dict['username']
        self.password = self._dict['password']

    @staticmethod
    def click(element):
        element.click()
        sleep(uniform(1, 2))

    def set_cookie(self, cookie):
        self.driver.add_cookie(cookie)

    def login(self):
        """
        Initialize variables used for locating elements throughout the login
        routine.
        Legend:
          q -> query/question
          s -> selector; answers `q`
          b -> plain_button
          f -> field of a form
        """
        b_random_class = 'c-ao-wikis__title'
        q_country_class = "btn dropdown-toggle js-disclaimer__min-height-32"
        q_country_title = 'Land wechseln'
        s_country_xpath = "//ul[@class='dropdown-menu inner']/li[4]"
        b_login1_class = 'c-button c-button--ghost-grey o-header-pre__buttons--equalwidth o-header-pre__login-button js-login-button'
        f_username_name = 'Username'
        f_password_name = 'Password'
        b_login2_class = 'c-button c-button--large c-button--block c-button--uppercase c-button--bold'
        
        #start logging in
        self.current_website = 'https://www.wikifolio.com/'
        self.driver.maximize_window()

        #Needed to trigger country selection
        element = self.driver.find_element_by_class_name(b_random_class)
        click(element)

        element = self.driver.find_element_by_class_name(q_country_class)
        click(element)

        element = self.driver.find_element_by_xpath(s_country_xpath)
        click(element)

        element = self.driver.find_element_by_class_name(b_login1_class)
        click(element)

        element = self.driver.find_element_by_name(f_username_name)
        click(element)
        element.send_keys(self.username)

        element = self.driver.find_element_by_name(f_password_name)
        click(element)
        element.send_keys(self.password)

        element = self.driver.find_element_by_class_name(b_login2_class)
        click(element)

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


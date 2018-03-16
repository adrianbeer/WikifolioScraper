from . import Driver

class WikifolioDriver(Driver):

     def __init__(self, config):
        super().__init__(config)
        self.username = self._dict['username']
        self.password = self._dict['password']


    def login(self):
        self.driver.maximize_window()
        #accept legal notice with international rights
        element = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn dropdown-toggle js-disclaimer__min-height-32')))
        self.chainz.click(element).perform()
        time.sleep(1)
        element = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'Internalional (beta)')))
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


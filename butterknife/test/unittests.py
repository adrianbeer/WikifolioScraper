import unittest
from ..src.WikifolioDriver import WikifolioDriver, Quarry
import os

class TestInitialization(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = WikifolioDriver(r'C:\Users\Adrian\Documents\GitHub\butterknife\butterknife\test\config.ini', 20)

    def test_site_navigation(self):
        self.driver.current_website = 'https://www.wikifolio.com/de/de/home'
        self.assertEqual(self.driver.driver.current_url, self.driver.current_website)

    def test_config_parser(self):
        self.assertEqual(self.driver.username, r'***REMOVED***')
        self.assertEqual(self.driver.password, r'***REMOVED***')

    def test_configure(self):
        self.driver.configure(r'C:\Users\Adrian\Documents\GitHub\butterknife\butterknife\test\quarries.ini')
        self.assertEqual(self.driver.quarries[0], Quarry(*('top20ger', 1, 'href', 'someLink')))

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == '__main__':
    unittest.main()

import unittest
from ..src.WikifolioDriver import WikifolioDriver, Quarry
import os

class TestInitialization(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = WikifolioDriver(r'C:\Users\Adrian\Documents\GitHub\butterknife\butterknife\test\config.ini', 20)

    def test_login(self):
        self.driver.login()

    @unittest.skip("testing skipping")
    def test_config_parser(self):
        self.assertEqual(self.driver.username, r'***REMOVED***')
        self.assertEqual(self.driver.password, r'***REMOVED***')

    @unittest.skip("testing skipping")
    def test_read_quarries(self):
        self.driver.read_quarries(r'C:\Users\Adrian\Documents\GitHub\butterknife\butterknife\test\quarries.ini')
        self.assertEqual(self.driver.quarries[0], Quarry(*('test2', 2, 'wikifolio-preview-title-link', 'https://www.wikifolio.com/en/int/all-wikifolios/search#/?tags=aktde,akteur,aktusa,akthot,aktint,etf,fonds,anlagezert,hebel&media=true&private=true&assetmanager=true&theme=true&super=true&WithoutLeverageProductsOnly=true&sortOrder=asc&sortBy=aum')))
        
    @unittest.skip("testing skipping")
    def test_scrape_link(self):
        self.driver.scrape_links()
        self.assertEqual(len(self.driver.blocks['test2']), 2)

#    @classmethod
#    def tearDownClass(cls):
#        cls.driver.quit()


if __name__ == '__main__':
    unittest.main()

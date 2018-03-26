import unittest
from ..src.WikifolioDriver import WikifolioDriver, Quarry
import os

class TestInitialization(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = WikifolioDriver(r'C:\Users\Adrian\Documents\GitHub\butterknife\butterknife\test\config.ini', 20)
        cls.driver.login()

    def test_sysconfig_parser(self):
        self.assertEqual(self.driver.username, r'***REMOVED***')
        self.assertEqual(self.driver.password, r'***REMOVED***')

    def test_block_generation(self):
        self.driver.parse_quarries(r'C:\Users\Adrian\Documents\GitHub\butterknife\butterknife\test\quarries.ini')
        self.assertEqual(self.driver.quarries[0], Quarry(*('test2', 2, 'wikifolio-preview-title-link', 'https://www.wikifolio.com/de/de/alle-wikifolios/suche#/?tags=aktde,akteur,aktusa,akthot,aktint,etf,fonds,anlagezert,hebel&media=true&private=true&assetmanager=true&theme=true&super=true&WithoutLeverageProductsOnly=true&sortOrder=asc&sortBy=aum&investable=true&realMoney=true')))
        self.driver.make_blocks_from_quarries()
        self.assertEqual(len(self.driver.blocks['test2']), 2)

    def test_scrape_content(self):
        # Levermann depot
        link = r'https://www.wikifolio.com/de/de/w/wf00quinte'
        row = self.driver.scrape_content(link)
        # Check ISIN
        self.assertEqual(row[0], 'DE000LS9AJF5')

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == '__main__':
    unittest.main()

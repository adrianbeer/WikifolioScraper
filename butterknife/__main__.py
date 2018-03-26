from collections import namedtuple
import csv
from datetime import datetime
import os

from src.WikifolioDriver import WikifolioDriver


def main():

    f_sysconfig = r'C:\Users\Adrian\Documents\GitHub\butterknife\butterknife\src\config.ini'
    f_quarries = r'C:\Users\Adrian\Documents\GitHub\butterknife\butterknife\src\quarries.ini'

    driver = WikifolioDriver(f_sysconfig, 20)
    driver.parse_quarries(f_quarries)
    driver.login()
    driver.make_blocks_from_quarries()

    for key in driver.blocks:
        fn = os.path.join(os.path.dirname(__file__), 'data', key)
        with open(fn + '.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            for link in driver.blocks[key]:
                row = driver.scrape_content(link)
                date = str(datetime.now().date())
                row.insert(0, date)
                writer.writerow(row)
    driver.quit()

if __name__== '__main__':
    main()


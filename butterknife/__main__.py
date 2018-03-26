from collections import namedtuple
from datetime import datetime
import datetime
import csv
import os

from src.WikifolioDriver import WikifolioDriver


def main():
    """---------------------"""
    """Initialize variables """
    """---------------------"""

    f_sysconfig = r'C:\Users\Adrian\Documents\GitHub\butterknife\butterknife\src\config.ini'
    f_quarries = r'C:\Users\Adrian\Documents\GitHub\butterknife\butterknife\src\quarries.ini'

    print(\
    """---------------------"""
    """    Start Running    """
    """---------------------"""
    )

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

    print(\
    """---------------------"""
    """  Finished Running   """
    """---------------------"""
    )


    #-------------- old code -----------------------------------------

    #def scrape_cec(filename, amount, url):
    #      sum_cash_percentage, sum_abs_cash, sum_capital = 0,0,0
    #      with open(filename + '.csv', 'a', newline='') as csvfile:
    #         writer = csv.writer(csvfile, delimiter=';')
    #         for folio in sorted(links, key=lambda x: x[2]):
    #            link = 'https://www.wikifolio.com' + folio
    ###            DECLARING VARIABLES
    #            soup = tire.heat_soup(link)
    #            try:
    #               date, name, isin = str(datetime.now().date()), folio.split('/')[-1], tire.scrape_isin(soup)
    #               invested_capital = tire.scrape_invested_capital(soup).replace(".","").replace(',','.')
    #               weighting = tire.scrape_weighting(soup)
    #               equity = round(float(weighting[0].strip(' %').replace(',','.'))/100, 2)
    #               cash = round(float(weighting[1].strip(' %').replace(',','.'))/100, 2)
    #            except:
    #               print("ERROR OCCURRED")
    #               continue
    #            sum_cash_percentage += cash
    #            sum_abs_cash += cash*float(invested_capital)
    #            sum_capital += float(invested_capital)
    #            
    #            row = [date, name, isin, invested_capital, equity, cash]
    #            print(row)
    #            writer.writerow(row)
    ###            JSON START
    #            with open(filename + '.json', 'r') as f:
    #               json_data = json.load(f)
    #               if isin in json_data['folios']:
    #                  json_data['folios'][isin]['tracking'][date] = {'invested capital':invested_capital,
    #                                                                 'equity':equity,
    #                                                                 'cash':cash}
    #               else:
    #                  json_data['folios'][isin] = {'tracking':{},'name':name}
    #                  json_data['folios'][isin]['tracking'][date] = {'invested capital':invested_capital,
    #                                                                 'equity':equity,
    #                                                                 'cash':cash}
    #               with open(filename + '.json', 'w') as f:  
    #                  f.write(json.dumps(json_data))                                           
    ###            JSON END
    #      cash_mean = sum_cash_percentage/len(links)
    #      agg_cash_mean = sum_abs_cash/sum_capital
    #      with open(filename + '_indicator.csv', 'a', newline='') as csvfile:
    #         writer = csv.writer(csvfile, delimiter=';')
    #         writer.writerow([date, agg_cash_mean, cash_mean])
    #      print('FINISHED SCRAPING PROCESS')         
    #

if __name__== '__main__':
    main()


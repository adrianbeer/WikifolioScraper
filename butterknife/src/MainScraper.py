from collections import namedtuple

from . import WikifolioDriver




driver = WikifolioDriver(config.ini, 20)
#2 options: login or set cookies
# v/

c_portfolio = "//ul[@class='c-wfdetail__tabs-list']/li[1]"
get_stocks = driver.get_text_by_class(c-portfolio__head-label)

#-------------- old code -----------------------------------------

#def scrape_cec(filename, amount, url):
###      INDICATOR INITIALIZATION
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
               equity = round(float(weighting[0].strip(' %').replace(',','.'))/100, 2)
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

def main():


if __name__== '__main__':
    main()


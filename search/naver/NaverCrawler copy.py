import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from ExcelFileReader import ExcelFileReader
from util.util import Find


class NaverCrawler:

    def crawl_search_page(url=None):
        '''Search Page Crawling by keyword'''

        try:
            html = requests.get(url, headers={'User-Agent': 'Moziilla/5.0'})
            return html.content
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback_details = {
                     'filename': exc_traceback.tb_frame.f_code.co_filename,
                     'lineno'  : exc_traceback.tb_lineno,
                     'name'    : exc_traceback.tb_frame.f_code.co_name,
                     'type'    : exc_type.__name__,
                     'message' : str(e)
                    }
            print(traceback_details)
            return ''

    def parse_search_page(self, html_content, pid = 0):
        '''Parse Html Page, and extract key data'''

        mall_list = []
        product_list = []
        price_list = []
        url_list = []
        delivery_list = []

        try:
            soup_obj = BeautifulSoup(html_content, "html.parser")
            tables = soup_obj.find_all("table", {"class": "tbl tbl_v"})
            for table in tables:
                #1 row in 1 table
                tr = table.find("tr")
                print("=======================================================================")
                #find td tags, mall info
                mall_list.append(self._parse_mall_info(tr))
                #Get product name
                td_lft = tr.find("td", {"class": "lft"})
                product_list.append(td_lft.find('a').text)
                #Get price info
                td_price = tr.find("td", {"class": "td_price"}).find('span').text.replace(',', '')
                price_list.append(td_price)
                #Get price url info
                td_url = tr.find("td", {"class": "td_price"}).find('a')['href']
                url_list.append(td_url)
                #Get delivery cost info
                delivery_td = tr.find_all("td")[3]
                delivery_cost = delivery_td.find('p').text.replace('원', '').replace('무료배송', '0').replace(',', '')
                delivery_list.append(delivery_cost)

        except Exception as e:
            print(e)
        
        naver_df = pd.DataFrame(
            {
                'pid' : pid,
                'mall': mall_list,
                'product_name' : product_list,
                'price': price_list,
                'url': url_list,
                'delivery_cost': delivery_list
            }

        )

        return naver_df

    def _parse_mall_info(tr):
        try:
            mall_td = tr.find_all("td")[0]
            return mall_td.find('a')['data-mall-name']
        except:
            return ''

    def run_craweler(self, url, result_df, info_type):
        '''Check url is vaild and extract key data'''

        if "https://search.shopping.naver.com/" in str(url):
            html = self.crawl_search_page(Find(url)[0])
            naver_df = self.parse_search_page(self, html, pid)
            naver_df['type'] = info_type
            result_df = pd.concat([result_df, naver_df], axis = 0,  ignore_index=True)
        return result_df



if __name__ == '__main__':
    data = ExcelFileReader.load('../data/naver_url.pkl')
    result_df = pd.DataFrame()

    crawler = NaverCrawler
    for row in data.values:
        pid= row[0]
        nurl_pg = row[11] #P&G Product url
        nurl_1 = row[30] #Competitor 1 url
        nurl_2 = row[47] #Competitor 2 url

        result_df = NaverCrawler.run_craweler(crawler, nurl_pg, result_df, 'P&G Product')
        result_df = NaverCrawler.run_craweler(crawler, nurl_1, result_df, 'Competitor 1')
        result_df = NaverCrawler.run_craweler(crawler, nurl_2, result_df, 'Competitor 2')

    print(result_df)

    #html = crawler.crawl_search_page(None)
    #crawler.parse_search_page(html)
    
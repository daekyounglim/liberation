import requests
from bs4 import BeautifulSoup
from datetime import datetime
from helper.DBHelper import DBHelper


class NaverCrawler:

    def crawl_search_page(url=None):
        '''Search Page Crawling by keyword'''

        url = "https://search.shopping.naver.com/detail/detail.nhn?cat_id=50002675&nv_mid=18622015409&query=%\
        EB%8B%A4%EC%9A%B0%EB%8B%88&bt=0&frm=NVSCPRO&NaPm=ct%3Dkgky2fdk%7Cci%3D65dc82f4d5793a57fa52533db36eabcb\
        27feb0ef%7Ctr%3Dsls%7Csn%3D95694%7Chk%3D2912c11df428952c7636f6a9b7ee7af59eca5ecc"
        html = requests.get(url, headers={'User-Agent': 'Moziilla/5.0'})
        return html.content

    def parse_search_page(html_content):
        '''Parse Html Page, and extract key data'''

        soup_obj = BeautifulSoup(html_content, "html.parser")
        tables = soup_obj.find_all("table", {"class": "tbl tbl_v"})
        for table in tables:
            tr_list = table.find_all("tr")
            for tr in tr_list:
                print("=======================================================================")
                td = tr.find_all("td")
                mall_td = td[0]
                mall = mall_td.find('a')['data-mall-name']
                print(mall)


if __name__ == '__main__':
    crawler = NaverCrawler
    html = crawler.crawl_search_page(None)
    crawler.parse_search_page(html)


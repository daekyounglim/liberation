import requests
from bs4 import BeautifulSoup
from datetime import datetime
from helper.DBHelper import DBHelper


class CoupangCrawler:

    def crawl_search_page(keyword):
        '''Search Page Crawling by keyword'''

        url = f"https://www.coupang.com/np/search?component=&q={keyword}&rating=0&sorter=scoreDesc&listSize=60"
        html = requests.get(url, headers={'User-Agent': 'Moziilla/5.0'})
        return html.content

    def parse_search_page(html_content):
        '''Parse Html Page, and extract key data'''

        soup_obj = BeautifulSoup(html_content, "html.parser")
        product_list = []

        lis = soup_obj.find("ul", {"id": "productList"}).findAll("li")

        for i, li in enumerate(lis):
            try:
                product = li.find("div", {"class": "name"})

                discount_rate = li.find("div", {"class": "price"}).find(
                    "span", {"class": "instant-discount-rate"}
                )

                base_price = li.find("div", {"class": "price"}).find(
                    "del", {"class": "base-price"}
                )

                price = li.find("em", {"class": "sale"}).find(
                    "strong", {"class": "price-value"}
                )

                product_name = product.text.strip()
                sale_price = price.text.strip()
                base_price_str = sale_price
                discount_rate_str = '0%'

                if base_price is not None:
                    base_price_str = base_price.text.strip()
                if discount_rate is not None:
                    discount_rate_str = discount_rate.text.strip()

                pid = li.find('a')['data-product-id']
                iid = li.find('a')['data-item-id']
                vid = li.find('a')['data-vendor-item-id']
                rank = i + 1

                sale_price = int(sale_price.replace(',', ''))
                discount_rate = int(discount_rate_str.replace('%', ''))
                base_price = int(base_price_str.replace(',', ''))
                brand = product_name.split(' ')[0]
                product = {
                    'site': 'coupang',
                    'keyword': keyword,
                    'brand': brand,
                    'page_id': str(pid),
                    'sub_page_id': str(vid),
                    'page_name': product_name,
                    'base_price': str(base_price),
                    'final_price': str(sale_price),
                    'discount_rate': str(discount_rate),
                    'search_rank': str(rank),
                    'base_date': datetime.now().strftime('%Y-%m-%d')
                }
                product_list.append(product)
            except:
                print(f'Parse Error {i}th element')

        return product_list


if __name__ == '__main__':
    keyword_list = ['팸퍼스', '다우니', '질레트', '오랄비', '페브리즈', '브라운면도기', '기저귀',
                    '섬유유연제', '면도기', '샴푸', '방향제', '칫솔', '전기면도기', '전동칫솔', '팬티기저귀',
                    '신생아기저귀', '아기기저귀', '소형기저귀', '밴드기저귀', '일자형기저귀']

    for keyword in keyword_list:
        crawler = CoupangCrawler
        html = crawler.crawl_search_page(keyword)
        product_list = crawler.parse_search_page(html)
        dbhelper = DBHelper()
        dbhelper.batch_insert(product_list, 'search_rank')


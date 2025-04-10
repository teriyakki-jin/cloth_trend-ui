import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# 셀레니움 초기화 함수
def init_driver():
    options = Options()
    options.add_argument('--headless')  # 창을 띄우지 않음
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    return webdriver.Chrome(service=service, options=options)

# 순위/브랜드/제품명/링크 크롤링
def rbnl(html):
    musinsa_rank_df = pd.DataFrame()

    rank_no_list = [i.text.strip() for i in html.select('#goodsRankList > li > p')]
    brand_list = [i.text.strip() for i in html.select('#goodsRankList > li > div.li_inner > div.article_info > p.item_title > a')]
    link_name_html = html.select('#goodsRankList > li > div.li_inner > div.article_info > p.list_info > a')
    link_list = [i['href'] for i in link_name_html]
    name_list = [i['title'] for i in link_name_html]

    musinsa_rank_df['순위'] = rank_no_list
    musinsa_rank_df['브랜드명'] = brand_list
    musinsa_rank_df['의류명'] = name_list
    musinsa_rank_df['링크'] = link_list

    # 상세 정보 크롤링
    musinsa_detail_df = specific_info(link_list)
    result = pd.concat([musinsa_rank_df, musinsa_detail_df], axis=1)

    return result

# 상세 페이지 크롤링
def specific_info(link_list):
    headers = {'User-Agent': 'Mozilla/5.0'}
    driver = init_driver()

    part_num_list, sex_list, view_list, sales_list, like_list = [], [], [], [], []

    for link in tqdm(link_list):
        try:
            response = requests.get(link, headers=headers)
            html = bs(response.text, 'lxml')

            # 품번
            try:
                part_num_html = html.select_one('#product_order_info > div.explan_product.product_info_section > ul > li:nth-child(1) > p.product_article_contents > strong')
                part_num = part_num_html.get_text().split('/')[-1].strip()
            except:
                part_num = 'N/A'

            # 성별
            try:
                sex_html = html.select('#product_order_info > div.explan_product.product_info_section > ul > li > p.product_article_contents > span.txt_gender')
                sex = sex_html[0].get_text().replace('\n', ' ').strip()
            except:
                sex = 'N/A'

            # 셀레니움으로 동적 정보 가져오기
            driver.get(link)
            time.sleep(1.5)  # 로딩 대기

            sel_html = bs(driver.page_source, 'lxml')

            # 조회수
            try:
                view = sel_html.find("strong", {"id": "pageview_1m"}).get_text()
            except:
                view = 'N/A'

            # 누적판매
            try:
                sales = sel_html.find("strong", {"id": "sales_1y_qty"}).get_text()
            except:
                sales = 'N/A'

            # 좋아요
            try:
                like = sel_html.find("span", {"class": "prd_like_cnt"}).get_text()
            except:
                like = 'N/A'

            part_num_list.append(part_num)
            sex_list.append(sex)
            view_list.append(view)
            sales_list.append(sales)
            like_list.append(like)

        except Exception as e:
            print(f"에러 발생: {e}")
            part_num_list.append('Error')
            sex_list.append('Error')
            view_list.append('Error')
            sales_list.append('Error')
            like_list.append('Error')

    driver.quit()

    return pd.DataFrame({
        '품번': part_num_list,
        '성별': sex_list,
        '조회수(1개월)': view_list,
        '누적판매(1년)': sales_list,
        '좋아요수': like_list
    })

# 전체 함수
def musinsa_rank(category_num=1, page_num=1):
    url = f"https://www.musinsa.com/ranking/best?period=now&age=ALL&mainCategory=00{category_num}&subCategory=&leafCategory=&price=&golf=false&kids=false&newProduct=false&exclusive=false&discount=false&soldOut=false&page={page_num}&viewType=small&priceMin=&priceMax="
    response = requests.get(url)
    html = bs(response.text, 'lxml')
    return rbnl(html)

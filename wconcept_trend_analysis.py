from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# 브랜드별 스타일 수동 매핑
style_dict = {
    "망고매니플리즈": "Minimal",
    "닐바이피": "Y2K",
    "주르티": "Street",
    "미나수": "Casual",
    "몽돌": "Minimal",
    "시야쥬": "Casual",
    "룩캐스트": "Feminine",
    "리엘": "Romantic",
    "아틀리에 나인": "Modern"
}

def crawl_wconcept_full(keyword="여름"):
    options = Options()
    options.add_argument("--headless")  # 브라우저 안 띄우기
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = f"https://www.wconcept.co.kr/Search?keyword={keyword}"
    driver.get(url)
    time.sleep(5)  # 페이지 로딩 대기

    product_items = driver.find_elements(By.CSS_SELECTOR, "div.product-item")

    brand_list = []
    name_list = []
    price_list = []
    image_url_list = []
    style_list = []

    for item in product_items:
        try:
            brand = item.find_element(By.CSS_SELECTOR, "span.text.title").text.strip()
            name = item.find_element(By.CSS_SELECTOR, "span.text.detail").text.strip()
            price = item.find_element(By.CSS_SELECTOR, "span.text.final-price strong").text.strip().replace(",", "")
            img_tag = item.find_element(By.CSS_SELECTOR, "img")
            image_url = img_tag.get_attribute("src").split("?")[0] if img_tag else ""
            style = style_dict.get(brand, "Other")

            brand_list.append(brand)
            name_list.append(name)
            price_list.append(price)
            image_url_list.append(image_url)
            style_list.append(style)
        except Exception as e:
            print("Error:", e)
            continue

    driver.quit()

    df = pd.DataFrame({
        "brand": brand_list,
        "name": name_list,
        "price": price_list,
        "style": style_list,
        "image_url": image_url_list
    })

    df.to_csv("wconcept_products.csv", index=False, encoding="utf-8-sig")
    print("✅ CSV 저장 완료: wconcept_products.csv")

# 실행
crawl_wconcept_full("여름")

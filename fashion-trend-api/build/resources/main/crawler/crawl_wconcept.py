import os
import shutil
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys

# Save paths
IMAGE_DIR = "./static/images"
CSV_PATH = os.path.join(os.path.dirname(__file__), "wconcept_products.csv")


# Reset old data
def reset_previous_data():
    if os.path.exists(IMAGE_DIR):
        shutil.rmtree(IMAGE_DIR)
        print(" Image directory cleaned!")
    os.makedirs(IMAGE_DIR, exist_ok=True)

    if os.path.exists(CSV_PATH):
        os.remove(CSV_PATH)
        print(" CSV file reset!")


# Manual brand-style mapping
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

def download_image(url, filename):
    path = os.path.join(IMAGE_DIR, filename)
    if os.path.exists(path):
        print(f" Skipping duplicate image: {filename}")
        return True

    try:
        print(f" Downloading image: {url}")
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            with open(path, "wb") as f:
                f.write(response.content)
            print(f" Image saved: {filename}")
            return True
        else:
            print(f" Status code {response.status_code}: {url}")
    except Exception as e:
        print(f" Download failed: {url} → {e}")
    return False


def crawl_wconcept_and_download(keyword="summer clothes"):
    print(f" Starting crawl with keyword: {keyword}")
    reset_previous_data()

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    url = f"https://www.wconcept.co.kr/Search?keyword={keyword}"
    driver.get(url)

    for i in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    product_items = driver.find_elements(By.CSS_SELECTOR, "div.product-item")
    print(f" Total products found: {len(product_items)}")

    brand_list = []
    name_list = []
    price_list = []
    style_list = []
    image_name_list = []

    seen_names = set()
    idx = 0

    for item in product_items:
        try:
            brand = item.find_element(By.CSS_SELECTOR, "span.text.title").text.strip()
            name = item.find_element(By.CSS_SELECTOR, "span.text.detail").text.strip()
            price = item.find_element(By.CSS_SELECTOR, "span.text.final-price strong").text.strip().replace(",", "")

            if name in seen_names:
                print(f" Duplicate product, skipped: {name}")
                continue
            seen_names.add(name)

            print(f"\n Product {idx+1}: {brand} | {name} | ₩{price}")

            img_tag = item.find_element(By.CSS_SELECTOR, "img")
            image_url = img_tag.get_attribute("src")

            if not image_url or "data:image" in image_url:
                image_url = (
                    img_tag.get_attribute("data-src") or
                    img_tag.get_attribute("data-original") or
                    img_tag.get_attribute("srcset") or
                    img_tag.get_attribute("data-srcset") or
                    ""
                )

            if not image_url or "data:image" in image_url:
                print(" Invalid image URL, skipped")
                continue

            style = style_dict.get(brand, "Other")
            image_name = f"product_{idx}.jpg"

            if download_image(image_url, image_name):
                brand_list.append(brand)
                name_list.append(name)
                price_list.append(price)
                style_list.append(style)
                image_name_list.append(image_name)
                idx += 1
            else:
                print("⚠ Image failed to save, skipped")

        except Exception as e:
            print(" Error during item processing:", e)
            continue

    driver.quit()
    df = pd.DataFrame({
        "brand": brand_list,
        "name": name_list,
        "price": price_list,
        "style": style_list,
        "image_file": image_name_list
    })

    df.to_csv(CSV_PATH, index=False, encoding="utf-8-sig")
    print(f"\n CSV saved successfully! Total products: {len(df)}")


# Run if directly executed
if __name__ == "__main__":
    if len(sys.argv) >= 2:
        keyword = sys.argv[1]
    else:
        keyword = "summer"

    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    crawl_wconcept_and_download(keyword)

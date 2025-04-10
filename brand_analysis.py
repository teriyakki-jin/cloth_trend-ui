
# brand_analysis.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import pandas as pd

# ✅ Set Korean font (Windows)
font_path = "C:/Windows/Fonts/malgun.ttf"
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc("font", family=font_name)

# Step 1: Crawl brand and product names
def crawl_brand_product(keyword="여름"):
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = f"https://www.wconcept.co.kr/Search?keyword={keyword}"
    driver.get(url)
    time.sleep(5)

    brand_elements = driver.find_elements(By.CSS_SELECTOR, "span.text.title")
    product_elements = driver.find_elements(By.CSS_SELECTOR, "span.text.detail")

    brand_names = [e.text.strip() for e in brand_elements if e.text.strip()]
    product_names = [e.text.strip() for e in product_elements if e.text.strip()]

    driver.quit()

    return [{"브랜드": b, "상품명": p} for b, p in zip(brand_names, product_names)]

# Step 2: Analyze brand frequency
def analyze_brands(data):
    df = pd.DataFrame(data)
    top_brands = df['브랜드'].value_counts().head(10)

    # Bar chart
    top_brands.plot(kind='bar', color='lightcoral')
    plt.title("상위 브랜드 TOP 10")
    plt.xlabel("브랜드")
    plt.ylabel("상품 수")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Run
if __name__ == "__main__":
    print("📦 브랜드 및 상품명 수집 중...")
    data = crawl_brand_product("여름")

    if data:
        print(f"✅ 총 {len(data)}개 상품 수집 완료")
        analyze_brands(data)
    else:
        print("❌ 데이터를 수집하지 못했습니다.")

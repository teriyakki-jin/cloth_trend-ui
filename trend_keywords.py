
# trend_keywords.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from matplotlib import font_manager, rc
import time
import re
import matplotlib.pyplot as plt
from collections import defaultdict

font_path = "C:/Windows/Fonts/malgun.ttf"
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

# Step 1: Crawl product names
def crawl_product_names(keyword="여름"):
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = f"https://www.wconcept.co.kr/Search?keyword={keyword}"
    driver.get(url)
    time.sleep(5)

    elements = driver.find_elements(By.CSS_SELECTOR, "span.text.detail")
    product_names = [elem.text.strip() for elem in elements if elem.text.strip() != ""]

    driver.quit()
    return product_names

# Step 2: Define keyword dictionaries
color_keywords = ["블랙", "화이트", "아이보리", "베이지", "핑크", "블루", "네이비", "민트", "카키", "그레이", "브라운", "옐로우"]
material_keywords = ["린넨", "코튼", "니트", "울", "시스루", "데님", "골지", "실크", "레이스"]
item_keywords = ["티셔츠", "셔츠", "팬츠", "원피스", "블라우스", "자켓", "가디건", "맨투맨", "후드", "스커트"]

# Step 3: Keyword frequency analysis
def keyword_analysis(product_names, keywords):
    count_dict = defaultdict(int)
    for name in product_names:
        clean = re.sub(r"[^가-힣a-zA-Z]", " ", name)
        for keyword in keywords:
            if keyword.lower() in clean.lower():
                count_dict[keyword] += 1
    return dict(sorted(count_dict.items(), key=lambda x: x[1], reverse=True))

# Step 4: Visualization
def show_bar_chart(counter_dict, title):
    plt.figure(figsize=(10, 4))
    plt.bar(counter_dict.keys(), counter_dict.values(), color='skyblue')
    plt.title(title)
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Run
if __name__ == "__main__":
    print("📦 Crawling product names...")
    product_names = crawl_product_names("여름")

    if product_names:
        print(f"✅ Collected {len(product_names)} product names")
        color_result = keyword_analysis(product_names, color_keywords)
        material_result = keyword_analysis(product_names, material_keywords)
        item_result = keyword_analysis(product_names, item_keywords)

        print("🎨 Visualizing colors...")
        show_bar_chart(color_result, "Top Colors")

        print("🧵 Visualizing materials...")
        show_bar_chart(material_result, "Top Materials")

        print("👕 Visualizing items...")
        show_bar_chart(item_result, "Top Items")
    else:
        print("❌ Failed to fetch products.")

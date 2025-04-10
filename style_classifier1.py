
# style_classifier.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Step 1: Crawl product names from W Concept
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

# Step 2: Define style categories with keywords
style_keywords = {
    "Street": ["크롭", "하이웨스트", "오버핏", "백프린팅", "조거"],
    "Minimal": ["린넨", "심플", "노카라", "단색", "슬랙스"],
    "Y2K": ["체인", "주얼리", "레이어드", "배꼽", "스팽글", "글리터"],
    "Feminine": ["시스루", "레이스", "프릴", "플라워", "뷔스티에"],
    "Classic": ["블레이저", "셔츠", "코튼", "트렌치", "니트"],
    "Casual": ["티셔츠", "맨투맨", "팬츠", "데님", "후드"]
}

# Step 3: Classify product name by style
def classify_style(product_names):
    result = []
    for name in product_names:
        matched_styles = []
        for style, keywords in style_keywords.items():
            for word in keywords:
                if word.lower() in name.lower():
                    matched_styles.append(style)
                    break
        if not matched_styles:
            matched_styles.append("Other")
        result.append({"Product Name": name, "Style": ", ".join(matched_styles)})
    return result

# Step 4: Visualize style distribution
def visualize_style_distribution(classified_data):
    df = pd.DataFrame(classified_data)
    style_counts = df['Style'].value_counts()

    # Bar chart
    style_counts.plot(kind='bar', color='skyblue')
    plt.title("Style Distribution")
    plt.xlabel("Style")
    plt.ylabel("Number of Products")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Word cloud
    wordcloud = WordCloud(
        font_path="C:/Windows/Fonts/malgun.ttf",  # Windows Korean font path
        background_color="white",
        width=800,
        height=400
    ).generate_from_frequencies(style_counts)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Style WordCloud")
    plt.show()

# Run
if __name__ == "__main__":
    print("📦 Crawling product names...")
    product_names = crawl_product_names("여름")
    if product_names:
        print(f"✅ Collected {len(product_names)} product names")
        classified = classify_style(product_names)
        print("📊 Visualizing style distribution...")
        visualize_style_distribution(classified)
    else:
        print("❌ Failed to fetch products.")

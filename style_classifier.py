
# style_classifier.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from wordcloud import WordCloud
import time
import re
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt



# 워드클라우드 생성 (한글 폰트 경로 지정)
wordcloud = WordCloud(
    font_path="C:/Windows/Fonts/malgun.ttf",  # ✅ 윈도우 기본 한글 폰트
    background_color="white",
    width=800,
    height=400
).generate_from_frequencies(counter)


# Step 1: 상품명 크롤링
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

# Step 2: 스타일 분류
style_keywords = {
    "스트릿": ["크롭", "하이웨스트", "오버핏", "백프린팅", "조거"],
    "미니멀": ["린넨", "심플", "노카라", "단색", "슬랙스"],
    "Y2K": ["체인", "주얼리", "레이어드", "배꼽", "스팽글", "글리터"],
    "페미닌": ["시스루", "레이스", "프릴", "플라워", "뷔스티에"],
    "클래식": ["블레이저", "셔츠", "코튼", "트렌치", "니트"],
    "캐주얼": ["티셔츠", "맨투맨", "팬츠", "데님", "후드"]
}

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
            matched_styles.append("기타")
        result.append({"상품명": name, "스타일": ", ".join(matched_styles)})
    return result

# Step 3: 스타일 분포 시각화
def visualize_style_distribution(classified_data):
    df = pd.DataFrame(classified_data)
    style_counts = df['스타일'].value_counts()

    style_counts.plot(kind='bar', color='skyblue')
    plt.title("스타일 분포")
    plt.xlabel("스타일")
    plt.ylabel("상품 수")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# 실행
if __name__ == "__main__":
    print("📦 상품명 크롤링 중...")
    product_names = crawl_product_names("여름")
    if product_names:
        print(f"✅ 상품명 {len(product_names)}개 수집 완료")
        classified = classify_style(product_names)
        print("📊 스타일 분포 시각화 시작!")
        visualize_style_distribution(classified)
    else:
        print("❌ 상품을 가져오지 못했습니다.")

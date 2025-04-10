# wconcept_trend_analysis.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Step 1: W Concept에서 상품명 크롤링
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

# Step 2: 키워드 분석
def extract_keywords(product_names):
    keywords = []
    for name in product_names:
        clean = re.sub(r"\[.*?\]", "", name)  # [태그] 제거
        clean = re.sub(r"[^가-힣a-zA-Z]", " ", clean)  # 특수문자 제거
        clean = re.sub(r"\s+", " ", clean).strip()  # 공백 정리
        keywords.extend(clean.split())
    return Counter(keywords)

# Step 3: 워드클라우드 시각화
def draw_wordcloud(counter):
    wordcloud = WordCloud(
        font_path="malgun.ttf",  # Windows 한글 폰트
        background_color="white",
        width=800,
        height=400
    ).generate_from_frequencies(counter)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("W Concept 패션 트렌드 워드클라우드", fontsize=16)
    plt.show()

# 실행
if __name__ == "__main__":
    print("📦 상품명 크롤링 중...")
    products = crawl_product_names("여름")

    if products:
        print(f"✅ 상품명 {len(products)}개 수집 완료")
        print("🧠 키워드 분석 중...")
        keyword_counter = extract_keywords(products)
        print("🎨 워드클라우드 시각화 시작")
        draw_wordcloud(keyword_counter)
    else:
        print("❌ 상품을 가져오지 못했습니다.")

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# 크롬 옵션 설정
options = Options()
options.add_argument("--start-maximized")
options.add_argument("user-agent=Mozilla/5.0")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# 드라이버 실행
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    })
    """
})

# 무신사 랭킹 페이지 접속
url = "https://www.musinsa.com/main/musinsa/ranking?storeCode=musinsa&sectionId=200&categoryCode=000"
driver.get(url)
time.sleep(5)  # 초기 로딩 대기

# ⬇️ 스크롤 내려서 동적 데이터 강제 로딩
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)  # 렌더링 기다림

# 상품 요소 수집
items = driver.find_elements(By.CSS_SELECTOR, "#goodsRankList > li")

print(f"📦 상품 수: {len(items)}개")

data = []
for item in items:
    try:
        brand = item.find_element(By.CLASS_NAME, "item_title").text.strip()
        name = item.find_element(By.CLASS_NAME, "list_info").text.strip()
        link = item.find_element(By.CLASS_NAME, "list_info").find_element(By.TAG_NAME, "a").get_attribute("href")
        price = item.find_element(By.CLASS_NAME, "price").text.strip().replace("\n", " ")
        data.append({
            "브랜드": brand,
            "상품명": name,
            "링크": link,
            "가격": price
        })
    except Exception as e:
        print("❗ 항목 처리 중 오류:", e)

driver.quit()

# CSV 저장
df = pd.DataFrame(data)
df.to_csv("musinsa_ranking.csv", index=False, encoding="utf-8-sig")

print(f"✅ {len(df)}개의 상품 정보 저장 완료! ➡️ musinsa_ranking.csv")

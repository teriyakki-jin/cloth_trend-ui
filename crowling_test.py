from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.add_argument("--start-maximized")
# options.add_argument("--headless")  # 창 안 띄우고 싶으면 주석 해제

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# W Concept 여름 키워드 검색 페이지 접속
driver.get("https://www.wconcept.co.kr/Search?keyword=여름")
time.sleep(5)  # 페이지 렌더링 대기

# 상품명 추출 (클래스 이름 기반)
elements = driver.find_elements(By.CSS_SELECTOR, "span.text.detail")

print("🔥 W Concept 상품명 리스트:")
for i, elem in enumerate(elements[:10]):
    print(f"{i+1}. {elem.text.strip()}")

driver.quit()

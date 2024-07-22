## 크롤링해야하는 카테고리별 링크 dict

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium_sets import driver
import time, json


# 오류메시지 출력
import traceback
driver = driver()

## 크롤링
items = [] # 수집장소
BASE_URL = "https://hotping.co.kr"
driver.get(BASE_URL)
time.sleep(3)
try:
    cat_box = driver.find_element(By.CLASS_NAME, 'postion')
    cat_link = [c.get_attribute('href') for c in cat_box.find_elements(By.TAG_NAME, 'a')[7:12]] # 상의만 크롤링할 것 (원피스, 아우터, 상의, 니트, 셔츠)
    for c in cat_link: # 카테고리별
        driver.get(c)
        time.sleep(5) # 대기 
        cat = driver.find_element(By.CLASS_NAME, 'titleArea').text
        # 5페이지씩만 크롤링 (총 300개)
        page_box = driver.find_element(By.CLASS_NAME, 'ec-base-paginate')
        page = page_box.find_element(By.TAG_NAME, 'ol')
        page_a = page.find_elements(By.TAG_NAME, 'a')
        pages = [p.get_attribute('href') for p in page_a]
        for p in pages: # 페이지별로 크롤링
            driver.get(p)
            time.sleep(3) # 대기
            product_box = driver.find_element(By.CLASS_NAME,'xans-product-listnormal')
            products = product_box.find_elements(By.CLASS_NAME, 'box')
            for product in products: # 상품별
                link = product.find_element(By.TAG_NAME, 'a').get_attribute('href') # 상품링크
                img = product.find_element(By.TAG_NAME, 'img').get_attribute('src') # 이미지
                name = product.find_element(By.CLASS_NAME, 'name')
                item = name.find_element(By.TAG_NAME, 'a').text
                lis = product.find_elements(By.TAG_NAME, 'li')
                if len(lis) == 4:
                    price = lis[1].text
                    price = price.replace(',', '').replace('원', '')[:5]
                else:
                    price = lis[0].text
                    price = price.replace(',', '').replace('원', '')
                price = int(price)
                items.append({
                    'cat': cat,
                    'name': item,
                    'img': img,
                    'price': price,
                    'link': link
                })
    driver.quit() # 드라이버 해제
    print(items[0])
    print(f'아이템 수: {len(items)}')  
    # json 파일 생성 및 저장
    with open('./items.json', 'w', encoding='utf-8') as file:
        json.dump(items, file, ensure_ascii=False, indent=2) # ensure_ascii: 비 ascii 문자 그대로 ,indent: 들여쓰기 적용
except:
    if len(items) > 0:
        print(items[0])  
        # 크롤링 된 만큼만 json 파일 생성 및 저장
        with open('./items.json', 'w', encoding='utf-8') as file:
            json.dump(items, file, ensure_ascii=False, indent=2) # ensure_ascii: 비 ascii 문자 그대로 ,indent: 들여쓰기 적용
    print(traceback.format_exc()) # 오류 메시지 출력
    driver.quit() # 중간에 오류난 경우 드라이버 해제해주기   
    
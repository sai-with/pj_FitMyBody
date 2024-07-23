from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium_sets import driver
import pandas as pd
import time, json


# 오류메시지 출력
import traceback
# 드라이버 불러오기
driver = driver()

# link 가져오기
items_link = pd.read_json('./items_link.json')

## 크롤링
review_list = [] # 수집장소
try:
    for item_id, link in items_link.itertuples(index=False, name=None): # name=None return regular tuples 
        driver.get(link) # 제품 상세페이지 접속
        time.sleep(3) # 대기
        info_dict = dict()
        info_dict['item_id'] = item_id
        # 리뷰 버튼
        review_bar = driver.find_element(By.CLASS_NAME,'menu')
        
        # 페이징을 위해 리뷰 개수 파악하기
        n_review = review_bar.find_element(By.TAG_NAME, 'span').text
        n_review = n_review.replace('(', '').replace(')', '').astype(int)
        
        review = review_bar.find_elements(By.TAG_NAME, 'li')[1] # 두번째 탭이 구매후기
        review_a = review.find_element(By.TAG_NAME, 'a').get_attribute('href') # 구매후기 링크
        
        driver.get(review_a) # 리뷰 페이지 접속
        # 페이지당 리뷰 5개
        if n_review != 0: # 리뷰데이터가 있는경우
            while n_review > 0: 
                n_review -= 5
                button = driver.find_element(By.CLASS_NAME, 'pagination__button--next')
                review_box = driver.find_element(By.CLASS_NAME, 'reviews')
                reviews = review_box.find_elements(By.TAG_NAME, 'li')
                for review in reviews:
                    info_dict['평소사이즈'] = None # 값이 없는 경우 결측치로 넘기기 위해
                    left = review.find_element(By.CLASS_NAME, 'review_list_v2__review_lcontent')
                    right = review.find_element(By.CLASS_NAME, 'review_list_v2__review_rcontent')
                    if right.find_element(By.TAG_NAME, 'b').text == '네이버 페이 구매자': # 고객 정보 없는 경우
                        pass
                    else:
                        if left.find_element(By.CLASS_NAME, 'review_list_v2__score_text').text == '아주 좋아요': # 별점 5개인 리뷰만 수집
                            infos = right.find_elements(By.CLASS_NAME, 'review_options_v2__option')
                            for info in infos:
                                key, value = info.find_elements(By.TAG_NAME, 'span')
                                info[key.text] = value.text
                            
                    review_list.append(info_dict)
                button.click() # 다음 페이지 이동
        
except:
    driver.quit()
        
    
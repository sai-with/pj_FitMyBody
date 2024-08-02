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
'''
08/02 idx:23 '''
items_link = pd.read_json('./items_link.json')

## 크롤링
def get_value(item_id, n_review, review_list):
    
    def get_detail():
        # 리뷰 구역
        review_content = driver.find_element(By.CLASS_NAME, 'products_reviews_list')
        review_box = review_content.find_element(By.CLASS_NAME, 'reviews')
        # 리뷰들(페이지당 리뷰 5개)
        reviews = review_box.find_elements(By.CLASS_NAME, 'review_list_v2')
        for review in reviews: # 각 리뷰마다
            keys = ['품번', '아이디', '별점', '키', '몸무게', '평소사이즈', '타입', '리뷰']
            vals = [item_id, None, None, None, None, None, None, None] # 값이 없는 경우 결측치로 넘김
            info_dict = dict(zip(keys, vals)) # 딕셔너리 생성
            # 리뷰 수집
            left = review.find_element(By.CLASS_NAME, 'review_list_v2__review_lcontent')
            right = review.find_element(By.CLASS_NAME, 'review_list_v2__review_rcontent')
            customer = right.find_element(By.TAG_NAME, 'b').text
            if customer == '네이버 페이 구매자': # 고객 정보 없는 경우
                pass
            else: # 품번, 리뷰 아이디, 별점, 키, 몸무게, 평소사이즈, 구매 타입(색상, 사이즈)
                star_content = left.find_element(By.CLASS_NAME, 'review_list_v2__score_star')
                star = star_content.find_element(By.TAG_NAME, 'span').text
                star = star.strip('별점: ') # strip은 양쪽 방향에서 제거 -> 중간에 있는 문자 제거 불가
                star = int(star) # 정수 변환
                info_dict['별점'] = star # 별점 입력
                
                comments = left.find_element(By.CLASS_NAME, 'review_list_v2__message').text
                comment = comments.strip('\n') # 줄바꿈 제거
                info_dict['리뷰'] = comment # 리뷰 입력
                
                user_id = right.find_element(By.TAG_NAME, 'b').text
                user_id = user_id.strip('*')
                info_dict['아이디'] = user_id # 아이디 입력
                
                infos = right.find_elements(By.CLASS_NAME, 'review_options_v2__option')
                for info in infos:
                    key, value = info.find_elements(By.TAG_NAME, 'span') # ex) span[0]:키, span[1]:165~170
                    key = key.text
                    value = value.text
                    info_dict[key] = value # 키, 몸무게, 평소사이즈, 타입 입력
                review_list.append(info_dict) # 수집장소에 추가
        return review_list
    
    
    if n_review <= 5: # 페이징 불필요
        review_list = get_detail()
    elif n_review > 5: # 페이징 필요
        while n_review > 0: 
            # 페이징 버튼
            button = driver.find_element(By.CLASS_NAME, 'pagination__button--next')
            n_review -= 5
            review_list = get_detail()
            if n_review > 0: # 남은 페이지가 있으면
                button.click() # 다음 페이지 이동
                time.sleep(2) # 대기
        
    return review_list

def scrap(data):
    review_list = [] # 수집장소
    try:
        for item_id, link in data.itertuples(index=False, name=None): # name=None return regular tuples 
            url = link + '#prdReview'
            driver.get(url) # 리뷰 페이지 접속
            time.sleep(3) # 대기
            # 리뷰 버튼
            review_bar = driver.find_element(By.CLASS_NAME,'menu')
            
            # 페이징을 위해 리뷰 개수 파악하기
            n_review = review_bar.find_element(By.TAG_NAME, 'span').text
            n_review = n_review.strip('()') # ex) (1,225)
            n_review = n_review.replace(',', '')
            n_review = int(n_review)
            if n_review == 0: # 리뷰없으면
                pass
            # iframe 접근(리뷰창)
            iframe = driver.find_element(By.ID, 'crema-product-reviews-3')
            driver.switch_to.frame(iframe) # 리뷰 iframe으로 이동
            review_list = get_value(item_id, n_review, review_list)
            
        driver.quit() # 브라우저 종료
        print('수집한 리뷰 개수: ', len(review_list)) # 수집한 리뷰 개수
        with open('../Transform/reviews.json', 'a', encoding='utf-8') as file: # 파일 이어쓰기
            json.dump(review_list, file, ensure_ascii=False, indent=2) # 한글깨짐 방지, 들여쓰기
        
    except:
        driver.quit() # 브라우저 종료
        with open('../Transform/reviews.json', 'a', encoding='utf-8') as file: # 파일 이어쓰기
            json.dump(review_list, file, ensure_ascii=False, indent=2) # 한글깨짐 방지, 들여쓰기
        print(review_list[-1])
        print('수집한 데이터\n', len(review_list))
        print(traceback.format_exc()) # 오류 메시지 출력
scrap(items_link.iloc[24:50])

    
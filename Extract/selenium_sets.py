from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def driver():
    ## Chrome Options
    # 브라우저 꺼짐 방지
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    # 불필요한 에러 메세지 없애기
    chrome_options.add_experimental_option("excludeSwitches" , ["enable-logging"])
    # 창 최대화
    chrome_options.add_argument("--start-maximized")

    ## driver 설정
    auto_driver = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=auto_driver, options=chrome_options)
    return driver
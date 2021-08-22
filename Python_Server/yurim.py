from selenium import webdriver
import json
import math
import statistics
import requests


#공적대출 금리 스크래핑
def publicloan():
    #브라우저가 크롤링 하는것을 새창으로 띄우지 않고 뒤에서 돌아가도록 숨기는 코드
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless') 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("lang=ko_KR")
    chrome_options.add_argument("user-agent")
    driver = webdriver.Chrome('./chromedriver', chrome_options=chrome_options)
    driver.implicitly_wait(3)
    chrome_options.add_argument('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    loanpercen=""
    driver.get("https://search.naver.com/search.naver?where=nexearch&query=cd%EA%B8%88%EB%A6%AC&ie=utf8&sm=tab_she&qdt=0")
    driver.implicitly_wait(3)
    loanpercen=driver.find_element_by_xpath('//*[@id="_cs_root"]/div[1]/div/h3/a/span[2]/strong').text #변동금리
    loanpercenint=float(loanpercen)+2.444 #변동금리 + 가산금리
    # json_loanpercenint = json.dumps(loanpercenint) #이건 안해도 jsonify에서 하면 되겠즤?
    
    return loanpercenint #대출금리

##########################################################
method = 'month' # 대출기간 년 / 개월

def publicloanmonth():
    u2 = 10000000 # 대출금액
    u3 = 3 #개월
    u4  = publicloan() # 연이자율
    
    publicloanmonthpay=(u2*u4*0.01)*2/24
    # round(publicloanmonth,1)
    json_publicloanmonthpay=json.dumps(publicloanmonthpay)
    
    return json_publicloanmonthpay #거치기간 월 이자액


#공적대출은 원금 균등방법으로 상환한다.
def cal_principal(u2, u3, u4, method ):
    u2 = 10000000 # 대출금액
    u3 = 3 #개월
    u4  = publicloan() # 연이자율
    
    if method == 'year':
        u3 = u3 * 12
    URL = "https://m.search.naver.com/p/csearch/content/apirender.nhn?_callback=window.__jindo2_callback._8881&q=대출이자계산기&where=m&pkid=69&u1=interest3&u2={}&u3={}&u4={}&u5=principal&u6=all".format(u2, u3, u4)
   
    response = requests.get(URL)
    text = response.text
    sub_text = text[text.index('{'):text.index(')')]
    dic = json.loads(sub_text)
    cnt = 1 # 납입회차
    total_interest = 0 # 총 대출이자
    monthRe = []

    for data in dic['result']:
        # print(f"count: {cnt} data: {data}")
        total_interest += int(data['interest'].replace("'", "").replace(",", ""))
        cnt += 1
        monthRe.append(int(data['monthRepay'].replace("'", "").replace(",", "")))
           # 평균 월상환금,          최소 월상환금, 최대 월 상환금
    print(round(statistics.mean(monthRe)), round(min(monthRe)), round(max(monthRe)))
    return round(statistics.mean(monthRe))
    
# print(publicloanmonth())
# cal_principal(10000000, 3, publicloan(), 'year' )
# print(type(cal_principal(u2,u3,u4,method))) (edited) 
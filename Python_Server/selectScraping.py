# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import datetime
import json
import requests
import math
import statistics

import time


def hi():
    List = []
    resList = []
    Ret= []
    driver = webdriver.Chrome('./chromedriver')
    # driver.implicitly_wait(10000)
    driver.get('http://finlife.fss.or.kr/creditfacility/selectCreditfacility.do?menuId=2000104')
    # driver.implicitly_wait(10000)
    driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[1]/div[3]/ul/li[2]/button').click()
    driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[1]/button').click()
    driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[1]/div[3]/ul/li[2]/button').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[1]/button').click()
    time.sleep(2)
    table = driver.find_element_by_xpath('//*[@id="ajaxResult"]/div[1]/table').find_element_by_tag_name('tbody')
    time.sleep(1)
    print("----------------------종료")
    # 상위 10개 row만 받아옴

    for i in range (99):
        # print(table.find_elements_by_tag_name("td")[i].text)
        List.append(table.find_elements_by_tag_name("td")[i].text)
    snum = 0
    enum= 11 # 정제 전 row size =11
    for i in range (9):
        resList.append(List[snum:enum]) # 슬라이싱
        snum = enum
        enum +=11
    # 고객 신용 등급
    # 1: 1~2등급, 2: 3~4등급,  3: 5~6등급,  4: 7~8등급,  5: 9~10등급
    trustGrade = 1 # 고객 신용 등급이 1~2일 때
    trustGrade += 2 
    bank = []
    rate = []
    temp = 0
    for i in range (9):
        bank.append(resList[i][0])
        temp=resList[i][trustGrade]
        temp = float(temp[:-1])
        rate.append(temp)
    Ret.append(bank)
    Ret.append(rate)
    dicData = {} # 딕셔너리 데이터
    dicData['bank'] = Ret[0]
    dicData['rate'] = Ret[1]
    
    JSON_VAL = json.dumps(dicData,ensure_ascii = False)
    print("hi 함수 작동 ")
    print(type(JSON_VAL)) #str로 찍힘 
    print(JSON_VAL)
    return JSON_VAL


#1. 원리금 균등방법 :: 빌린돈과 이자를 합한 금액을 똑같이 나눠서 갚는 방식
def cal_principal_interest(u2, u3, u4, method = 'year'):
    if method == 'year':
        u3 = u3 * 12
    URL = "https://m.search.naver.com/p/csearch/content/apirender.nhn?_callback=window.__jindo2_callback._8881&q=대출이자계산기&where=m&pkid=69&u1=interest3&u2={}&u3={}&u4={}&u5=principal_interest&u6=all".format(u2, u3, u4)
    response = requests.get(URL)
    text = response.text
    sub_text = text[text.index('{'):text.index(')')]
    dic = json.loads(sub_text)
    cnt = 1 # 납입회차
    total_interest = 0 # 총 대출이자
    totalRe = []
    for data in dic['result']:
        #print(f"count: {cnt} data: {data}")
        total_interest += int(data['interest'].replace("'", "").replace(",", ""))
        cnt += 1
        totalRe.append(int(data['monthRepay'].replace("'", "").replace(",", "")))
    # 총이자액, 총 상환금액   
    return total_interest, sum(totalRe)
#2. 원금 균등방법 :: 빌린돈을 똑같이 나눠서 갚는 방식
def cal_principal(u2, u3, u4, method ):
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
        #print(f"count: {cnt} data: {data['monthRepay']}")
        total_interest += int(data['interest'].replace("'", "").replace(",", ""))
        cnt += 1
        monthRe.append(int(data['monthRepay'].replace("'", "").replace(",", "")))
    # 총 이자액, 평균 월상환금, 최소 월상환금, 최대 월 상환금
    return total_interest, statistics.mean(monthRe), min(monthRe), max(monthRe)
#3. 만기일시방법 :: 마지막에 빌린돈을 한번에 갚는 방식
def cal_expire(u2, u3, u4, method ):
    if method == 'year':
        u3 = u3 * 12 
    URL = "https://m.search.naver.com/p/csearch/content/apirender.nhn?_callback=window.__jindo2_callback._8881&q=대출이자계산기&where=m&pkid=69&u1=interest3&u2={}&u3={}&u4={}&u5=expire&u6=all".format(u2, u3, u4)
    response = requests.get(URL)
    text = response.text
    sub_text = text[text.index('{'):text.index(')')]
    dic = json.loads(sub_text)
    total_interest =dic['result']['totalInterest'].replace(",", "")
    money = u2 + int(total_interest)
    # 총 이자액, 총 상환금액
    return int(total_interest), money

# varia = hi()
# dic_var = json.loads(varia)
# amount = 1000000 # 대출금액
# period = 3       # 대출기간
# method = 'month' # 대출기간 년 / 개월
# for i in range(len(dic_var['bank'])):
#      rate  = dic_var['rate'][i] # 연이자율

def fin():  # 챗봇에서 받은 신용등급이랑 
    varia = hi()
    dic_var = json.loads(varia)
    amount = 1000000 # 대출금액
    period = 3       # 대출기간
    method = 'month' # 대출기간 년 / 개월
    for i in range(len(dic_var['bank'])):
        rate  = dic_var['rate'][i] # 연이자율
    re = []
    nn = dic_var['bank']
    for i in range(len(nn)):
        #print(nn[i]) # 은행이름
        rate  = dic_var['rate'][i] # 연이자율
        a, b = cal_principal_interest(amount, period, rate, method)
        c, d, e, f = cal_principal(amount, period, rate, method)
        g, h = cal_expire(amount, period, rate, method)
        result= {"name":nn[i],
                "principal_interest" :a , #원리금균등
                "total_principal_interst": b, #원리금균등
                "principal" : c, #원금균등
                "mean":round(d), #원금균등
                "min":e, #원금균등
                "max":f, #원금균등
                "expire":g, #만기일시
                "total_expire":h #만기일시
                 }
        re.append(result)
    
    json.dumps(re, ensure_ascii=False)
    print(type(re))
    print(re)
    return re

#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from selenium import webdriver
import re
import pymysql
import time
from konlpy.tag import Hannanum #Konlpy안의 여러 형태소 분석기중 가장 noun를 잘 뽑아낸 Hannanum분석기를 사용
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys


#pymysql라이브러리를 활용해 로컬에 구축한 MySQL서버와 연결하는 코드입니다.

db = pymysql.connect(host='127.0.0.1',user='root',password='ehdrlehdrl1996^^',db='mysql')
cursor = db.cursor()
sql = "insert into final_daum(title,content,name,date,click_num) values (%s,%s,%s,%s,%s)"
#MySQL DB에 미리 생성해둔 final_daum라는 테이블에 insert를 하는 sql문 
driver =webdriver.Chrome('C:\young\chromedriver') ## 경로
driver.get('https://search.daum.net/search?w=cafe&DA=CCB&q=%EA%B5%90%EB%B3%B4%20%EB%9D%BC%EC%9D%B4%ED%94%84%ED%94%8C%EB%9E%98%EB%8B%9B&m=board&sort=accuracy&ASearchType=1&lpp=10&rlang=0&req=cafe&spacing=0')
#다음 카페에 '교보라이프플래닛'을 검색한 결과화면을 불러옵니다.
driver.implicitly_wait(2)

html = driver.page_source
soup = BeautifulSoup(html,'html.parser')


#검색결과페이지에서 결과 10개의 title과 link address를 가져오는 함수 'crawler'입니다.

def crawler():

    # 맨앞에 사진이 없는 경우 div가 하나, 있는 경우 div가 두개 이므로 이를 구분해 줘야 합니다.
    link_text = []
    name_data = []


    for count in range(1, 11):
        row_arr = []

        try: #div2 -> 사진이 있음
            # 태그에서 제목과 링크주소 추출
            titlebox = driver.find_element_by_xpath("//*[@id='cafeResultUL']/li[" + str(count) + "]/div[2]/div/div[1]/a")
            print("제목:" + titlebox.text) #제목
            link_text.append(titlebox.get_attribute('href'))  # 링크주소
            print(link_text)
            namebox = driver.find_element_by_xpath("//*[@id='cafeResultUL']/li[" + str(count) + "]/div[2]/div/div[2]/span[1]/a[2]")
            name_data.append(namebox.get_attribute('title'))  # 카페 이름

        except: #div2가 없어 오류가 났을 시 여기로 넘어오게 됩니다.

            try:  # div1 -> 사진이 없음
                titlebox = driver.find_element_by_xpath(
                    "//*[@id='cafeResultUL']/li[" + str(count) + "]/div[1]/div/div[1]/a")
                print("제목:" + titlebox.text) #제목
                row_arr.append(titlebox.text)
                link_text.append(titlebox.get_attribute('href'))  # 링크주소
                row_arr.append(link_text)
                print(link_text)
                namebox = driver.find_element_by_xpath(
                    "//*[@id='cafeResultUL']/li[" + str(count) + "]/div/div/div[2]/span[1]/a[2]")
                name_data.append(namebox.get_attribute('title'))  # 카페 이름


            except:
                print("pass2")
                pass


    #앞 for문에서 저장한 link정보들을 가져와 각 블로그를 열어 'crawling'함수가 포스팅 내용을 확인합니다.        
    for a in range(0, 10):  #한 페이지에 있는 링크 10개 열기
        driver.get(link_text[a])
        driver.implicitly_wait(1)
        crawling(name_data[a])
        driver.implicitly_wait(1)
        driver.back()


#link를 이용해 페이지가 열리면 그 안에서 포스팅 내용을 크롤링하는 crawling함수입니다.

def crawling(name): #포스팅 html안에 카페이름태그가 없어 링크주소를 받아올 때 카페이름도 함께 크롤링해 받아왔습니다. 

    try:

        driver.switch_to.frame('down') #iframe이 변경되는 부분을 적용해주었습니다.

        #포스팅의 제목
        title = driver.find_element_by_xpath("//*[@id='bbsForm']/div[3]/div/span[2]")
        title_data = title.text
        print(title_data)

        #포스팅한 날짜
        date = driver.find_element_by_xpath("//*[@id='bbsForm']/div[4]/span[6]")
        date_data = date.text[:10]
        print(date_data)
        driver.implicitly_wait(2)

        #포스팅의 내용
        body = driver.find_element_by_xpath("// *[ @ id = 'user_contents']")
        driver.implicitly_wait(2)

        #조회수
        clicknum = driver.find_element_by_xpath("//*[@id='bbsForm']/div[4]/span[2]")
        click = clicknum.text[3:]
        print(click)
        driver.implicitly_wait(2)



    except NoSuchElementException:
                print("Nosuch")
                pass

    except UnicodeEncodeError:
                print("uni")
                pass

    #DB에 insert와 commit를 합니다.
    cursor.execute(sql, (title_data, body.text, name, date_data, click))
    db.commit()

crawler()


#검색결과는 한 탭에 10개씩 보여집니다. 이 탭을 넘겨주는 코드. 여기선 range(1,7)라고 설정했으므로 10*7 = 70개의 검색결과를 뽑아옵니다.

for abb in range(1,7) :

    try:

        temp = driver.find_element_by_xpath("// *[ @ id = 'pagingArea'] / span / span[2] / a[" + str(abb) + "]")
        temp.send_keys(Keys.ENTER)
        time.sleep(5)
        crawler()

    except:
        pass


#driver와 로컬 DB서버를 닫아준다.
db.close()
driver.close()
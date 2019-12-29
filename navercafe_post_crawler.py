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
import datetime


#이 코드를 추가 시 크롤링 결과가 하나의 csv파일에 저장되며, 파일명은 자동으로 생성된 날짜와 시간정보를 담도록하였습니다.
#딱 하루치의 크롤링 결과를 뽑아내 저장할 때 사용하는 코드입니다.
#밑의 코드에서 row_arr.append(뽑아낸내용)-> 이 코드가 추가 필요합니다.
'''today = datetime.datetime.today().strftime('bloga_%m%d_%H%M')
f = open('C:/young/' + today +'.csv',"a",newline='',encoding='utf-8')
csv_writer = csv.writer(f)
csv_writer.writerow(['제목','내용']) '''



#pymysql라이브러리를 활용해 로컬에 구축한 MySQL서버와 연결하는 코드입니다.

db = pymysql.connect(host='127.0.0.1',user='root',password='',db='mysql')
cursor = db.cursor()
sql = "insert into final_naver_copy(title,content,name,date,click_num) values (%s,%s,%s,%s,%s)"
#MySQL DB에 미리 생성해둔 final_naver_copy라는 테이블에 insert를 하는 sql문 
driver =webdriver.Chrome('C:\young\chromedriver')
driver2 =webdriver.Chrome('C:\young\chromedriver')
#Web Driver를 두번 사용했습니다. 이유는 밑에서 설명합니다.
driver.get('https://section.cafe.naver.com/cafe-home/search/articles?query=%EA%B5%90%EB%B3%B4%EB%9D%BC%EC%9D%B4%ED%94%84%ED%94%8C%EB%9E%98%EB%8B%9B#%7B%22query%22%3A%22%EA%B5%90%EB%B3%B4%EB%9D%BC%EC%9D%B4%ED%94%84%ED%94%8C%EB%9E%98%EB%8B%9B%22%2C%22page%22%3A1%2C%22sortBy%22%3A0%2C%22period%22%3A%5B%222003.12.01%22%2C%222019.09.18%22%5D%2C%22menuType%22%3A%5B0%5D%2C%22searchBy%22%3A0%2C%22duplicate%22%3Afalse%2C%22includeAll%22%3A%22%22%2C%22exclude%22%3A%22%22%2C%22include%22%3A%22%22%2C%22exact%22%3A%22%22%7D')
#네이버카페에 '교보라이프플래닛'을 검색한 결과화면을 불러옵니다.
driver.implicitly_wait(2)

html = driver.page_source
soup = BeautifulSoup(html,'html.parser')


#검색결과페이지에서 결과 10개의 title과 link address를 가져오는 함수 'crawler'입니다.

def crawler():
    #찾는 태그가 없으면 오류가 발생할 수 있어 그런 오류들을 pass하기위해 try-except문 사용 
    try:
        pn = [] #page number
        link_text = []
        title_text = []

        # 태그에서 제목과 링크주소 추출
        num = 0
        for count in range(1,11):
            atag = driver.find_element_by_xpath("//*[@id='ArticleSearchResultArea']/li[" + str(count) + "]/dl/dt/a")
            print("제목:"+atag.text)
            print(atag.get_attribute('href'))
            title_text.append(atag.text)  # 제목
            link_text.append(atag.get_attribute('href'))  # 링크주소
            b = link_text[num].split('/')
            c = b[4].split('?')
            pn.append(c[0])
            num+=1


        #앞 for문에서 저장한 link정보들을 가져와 각 블로그를 열어 'crawling'함수가 포스팅 내용을 확인합니다.
        #이 (페이지 열기->뒤로가기->열기->뒤로가기->...) 이 과정에서 검색결과 페이지가 새로고침이 되어 중복된 결과가 뽑히는 오류가 있었습니다.
        #그래서 Driver를 2개 사용해 검색결과를 넘기는 창, 링크를 열어 포스팅 내용을 끌어오는 창으로 분리하여 크롤링을 진행하는 방법으로 오류를 수정하였습니다. 
        for a in range(0, 10):  
            print("link[" + str(a) +"]: " + link_text[a])
            driver2.get(link_text[a])
            driver2.implicitly_wait(1)
            crawling(pn[a])
            driver2.implicitly_wait(1)

    except NoSuchElementException:
                print("Nosuch")
                pass

    except UnicodeEncodeError:
                print("uni")
                pass


#link를 이용해 페이지가 열리면 그 안에서 포스팅 내용을 크롤링하는 crawling함수입니다.

def crawling(pn): #xpath에 네이버에서 고유적으로 부여한 포스팅의 숫자(pn)이 있어, 이를 사용하기위해 link를 크롤링할 때 이 pn을 별도 리스트에 저장해 함께 넘겨줍니다.
    
    try:
        hannanum = Hannanum()
        pos_arr = []
    
        #포스팅의 제목
        name = driver2.find_element_by_xpath('/html/body/h1')
        name_data = name.text
        print(name_data)
        driver.implicitly_wait(2)

        driver2.switch_to.frame('cafe_main') #iframe이 변경되는 부분을 적용해주었습니다.

        #포스팅이 된 카페의 이름
        title = driver2.find_element_by_xpath('//*[@id="post_'+pn+'"]/div/div[1]/div[1]/table/tbody/tr/td[1]/span')
        title_data = title.text
        driver2.implicitly_wait(2)
        #row_arr.append(title_data)

        #포스팅의 내용
        body = driver2.find_element_by_xpath('//*[@id="tbody"]')
        body_data = no_space(body.text) #줄바꿈을 없애줍니다.
        driver2.implicitly_wait(2)

        #포스팅한 날짜
        date = driver2.find_element_by_xpath('//*[@id="post_'+pn+'"]/div/div[1]/div[2]/table/tbody/tr/td[2]')
        date_data = date.text[:10]
        print(date_data)
        driver2.implicitly_wait(2)

        #조회수
        click_num = driver2.find_element_by_xpath('//*[@id="cmtMenu"]/div[1]/table/tbody/tr/td[5]/span[2]')
        click = click_num.text.replace(',','')
        #row_arr.append(body_data)

        print("title"+title_data)
        print("body" + body_data)
        time.sleep(2)

        #내용분석에 도움이 되지않는 각종 문장부호들을 제거합니다.
        con = cleanText(body_data)
        val_list = hannanum.pos(con)
        time.sleep(3)

        #DB에 insert와 commit를 합니다.
        cursor.execute(sql,(title_data,body_data,name_data,date_data,click))
        db.commit()

    except NoSuchElementException:
                print("Nosuch")
                pass

    except UnicodeEncodeError:
                print("uni")
                pass


#공백제거
def no_space(text) :
    text1 = re.sub('&nbsp; | &nbsp;| \n|\t|\r|\\n','',text)
    text2 = re.sub('\n\n','',text1)

    return text2


#문장부호 제거
def cleanText(readData):
    text = re.sub('[-=+,#/\?:^$.’@*☆\"★♡♥※☆※~&%ㆍ!』\\‘”“|\(\)\n\<\>`\'…》]', ' ', readData)
    text1 = re.sub('\n\n', ' ', text)

    return text1


#검색 기간을 설정하도록 해주는 코드. %s를 사용해 사용자가 직접 입력하게 할 수도 있습니다.

a = driver.find_element_by_xpath("//*[@id='option_period_form']/fieldset/div/div[1]/div[2]/a/img")
a.click()
driver.implicitly_wait(2)
elem = driver.find_element_by_xpath("//*[@id='date_from']")
elem.clear()
elem.send_keys("2019.11.01")
elem = driver.find_element_by_xpath("//*[@id='date_to']")
elem.clear()
elem.send_keys("2019.12.16")
driver.find_element_by_xpath('//*[@id="option_period_direct"]/div[2]/input').click()


#검색결과는 한 탭에 10개씩 보여집니다. 이 탭을 넘겨주는 코드. 여기선 range(1,11)라고 설정했으므로 10*10 = 100개의 검색결과를 뽑아옵니다.

for abb in range(1,11) :

        temp = driver.find_element_by_xpath("//*[@id='content_srch']/div[3]/div[2]/button[" + str(abb) + "]")
        temp.send_keys(Keys.ENTER)
        time.sleep(5)
        crawler()

#driver와 로컬 DB서버를 닫아준다.
driver.close()
db.close()

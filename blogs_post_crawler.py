from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import time
import pymysql
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import datetime

'''today = datetime.datetime.today().strftime('blog_post_%m%d_%H%M')
z = open('C:/young/' + today + '.csv', "a", newline='',encoding='utf8')
csv_writer = csv.writer(z, delimiter=';')
csv_writer.writerow(['제목', '회사', '글내용'])  # col 제목 설정'''

db = pymysql.connect(host='127.0.0.1', user='root', passwd='ehdrlehdrl1996^^', db='mysql')
cursor = db.cursor()
sql = "insert into blog_post(title,content) values (%s,%s)"

driver =webdriver.Chrome('C:\young\chromedriver') ## 경로
driver.get('https://search.daum.net/search?w=blog&nil_search=btn&DA=STC&enc=utf8&q=%EA%B5%90%EB%B3%B4%20%EB%9D%BC%EC%9D%B4%ED%94%84%ED%94%8C%EB%9E%98%EB%8B%9B')
driver.implicitly_wait(2)

html = driver.page_source
soup = BeautifulSoup(html,'html.parser')


def crawler():
            # 태그에서 제목과 내용, 카페명 추출
            # 맨앞에 사진이 없는 경우 div가 하나, 있는 경우 div가 두개 이므로 이를 구분해 줘야 함
            link_text = []
            t = ''

            try:

                for count in range(1, 11):#div두개 -> 사진 있는 경우

                    titlebox = driver.find_element_by_xpath("/html/body/article/article/div/article/div/div[4]/div/div[3]/ul/li[" + str(count) + "]/div[2]/div/div[1]/a")
                    print(titlebox.text)
                    print(titlebox.get_attribute('href'))
                    link_text.append(titlebox.get_attribute('href'))


            except:

                   try : #div한개, 사진 없음
                            titlebox = driver.find_element_by_xpath("/html/body/article/article/div/article/div/div[4]/div/div[3]/ul/li[" + str(count) + "]/div/div/div[1]/a")
                            print(titlebox.text)
                            print(titlebox.get_attribute('href'))
                            link_text.append(titlebox.get_attribute('href'))
                            driver.implicitly_wait(2)


                   except NoSuchElementException:
                       print("Nosuch")
                       pass


                   except UnicodeEncodeError:
                       print("uni")
                       pass


            for a in range(0, 10):  ##한 페이지에 있는 링크 10개 열기
                print("link[" + str(a) + "]: " + link_text[a])
                driver.implicitly_wait(1)
                driver.get(link_text[a])
                crawling(link_text[a])
                driver.implicitly_wait(1)
                driver.back()


def crawling(lt):

       body_str = "s"

       if 'tistory' in lt:

                    print("tistory")
                    c = driver.find_elements_by_xpath('//*[@id="jb-page"]/div[4]/div/div[2]/div[1]/div[1]/article/div[1]/div/p')
                    // *[ @ id = "mArticle"] / div[3] / div / p[1]
                    driver.implicitly_wait(2)
                    for n in c :
                        print(n.text)
                        body_str += n.text

                    #csv_writer.writerow(ra)


       elif 'brunch' in lt:
                    print("brunch")
                    c = driver.find_elements_by_xpath('/html/body/div[3]/div[1]/div[2]/div[1]/p')
                    driver.implicitly_wait(2)
                    for n in c:
                        print(n.text)
                        body_str += n.text

                    #csv_writer.writerow(ra)


       elif 'naver' in lt:
                    print("naver")
                    c = soup.select('td > div > div > div > div > div > div > div > p > span')
                    driver.implicitly_wait(2)
                    for n in c:
                        print(n.text)
                        body_str += n.text

                    #csv_writer.writerow(ra)

       elif 'daum' in lt:
                    print("daum")
                    b = lt.split('/')
                    pn = b[2]
                    driver.implicitly_wait(2)
                    driver.switch_to.frame('BlogMain')
                    driver.implicitly_wait(2)
                    driver.switch_to.frame('if_b_' + pn)
                    driver.implicitly_wait(2)
                    html1 = driver.page_source
                    soup1 = BeautifulSoup(html1, 'html.parser')
                    c = soup1.select("#contentDiv > p")
                    for n in c:
                        print(n.text)
                        body_str += n.text

                    #csv_writer.writerow(ra)

       time.sleep(2)
       cursor.execute(sql,('a',body_str))





crawler()


for abb in range(2,4) :

        try:

            temp = driver.find_element_by_xpath("// *[ @ id = 'pagingArea'] / span / span[2] / a[" + str(abb) + "]")
            temp.send_keys(Keys.ENTER)
            time.sleep(5)
            crawler()

        except:
            print("pass4")
            pass



driver.close()
db.commit()
db.close()
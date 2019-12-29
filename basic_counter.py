#-*- coding: utf-8 -*-

import time
import pymysql
import csv
from collections import Counter

#csv파일에 저장
f = open("C:/young/word_daum.csv","a",newline='')
csv_writer = csv.writer(f,delimiter=';')
csv_writer.writerow(['word','number']) 


#pymysql라이브러리를 활용해 로컬에 구축한 MySQL서버와 연결하는 코드입니다.

db = pymysql.connect(host='127.0.0.1',user='root',password='ehdrlehdrl1996^^',db='mysql')
cursor = db.cursor()
sql = "select daum from noun"
#MySQL DB에 저장된 noun테이블에서 daum이라는 column의 데이터를 가져오라는 sql문
cursor.execute(sql)
result = cursor.fetchone()
time.sleep(2)

split_arr = result[0].split(' ')

# 불용어 처리하기
result2 = []
stop_words = ['제목', '오히려', '이상', '달리', '노', '린', '다나', '결코', '더욱', '음', '바로', '역시', '마치', '정도', '로서', "여기", '날', '누군가',
              '동안', '이자', '왜', '계속', '속', '안', '누구', '다른', '알', '등', '이', '수', '무엇', '더', '또', '것', '세', '살', '때', '누',
              '과', '그', '위해', '곳', '은', '는', '가', '을', '를', '중', '의', '간', '전', '후', '로', '못', '또한', '뒤', '다시', '대해',
              '듯', '데', '통해', '위', '대한', '때문', '가지', '두', '온', '채', '점', '번']
stop_words2 = ['니', '오가와', '이토', '조금', '라면', '보기', '본문', '정말', '얼마나', '그대로', '아주', '부작', '비아', '아두', '이번', '한편', '비롯',
               '만큼', '진짜', '그냥']
stop_words += one_dic.dic
stop_words += stop_words2
for w in split_arr:
   if w not in stop_words:
      result2.append(w)

time.sleep(3)

#가장 많이 등장하는 noun 100개 뽑아오기
count = Counter(result2).most_common(100)

for word in count:
   row_arr = []

   str_word = str(word)
   #list로 쭉 저장된 count결과를 스트링으로 바꾼 후 
   num = str_word.find(',') 
   # , 로 구분된 단어들을 쪼개서 별도 list에 저장
   word = str_word[2:num-1]
   print(word)
   row_arr.append(word)

   number = str_word[num+1:len(str_word)-1]
   number1 = number.strip()

   print(number1)

   row_arr.append(number1)

   csv_writer.writerow(row_arr)

   time.sleep(2)


db.close()
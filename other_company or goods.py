import time
import pymysql
import csv


f = open("C:/young/company.csv","a",newline='')
csv_writer = csv.writer(f,delimiter=';')
csv_writer.writerow(['company','num']) 
row_arr = []


#pymysql라이브러리를 활용해 로컬에 구축한 MySQL서버와 연결하는 코드입니다.

db = pymysql.connect(host='127.0.0.1',user='root',password='ehdrlehdrl1996^^',db='mysql')
cursor = db.cursor()
sql = "select content from daum_cafe_post1"
#daum_cafe_post1테이블에서 포스팅내용을 저장한 content column을 불러옵니다.
cursor.execute(sql)
result = cursor.fetchall()
time.sleep(2)

sql1 = "select content from naver_cafe_post"
#naver_cafe_post테이블에서 포스팅내용을 저장한 content column을 불러옵니다.
cursor.execute(sql1)
result1 = cursor.fetchall()
time.sleep(2)


company_array = ['삼성','신한','한화','농협','미래에셋','동양','흥국','메트라이프','메리츠']
#경쟁사 이름을 리스트에 저장해둡니다.
num_array = [0,0,0,0,0,0,0,0,0]
#경쟁사가 언급될 때마다 카운팅되어 value가 증가합니다.


#상품명 언급빈도 측정시에는 이와같이 array들을 변경합니다.
goods_array = ['정기보험','종신보험','연금보험','연금저축','어린이보험','암보험','교통상해보험','상해보험','저축보험','입원비보험','수술비보험','펫사랑','미세먼지질병','3대','연금전환']
num_array = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


#daum
for a in result:
    a_str = ''.join(a)
    print(a_str)
    num = 0
    for b in company_array:
        print('b: '+b)
        if b in a_str:
            num_array[num]+=1
            print('ok')
        #문자열 a안에 경쟁사이름 b가 있으면 num_array[해당 경쟁사 인덱스]+=1 합니다. 
        num+=1


#naver
for c in result1:
    c_str = ''.join(c)
    print(c_str)
    num = 0
    for d in company_array:
        print('d: '+d)
        if d in c_str:
            num_array[num]+=1
            print('ok')
        #문자열 c안에 경쟁사이름 d가 있으면 num_array[해당 경쟁사 인덱스]+=1 합니다. 
        num+=1

print(num_array)


#csv파일에 쓰기
for i in range(len(company_array)) :
    row_arr.append(company_array[i])
    row_arr.append(num_array[i])
    csv_writer.writerow(row_arr)
    row_arr.clear()

f.close()
db.close()
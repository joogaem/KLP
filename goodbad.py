import pandas as pd
import pymysql
import time

word_dic = {}


def polarity_to_dic() : #긍정 부정 값을 딕셔너리로 표현
    df = pd.read_csv('polarity.csv')
    split_df = df[['ngram','max.value']]

    num = 0
    for val in split_df['max.value'] :
        if 'POS' in val :
            word_p = split_df.loc[num][0]
            word_dic[word_p]=1

        elif 'NEG' in val :
            word_n = split_df.loc[num][0]
            word_dic[word_n]=-1

        num+=1


#pymysql라이브러리를 활용해 로컬에 구축한 MySQL서버와 연결하는 코드입니다.
#이후 dataframe에 데이터 저장
db = pymysql.connect(host='127.0.0.1',user='root',password='',db='mysql')
cursor = db.cursor()
sql = "select title, clicknum, content, pos from daum_cafe_post3"
cursor.execute(sql)
result = cursor.fetchall()
time.sleep(2)

sql1 = "select title, click_num, content, pos from naver_cafe_post1"
cursor.execute(sql1)
result1 = cursor.fetchall()
time.sleep(2)

data_dic = pd.DataFrame({'title':[],'clicknum':[], 'content':[], 'pos':[]})

for arr in result :
    a = pd.Series(arr,index = ['title','clicknum','content', 'pos'])
    data_dic = data_dic.append(a,ignore_index=True)

for arr in result1 :
    b = pd.Series(arr,index = ['title','clicknum','content','pos'])
    data_dic = data_dic.append(b,ignore_index=True)

time.sleep(3)


polarity_to_dic()
time.sleep(5)


#data와 형태소 비교하여 polarity score를 측정합니다.
score_arr = []
for p in data_dic['pos'] :
    score = 0
    p_arr = p.split(';')
    for pa in p_arr:
        for key,value in word_dic.items():
            if pa in key:
                score += value
    score_arr.append(score)
    time.sleep(3)

data_dic["score"] = score_arr
data_dic2 = data_dic.drop('pos',axis=1)
print(data_dic2)
data_dic2.to_csv('C:/young/goodbad.csv',sep=';',index=False, header=True)


db.close()

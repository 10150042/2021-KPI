#-*-coding:utf-8-*-             # 한글표현을 위해 utf-8 인코딩 명시
from bs4 import BeautifulSoup   # 파이썬 웹 파싱 라이브러리 중 하나인 bs4(beautifulsoup 4)에서 BeautifulSoup 임포트
import requests                 # 웹 request를 위해 requests 모듈 임포트
import sqlite3                  # DB사용을 위한 sqlite3 모듈 임포트

def ahnlab_parsing():
    url = 'https://asec.ahnlab.com/ko/'                     # 안랩ASEC url
    response = requests.get(url)                            # 안랩ASEC로 request를 보낸 후 결과값을 response 변수에 저장
    soup = BeautifulSoup(response.content, 'html.parser')   # BeautifulSoup 함수를 사용하여 파싱 결과값을 soup 변수에 저장
    context = soup.find_all(class_='posttitle')             # 기사 내 특정부분을 파싱하기 위해 전체 class 태그 내 값이 'posttitle' 인 태그 전체를 context 배열에 저장
    
    for i in range(5):
        link = context[i].a.attrs['href']                                           # 추출한 값 내부에 하이퍼링크 url 값을 추출
        title = context[i].text                                                     # 기사 제목 추출
        title = title.replace("\n", "").replace("				","")# 기사 제목 마지막에 존재하는 공백 제거
        title = title.replace("\"", "")                                             # 제목 내 '"'은 공백으로 치환
        title = title.replace("\'", "")                                             # 제목 내 "'"은 공백으로 치환
        info = ((link, title))                                                      # url, 제목을 묶어 info 변수에 저장
        conn = sqlite3.connect('C:\\파싱\\db\\ahnlab.db', isolation_level=None)     # 특정 경로에 위치한 db파일을 연결
        c = conn.cursor()                                                           # 커서 위치조정
        c.execute("SELECT link FROM data WHERE link=(?)",(link,))                   # db내 해당 url이 존재하는지 질의
        db_data = c.fetchone()                                                      # 조회한 결과값 반환
        
        if db_data is None: # 결과값이 없을 시
            c.execute("INSERT INTO data VALUES(?,?)", info)                                       # db에 해당 info(url, 제목)를 추가
            headers = {'Content-type': 'application/json; charset=utf-8'}                         # Slack에 업로드를 위해 html header 값 수정
            data = "{'text':" + "'" + "`안랩ASEC`" +" "+ title + '\n' + link + '\n' + "'}"        # Slack에 업로드 되어질 내용 수정
            response = requests.post('webhook url', headers=headers, data=data.encode('utf-8'))   # Slack webhook 을 통해 웹 파싱된 내용 업로드

            

#-*-coding:utf-8-*-
from bs4 import BeautifulSoup
import requests
import sqlite3

def ahnlab_parsing():
    url = 'https://asec.ahnlab.com/ko/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    context = soup.find_all(class_='posttitle')
    
    for i in range(5):
        link = context[i].a.attrs['href']
        title = context[i].text
        title = title.replace("\n", "").replace("				","")
        title = title.replace("\"", "")
        title = title.replace("\'", "")
        info = ((link, title))
        conn = sqlite3.connect('C:\\파싱\\db\\ahnlab.db', isolation_level=None)
        c = conn.cursor()
        c.execute("SELECT link FROM data WHERE link=(?)",(link,))
        db_data = c.fetchone()
        
        if db_data is None:
            c.execute("INSERT INTO data VALUES(?,?)", info)
            headers = {'Content-type': 'application/json; charset=utf-8'}
            data = "{'text':" + "'" + "`안랩ASEC`" +" "+ title + '\n' + link + '\n' + "'}"
            response = requests.post('webhook url', headers=headers, data=data.encode('utf-8'))

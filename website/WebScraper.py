from flask import redirect , url_for
from bs4 import BeautifulSoup
from . import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine


def get_Thess_Guide_events():

    from .models import Event,Date
    import requests
    
    try:
        db.session.query(Event).delete()
        db.session.query(Date).delete()
        db.session.commit()
    except:
        db.session.rollback()


    #get page source html code
    htmlsourceCode = getThessalonikiGuideSourceCode()
    
    soup = BeautifulSoup(htmlsourceCode, 'html.parser')

    #find links per event 
    a_tags= soup.find_all('div' ,{'class': 'event-content'})
    
    urls = list()
    for a in a_tags:
        urls.append(a.find('a')['href'])

    #get source code per url
    
    id = 0 
    count = 0
    for url in urls:
        id = id + 1
        
        page_soup = BeautifulSoup(requests.get(url).text , 'html.parser')

        #get all event attributes (name, image, description, location, date)
        #name
        name = page_soup.find('h1',{'class':"title-single text-bg-25 text-sm-23"})
        name = name.text

        #image
        div = page_soup.find('div' , {'class':'jo-bottom-15'})
        img = div.find('img').attrs['src']
        
        #description
        description = page_soup.find('div' , {'class': 'entry-content'})
        description = description.find('p').text

        #location 

        location = page_soup.find('div',{'class': 'jo-one-line'})
        location = location.text

        #putting Events into database
        ev = Event.query.filter_by(link= url).first()
        if not ev:
            new_Event = Event(id=id, link = url, name = name , image = img ,description = description ,location = location)
            try:
                db.session.add(new_Event)
            except:
                db.session.rollback()
                print("Raised Exeption 1!!")
                raise
            else:
                db.session.commit()

        div_date=page_soup.find_all('div' , {'class' : 'jo-btn jo-btn-5 text-bg-13 jcol-row'})
        for div in div_date:
            count = count +1
            d=div.find('div', {'class': 'jo-weight-600'}).text
            t=div.find('div', {'class': 'jo-gray'}).text
            
            exist = Date.query.filter_by(date_id= count).first()
            if not exist:
                
                new_Date = Date(date_id=count ,day=d, time=t ,event_id  = id )
                try:
                    db.session.add(new_Date)
                except:
                    db.session.rollback()
                    print("Raised Exeption 2!!")
                    raise
    db.session.commit()
    print("----------------------------------DATA SCRAPTED-----------------------------------------")

#get html source code of thessalonikiguide.gr/events/theatro/ 
#Curl source code
def getThessalonikiGuideSourceCode():
    import requests

    headers = {
        'authority': 'stats.g.doubleclick.net',
        'accept': '*/*',
        'accept-language': 'el-GR,el;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'cookie': 'DSID=AOKRq4o3QmX-NWYmiVxdiYA7HguWYohn1GhdDfgSS7t_zdNKxCz6PLy8HWW9ookTksFGwsEwA-l_uH6QaHi84O_edWu25TdzG7Ie-CFbIERzqxwQVpmYS_5Lb6FNAhR6fQxlk4f4rp1I_4AxA8lDjpDnByX2ZJUiDbeJlNVH-P301H8Awck_3BY-3egz9C2PQtGgNKcdjqO9XdV0pw0ASAFUeVtvRxxC_Hs_ZLgxgr6MS81tBnwzXW8ONnVeK1X16VyfIikyZFlDKTJalYX34cvWeUxcW4E7cPCz2GTEEx7wShTzwL8q62g',
        'dnt': '1',
        'if-modified-since': 'Tue, 27 Sep 2022 22:01:05 GMT',
        'referer': 'https://www.thessalonikiguide.gr/',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'DNT': '1',
        'Referer': 'https://www.thessalonikiguide.gr/',
        'Origin': 'https://www.thessalonikiguide.gr',
        'if-none-match': '"1399 / 315 of 1000 / last-modified: 1669118838"',
        'x-client-data': 'CI22yQEIprbJAQjEtskBCKmdygEIlKHLAQjF4cwBCPvqzAEIpPvMAQio/MwB',
        'content-length': '0',
        'content-type': 'text/plain',
        'origin': 'https://www.thessalonikiguide.gr',
        'If-None-Match': '"/A2srSIFXYMh66Dz2oo2xoMQ2Ko="',
        'If-Modified-Since': 'Fri, 18 Nov 2022 10:26:20 GMT',
    }

    response = requests.get('https://www.thessalonikiguide.gr/events/theatro/', headers=headers)

    return response.text

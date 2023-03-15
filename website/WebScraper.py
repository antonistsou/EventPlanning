from flask import redirect , url_for
from bs4 import BeautifulSoup
from . import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from string import digits
from datetime import datetime

def get_Thess_Guide_events():

    from .models import Event,Date
    import requests
    
    # get exact date 

    currentDate =datetime.today().strftime("%d/%m/%Y")
    
    currentDate = datetime.strptime(currentDate,"%d/%m/%Y")
    year = datetime.now().year
   
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
    a_tags= soup.find_all('div' ,{'class': 'col-12 col-sm-auto col-md-auto'})
    
    urls = list()
    p=0
    for a in a_tags:
        p+=1
        urls.append(a.find('a')['href'])

    #get source code per url
    
    id = 0 
    count = 0
    for url in urls:
        id = id + 1
        
        page_soup = BeautifulSoup(requests.get(url).text , 'html.parser')

        #get all event attributes (name, image, description, location, date)
        #name
        name = page_soup.find('h1',{'class':"fw-800 ithDF-f text-25 lh-120"})
        name = name.text

        #image
        div = page_soup.find('div' , {'class':'col-12 col-md-7'})
        img = div.find('img').attrs['src']
        
        #description
        description = page_soup.find('div' , {'class': 'entry-content'})
        description = description.find('p').text

        #event info
        info = page_soup.find('div' , {'class' : 'mb-20'})
        info = info.find('p').text

        #location 

        location1 = page_soup.find('div' , {'class': 'text-14 fw-600'})
        location2 = page_soup.find('div' , {'class': 'text-13 mb-15'})
        location  = location1.text + ' ,' + location2.text

        #putting Events into database
        ev = Event.query.filter_by(link= url).first()
        if not ev:
            new_Event = Event(link = url, name = name , image = img ,description = description , info= info,location = location)
            try:
                db.session.add(new_Event)
            except:
                db.session.rollback()
                print("Raised Exeption 1!!")
                raise
            else:
                db.session.commit()

        #Event Dates
        div_date=page_soup.find_all('div' , {'class' : 'col-4 col-sm-4 col-md-2 p-3'})
                                                    
        for div in div_date:
            count = count +1
            d=div.find('div', {'class': 'fw-600'}).text
            t=div.find('div', {'class': 'jo-gray'}).text
            
            remove_digits = str.maketrans('', '', digits)
            d1 =d.replace('/','')
            dayname= d1.translate(remove_digits)

            import re

            pattern=r'[ΔεΤρΤεΠεΠαΣαΚυ ]'
            
            exactdate = re.sub(pattern,'',d)

            exactdate +='/'+str(year)
        
            exactdate = datetime.strptime(exactdate,"%d/%m/%Y")

            delta  = exactdate - currentDate
            if delta.days> 0 and delta.days < 250:
                exist = Date.query.filter_by(date_id= count).first()
                if not exist:
                    new_Date = Date(dayname=dayname,day=exactdate, time=t ,event_id  = id )
                    
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
        'authority': 'www.thessalonikiguide.gr',
        'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'accept-language': 'el-GR,el;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'cookie': '_ga=GA1.2.1046530880.1678364695; euconsent-v2=CPoW08APoW08AAKAuAELC6CsAP_AAH_AAAyIJSNd_H__bW9r-f5_aft0eY1P9_r77uQzDhfNk-4F3L_W_LwX52E7NF36tq4KmR4ku1LBIUNlHNHUDVmwaokVryHsak2cpTNKJ6BEkHMZO2dYGF5vmxtj-QKY5v5_d3bx2D-t_9v-39z3z81Xn3d5_-_02PCdU5_9Dfn9fR_b89KP9_78v4v8_9_rk3_e__3_79_7_H9-QSjAJMNW4gC7MscGbQMIoEQIwrCQigUAEFAMLRAQAODgp2VgE-sIkACAUARgRAhwBRgQCAAASAJCIAJAiwQAAAiAQAAgAQCIQAMDAILACwEAgABANAxRCgAECQAyICIpTAgKgSCAlsqEEoLpDTCAKssAKARGwUACIJARWAAICwcAwRICViwQJMQbRACMAKAUSoVqKT00BAAA.YAAAAAAAAAAA; addtl_consent=1~39.4.3.9.6.9.13.6.4.15.9.5.2.11.1.7.1.3.2.10.3.5.4.21.4.6.9.7.10.2.9.2.18.7.20.5.20.6.5.1.4.11.29.4.14.4.5.3.10.6.2.9.6.6.9.4.4.29.4.5.3.1.6.2.2.17.1.17.10.9.1.8.6.2.8.3.4.146.8.42.15.1.14.3.1.18.25.3.7.25.5.18.9.7.41.2.4.18.21.3.4.2.7.6.5.2.14.18.7.3.2.2.8.20.8.8.6.3.10.4.20.2.13.4.6.4.11.1.3.22.16.2.6.8.2.4.11.6.5.33.11.8.1.10.28.12.1.3.21.2.7.6.1.9.30.17.4.9.15.8.7.3.6.6.7.2.4.1.7.12.13.22.13.2.12.2.10.1.4.15.2.4.9.4.5.4.7.13.5.15.4.13.4.14.10.15.2.5.6.2.2.1.2.14.7.4.8.2.9.10.18.12.13.2.18.1.1.3.1.1.9.25.4.1.19.8.4.5.3.5.4.8.4.2.2.2.14.2.13.4.2.6.9.6.3.2.2.3.5.2.3.6.10.11.6.3.16.3.11.3.1.2.3.9.19.11.15.3.10.7.6.4.3.4.6.3.3.3.3.1.1.1.6.11.3.1.1.11.6.1.10.5.2.6.3.2.2.4.3.2.2.7.15.7.14.1.3.3.4.5.4.3.2.2.5.4.1.1.2.9.1.6.9.1.5.2.1.7.10.11.1.3.1.1.2.1.3.2.6.1.12.5.3.1.3.1.1.2.2.7.7.1.4.1.2.6.1.2.1.1.3.1.1.4.1.1.2.1.8.1.7.4.3.2.1.3.5.3.9.6.1.15.10.28.1.2.2.12.3.4.1.6.3.4.7.1.3.1.1.3.1.5.3.1.3.4.1.1.4.2.1.2.1.2.2.2.4.2.1.2.2.2.4.1.1.1.2.2.1.1.1.1.2.1.1.1.2.2.1.1.2.1.2.1.7.1.2.1.1.1.2.1.1.1.1.2.1.1.3.2.1.1.8.1.1.6.2.1.6.2.3.2.1.1.1.2.2.3.1.1.4.1.1.2.2.1.1.4.3.1.2.2.1.2.1.2.3.1.1.2.4.1.1.1.5.1.3.6.3.1.5.2.3.4.1.2.3.1.4.2.1.2.2.2.1.1.1.1.1.1.11.1.3.1.1.2.2.5.2.3.3.5.1.1.1.4.2.1.1.2.5.1.9.4.1.1.3.1.7.1.4.5.1.7.2.1.1.1.2.1.1.1.4.2.1.12.1.1.3.1.2.2.3.1.2.1.1.1.2.1.1.2.1.1.1.1.2.4.1.5.1.2.4.3.8.2.2.9.7.2.2.1.2.1.4.6.1.1.6.1.1.2.6.3.1.2.201.300.100; __qca=P0-1966784026-1678364695131; __cf_bm=NTrySKzlzw0ubMnmpPwFDHrE_xYo_3ybDZ.zuSPZXJM-1678705458-0-Aas+I7rsrywdcDmcUjM6oJMyJfbKW4/J8sCvJMVInHm+l8ZyZ//KmsfqYTBPgvIp1bL6CJYyFqWyYI5TuZhRRts=; _gid=GA1.2.1540316050.1678705463',
        'dnt': '1',
        'if-modified-since': 'Mon, 13 Mar 2023 07:58:55 GMT',
        'referer': 'https://www.thessalonikiguide.gr/events/theatro/',
        'sec-ch-ua': '^\\^Chromium^\\^;v=^\\^110^\\^, ^\\^Not',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '^\\^Windows^\\^',
        'sec-fetch-dest': 'image',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Referer': 'https://www.thessalonikiguide.gr/',
        'DNT': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Origin': 'https://www.thessalonikiguide.gr',
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'Accept-Language': 'el-GR,el;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'image',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site',
        'If-None-Match': '^\\^kQIB0mzxcKM3Mm7qOVo7+dvSugs=^\\^',
        'If-Modified-Since': 'Thu, 09 Feb 2023 11:26:58 GMT',
    }



    response = requests.get('https://www.thessalonikiguide.gr/events/theatro/', headers=headers)

    return response.text

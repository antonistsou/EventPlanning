from flask import Blueprint , render_template ,request , flash ,redirect, url_for
from flask_login import  login_required , current_user
from bs4 import BeautifulSoup

views = Blueprint('views' , __name__)

#home screen 
@views.route('/' , methods = ['GET'])
@login_required
def home():
    from .models import Event 

    #get page source html code
    htmlsourceCode = getThessalonikiGuideSourceCode()
    
    soup = BeautifulSoup(htmlsourceCode, 'html.parser')

    #find links per event 
    a_tags= soup.find_all('div' ,{'class': 'event-content'})
    
    urls = list()
    for a in a_tags:
        urls.append(a.find('a')['href'])

    #get source code per url
    counter = 0 
    eventsList = list()

    import requests

    for url in urls:
        counter = counter + 1
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

        #dates
        dates =list()
        
        days = list()
        times = list()

        day = page_soup.find_all('div',{'class': 'jo-weight-600'})
        for d in day:
            days.append(d.text)
        
        time = page_soup.find_all('div',{'class': 'jo-gray'})
        for t in time:
            times.append(t.text)
        
        dates = days + times

        eventsList.append(Event(counter, name,img,description,location ,days ,times))  

    for i in eventsList:
        print(i.name + " " +i.image + " "+i.description + " "+i.location + " ",i.day ,i.time)
 
    return render_template("home.html" , user = current_user ,eventsList = eventsList)


@views.route('/result' , methods = ['GET' , 'POST'])
def result():
    return  render_template("result.html" , user = current_user)
    
#space addition to the date cause it didnt had
def dateStringFormation(s):
    s = s[:8] + ' ' + s[8:]
    return s


#get html source code of thessalonikiguide.gr/events/theatro/ 
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


# def codetry():
#     htmlsourceCode = getThessalonikiGuideSourceCode()
    
#     soup = BeautifulSoup(htmlsourceCode, 'html.parser')

#     from .models import Event 

#     count=0
    
#     events = list()
#     namess = list()
#     imagess = list()
#     descss = list()
#     locationss = list()
#     datess = list()

#     names = soup.find_all('h3' , {'class':'entry-title event-title'})
#     for name in names:
#         count+=1
#         namess.append((name.find('a').text))
    
#     images = soup.find_all('img' , {'class':'alignleft wp-post-image'})
#     for image in images:
#             imagess.append(image['src'])
  
#     descripitons = soup.find_all('div' , {'class':'jo-desc'})
#     for desc in descripitons:
#             descss.append(desc.text)

#     locations = soup.find_all('span' , {'itemprop':'streetAddress'})
#     for loc in locations:
#             locationss.append(loc.text)
    
#     dates = soup.find_all('div' , {'class':'event-dates'})
#     for date in dates:
#         if date.text!=" . . . ":
#             time = date.text
#             time = dateStringFormation(time)
#             datess.append(time)

#     for i in range(count):
#         events.append(Event(i,namess[i],imagess[i],descss[i],locationss[i],datess[i]))
    
#     for i in range(count):
#         print(events[1].location )

#     return datess
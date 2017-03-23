# -*- coding: utf-8 -*-

import requests
import re
from time import sleep

headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
'Cookie':'showNav=#nav-tab|0|0; navCtgScroll=0; navCtgScroll=0; showNav=#nav-tab|0|0; _hc.v="\"28c48835-807a-422e-ba61-ad744498f777.1450593856\""; __utma=1.196682546.1450594182.1450594182.1452605452.2; __utmz=1.1452605452.2.2.utmcsr=gufensoso.com|utmccn=(referral)|utmcmd=referral|utmcct=/search/; PHOENIX_ID=0a018986-152531ce5a3-13cb4e7; s_ViewType=10; JSESSIONID=2253E3DD5E72430473A45342361F6501; aburl=1; cy=1; cye=hongkong'}

def GetOpenRiceRestaurantsNames(html_file):
    restaurants_names = []
    pieces_with_restaurants_names = re.findall('<h2 class="title-name">(.*?)</h2>',
                                               html_file, re.S)

    for i in range(len(pieces_with_restaurants_names) - 2):
        restaurants_names.append(re.search('<a href=(.*?)>(.*?)</a>',
                                           pieces_with_restaurants_names[i],
                                           re.S).group(2).strip())
    
    return restaurants_names

def GetOpenRiceRestaurantsAddresses(html_file):
    restaurants_addresses = []
    pieces_with_restaurants_addresses = re.findall('<div class="or-sprite-inline-block condition_location_40x40_desktop"></div>(.*?)</div>',
                                                   html_file, re.S)
    
    for i in range(len(pieces_with_restaurants_addresses)-2):
        restaurants_addresses.append(re.search('<span>(.*?)<a href="(.*?)">(.*?)</a>',
                                     pieces_with_restaurants_addresses[i],
                                     re.S).group(1)
                                     + re.search('<span>(.*?)<a href="(.*?)">(.*?)</a>',
                                     pieces_with_restaurants_addresses[i],
                                     re.S).group(3))

    return restaurants_addresses

def GetOpenRicePageContents(food, page):
    url = 'https://www.openrice.com/en/hongkong/restaurants?what='

    if page != 1:
        url = url + food + '&page=' + '%i' % page
    else:
        url = url + food
    
    html = requests.get(url, headers=headers)
    return html.text

def GetYelpRestaurantsNames(html_file):
    restaurants_names = []
    pieces_with_restaurants_names = re.findall('<span class="indexed-biz-name">(.*?)</a>',
                                               html_file, re.S)

    for i in range(len(pieces_with_restaurants_names)):
        restaurants_names.append(re.search('<span >(.*?)</span>',
                                           pieces_with_restaurants_names[i],
                                           re.S).group(1))
    
    return restaurants_names

def GetYelpRestaurantsAddresses(html_file):
    restaurants_addresses = []
    pieces_with_restaurants_addresses = re.findall('<address>(.*?)<br>',
                                                   html_file, re.S)
    
    for i in range(len(pieces_with_restaurants_addresses)):
        restaurants_addresses.append(pieces_with_restaurants_addresses[i].strip())

    return restaurants_addresses

def GetYelpPageContents(food, page):
    url = 'https://www.yelp.com/search?find_desc='

    if page != 1:
        url = url + food + '&start=%i' % (page - 1) * 10
    else:
        url = url + food

    html = requests.get(url, headers=headers)
    return html.text

def GetGoogleMapCoordinate(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'sensor': 'false', 'address': address}
    r = requests.get(url, params=params)
    results = r.json()['results']

    if len(results) > 0:
        location = results[0]['geometry']['location']
        return (location['lat'], location['lng'])
    else:
        return (0, 0)

if __name__ == '__main__':
    print 'What kind of food do you want?'
    food = raw_input('>')
    OpenRice_contents = GetOpenRicePageContents(food.replace(' ', '%20'), 1)
    OpenRice_names = GetOpenRiceRestaurantsNames(OpenRice_contents)
    OpenRice_addresses = GetOpenRiceRestaurantsAddresses(OpenRice_contents)

    Yelp_contents = GetYelpPageContents(food.replace(' ', '+'), 1)
    Yelp_names = GetYelpRestaurantsNames(Yelp_contents)
    Yelp_addresses = GetYelpRestaurantsAddresses(Yelp_contents)

    print '--------------results from OpenRice--------------\n'

    for i in range(len(OpenRice_names)):
        (lat, lng) = GetGoogleMapCoordinate(OpenRice_addresses[i].strip())

        print OpenRice_names[i]
        print OpenRice_addresses[i].strip()

        if lat != 0 and lng != 0:
            print 'latitude:%f' % lat, 'longitude:%f' % lng
        
        print '\n'

        sleep(1)


    print '--------------results from Yelp-------------\n'
    
    for i in range(len(Yelp_names)):
        (lat, lng) = GetGoogleMapCoordinate(Yelp_addresses[i])

        print Yelp_names[i]
        print Yelp_addresses[i]

        if lat != 0 and lng != 0:
            print 'latitude:%f' % lat, 'longitude:%f' % lng
        
        print '\n'

        sleep(1)
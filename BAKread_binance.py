import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time
import curses
import os

def findCoin(title):
    listings = []
    with open('news.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
                for col in row:
                    if "Will List" in col and title == col:
                        return True                    

def new_coins():
    exist = findCoin("sss")
    print("------------------------------------")

    base_announcement_url = "https://www.binance.com"
    coin_market_cap_url_base = "https://coinmarketcap.com/currencies/"
    new_url = ""

    print("CALL")
    header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36","X-Requested-With": "XMLHttpRequest"}
    url = 'https://www.binance.com/en/support/announcement/c-48?navId=48'
    r = requests.get(url, headers = header)
    main_soup = BeautifulSoup(r.text, 'html.parser')
    listing_articles = main_soup.find("div", attrs={"class": "css-6f91y1"})
    #print(listing_articles.div)
    #new_initial_url_index = 42
    time.sleep(2.0) # time.sleep(1 * 60 * 5) 5min
    for e in listing_articles.div:
        try:
            e = str(e)
            #print(e)
            new_url_index = e.index('href=')
            #print(new_url_index)
            if new_url_index > 0:
                href_end_index = e[new_url_index:].index(">")
                new_url_href = e[new_url_index:]
                new_title_index = e[new_url_index:].index(">")
                new_title = new_url_href[new_title_index+1:].replace("</a>", "")

                if "View more" not in new_url_href and "Will List" in new_url_href:
                    new_url = new_url_href.split('"')[1]
                    coin_name_index = new_url_href.index("Will List")
                    end_coin_name_index = new_url_href.index("(")
                    coin_name = new_url_href[coin_name_index:end_coin_name_index]
                    coin_name = coin_name.replace("Will List ", "")
                    splited_coin_name = coin_name.split(" ")

                    #print(new_url_href)
                    #print(coin_name)
                    #print(new_title)
                    #print(base_announcement_url + new_url)

                    r = requests.get(base_announcement_url + new_url, headers = header)
                    main_soup = BeautifulSoup(r.text, 'html.parser')
                    article_date = main_soup.find("div", attrs={"class": "css-17s7mnd"})
                    time.sleep(2.0) # time.sleep(1 * 60 * 5) 5min
                    for a in article_date:
                        try:
                            #print(a)
                            article_date = a

                            for splited_name in splited_coin_name:
                                #print("splited_name")
                                #print(splited_name)
                                coin_market_cap_url_base += splited_name.lower()

                                coin_market_cap_url_base += "-"

                            #print("coin_market_cap_url_base")    
                            coin_market_cap_url_base = coin_market_cap_url_base.replace("--", "")
                            #print(coin_market_cap_url_base+"/market")   

                            os.system("script2.py 1")

                            with open("news.csv", "a") as csv_file:
                                writer = csv.writer(csv_file)
                                writer.writerow([new_title, base_announcement_url + new_url, article_date]) 

                            coin_market_cap_url_base = "https://coinmarketcap.com/currencies/"
                        except e:
                            print(e)
                        
        except:
           print("")
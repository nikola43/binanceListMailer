import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time
import curses
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from socket import gaierror
from telethon import TelegramClient, events
import asyncio


def findCoin(title):
    listings = []
    with open('news.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            for col in row:
                if title == col:
                    return True


async def new_coins(client):
    base_announcement_url = "https://www.binance.com"
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"}
    url = 'https://www.binance.com/en/support/announcement/c-48?navId=48'
    r = requests.get(url, headers=header)
    main_soup = BeautifulSoup(r.text, 'html.parser')
    listing_articles = main_soup.find("div", attrs={"class": "css-6f91y1"})
    ##time.sleep(2.0)  # time.sleep(1 * 60 * 5) 5min
    for e in listing_articles.div:
        try:
            e = str(e)
            new_url_index = e.index('href=')
            if new_url_index > 0:
                new_url_href = e[new_url_index:]
                if "View more" not in new_url_href and "Will List" in new_url_href or "Introducing" in new_url_href:
                    new_url = new_url_href.split('"')[1]
                    r = requests.get(base_announcement_url + new_url, headers=header)
                    main_soup = BeautifulSoup(r.text, 'html.parser')
                    article_date = main_soup.find("div", attrs={"class": "css-17s7mnd"})
                    # time.sleep(2.0)  # time.sleep(1 * 60 * 5) 5min

                    exist = findCoin(base_announcement_url + new_url)
                    if exist is None:
                        for x in range(30):
                            destination_user_username = 'Todos al tren'
                            entity = await client.get_entity(destination_user_username)
                            await client.send_message(entity=entity,
                                                      message="NUEVA MONEDA EN BINANCE, APRESURATE NEGRO " + base_announcement_url + new_url)
                            # send_mail(base_announcement_url + new_url, "pauloxti@gmail.com, erquesabesabe@gmail.com, rodriguezcardosojorge@gmail.com, robertobaus1@gmail.com")
                            time.sleep(5.0)

                        with open("news.csv", "a") as csv_file:
                            writer = csv.writer(csv_file)
                            writer.writerow([base_announcement_url + new_url, article_date])
                    # os.system("run.py 1")

        except:
            print("")


def send_mail(msg, to):
    mail_content = msg

    # The mail addresses and password
    sender_address = 'paulogst16@gmail.com'
    sender_pass = '-ArdBoard23'
    receiver_address = to
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'NUEVA MONEDA EN BINANCE, APRESURATE NEGRO'  # The subject line
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')


session = "test"
api_id = 2156362
api_hash = "0d96604bf1fa9092de979309d1606466"
proxy = None  # https://github.com/Anorov/PySocks
telegram = TelegramClient(session, api_id, api_hash, proxy=None).start()

if __name__ == "__main__":
    while True:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(new_coins(telegram))

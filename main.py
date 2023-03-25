from requests import get
from bs4 import BeautifulSoup

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import datetime


date = datetime.datetime.now()
today = f"{date.day:02d}-{date.month:02d}-{date.year}"
new_articles_count = 0
news_url = "https://www.sbnation.com/nfl-news"


def search_news(url: str) -> str:
    """
        This function is checking if there are any new articles that match the current date
        and if so, it creates a list of news links and returns it as a string
    """
    global new_articles_count
    content = f"<h1 style='font-family: Verdana, sans-serif'>Today's Top NFL news</h1>\n{'-'*70}\n<br><br>"
    try:
        res = get(url)
    except Exception as err:
        print(err)
    else:
        soup = BeautifulSoup(res.content, "html.parser")
        for index, tag in enumerate(soup.find_all("div", class_="c-entry-box--compact c-entry-box--compact--article")):      
            news_date = tag.find("span", class_="c-byline-wrapper").time.string.split(" ")[-1]
            if int(news_date) == date.day:
                new_articles_count += 1
                img = [*tag.div.children][3].img["src"]
                text = tag.h2.string
                news_link = tag.a["href"]
                new_line = f"""
                    <div style="display: flex; font-family: Verdana, sans-serif;">
                        <img src={img} style="display: block; width: 100px; height: 100px; object-fit: cover; margin-right: 1rem;"/>
                        <a href={news_link} target="_blank" style="font-size: 1.2rem; font-weight: 500; color: black; display: block; padding-top: 1.5rem">{text}</a>
                    </div>
                """
                content += f"{new_line}\n<br>"
    return content


email_content = search_news(news_url)

if new_articles_count:
    email_content += "<br>----------------------------------<br>"
    email_content += "<h4>End Of Message...</h4>"

    # email config
    SERVER = 'smtp.gmail.com' 
    PORT = 587 
    FROM = ''  # sender
    TO = ''  # receiver
    PWD = ''  # sender's password

    # email body
    email_body = MIMEMultipart()

    email_body["Subject"] = f"Top New NFL News for {today}"
    email_body["From"] = FROM
    email_body["To"] = TO

    email_body.attach(MIMEText(email_content, "html"))

    # sending email
    email_server = smtplib.SMTP(SERVER, PORT)
    email_server.set_debuglevel(1)
    email_server.ehlo()
    email_server.starttls()
    email_server.login(FROM, PWD)
    email_server.sendmail(FROM, TO, email_body.as_string())

    print("Email is sent")
    print()

    email_server.quit()
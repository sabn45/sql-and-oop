import sqlite3
import requests
import smtplib
import ssl
import selectorlib



url = "http://programmer100.pythonanywhere.com/tours/"


class Retrieve:
    def get_html(self, url):
        req = requests.get(url)
        html = req.text
        return html

    def scrape(self, html):
        selector = selectorlib.Extractor.from_yaml_file("scrape.yaml")
        value = selector.extract(html)['tours']
        return value


class Data:
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)

    def add_data(self, value):
        row = value.split(',')
        row = [item.strip() for item in row]
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
        self.connection.commit()

    def read_data(self, value):
        row = value.split(',')
        row = [item.strip() for item in row]
        band, city, date = row
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
        content = cursor.fetchall()
        return content


class Email:
    def send(self, message):
        host = "smtp.gmail.com"
        port = 465

        password = "x"
        sender = "pythonlearning475@gmail.com"
        receiver = "pythonlearning475@gmail.com"
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver, message.encode("utf-8"))


while True:
    extract = Retrieve()
    html = extract.get_html(url)
    value = extract.scrape(html)
    print(value)

    if value != "No upcoming tours":
        data_base = Data(db_path= 'data_sql.db')
        content = data_base.read_data(value)
        if not content:
            data_base.add_data(value)
            body = f"Hey, here is a text message!!{value}"
            subject_body = "Subject: Email from scrapping project\n\n" + body
            email = Email()
            email.send(subject_body)
            print("email sent")


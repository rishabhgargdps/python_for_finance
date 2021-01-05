import os
import smtplib
import imghdr
from email.message import EmailMessage
from decouple import config

import yfinance as yf
import datetime as dt
from time import sleep
import pandas as pd
from pandas_datareader import data as pdr

EMAIL_ADDRESS = config('EMAIL_USER')
EMAIL_PASSWORD= config('EMAIL_PASS')

msg=EmailMessage()
yf.pdr_override()
start = dt.datetime(2018, 12, 1)
now = dt.datetime.now()

stock = input("Enter the stock ticker: ")
TargetPrice = 9

msg["Subject"]= "Alert on "+stock
msg["From"]=EMAIL_ADDRESS
msg["To"]=EMAIL_ADDRESS
alerted=False

while 1:
    df = pdr.get_data_yahoo(stock , start, now)
    current_close = df["Adj Close"][-1]
    condition = current_close>TargetPrice
    if condition and alerted==False:
        message = stock+" Has activated the alert price of "+str(TargetPrice)+\
            "\nCurrent Price: "+str(current_close)
        msg.set_content(message)
        
        files = [r"/home/rishabhgarg/Downloads/Sample_stocks.ods"]
        for file in files:
            with open(file, 'rb') as f:
                file_data = f.read()
                file_name = "FundamentalList.xlsx"
                msg.add_attachment(file_data, maintype="application",
                subtype="ocetet-stream", filename=file_name)

        alerted=True
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print("Completed")
    else:
        print("No new alerts")
    sleep(60)
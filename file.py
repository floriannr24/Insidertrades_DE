import datetime
from datetime import timedelta, date
import yfinance as yf
import pandas as pd

df = pd.read_excel("C:/Users/FSX-P/Insider_DE.xlsx")

for index, row in df.iterrows():

    date5 = row["+5 Tage"].to_pydatetime()
    date10 = row["+10 Tage"].to_pydatetime()
    date20 = row["+20 Tage"].to_pydatetime()
    date30 = row["+30 Tage"].to_pydatetime()

    if date5.date() > date.today() or date10.date() > date.today() or date20.date() > date.today() or date30.date() > date.today():
        continue

    ticker = yf.Ticker(row["Code"])

    history = ticker.history(start=date5, end=date5 + timedelta(days=1))
    price5 = None
    for i, day in history.iterrows():
        price5 = round(day["Close"], 2)
    df.at[index, "Kurs5"] = price5

    history = ticker.history(start=date10, end=date10 + timedelta(days=1))
    price10 = None
    for i, day in history.iterrows():
        price10 = round(day["Close"], 2)
    df.at[index, "Kurs10"] = price10

    history = ticker.history(start=date20, end=date20 + timedelta(days=1))
    price20 = None
    for i, day in history.iterrows():
        price20 = round(day["Close"], 2)
    df.at[index, "Kurs20"] = price20

    history = ticker.history(start=date30, end=date30 + timedelta(days=1))
    price30 = None
    for i, day in history.iterrows():
        price30 = round(day["Close"], 2)
    df.at[index, "Kurs30"] = price30

    if price5:
        df.at[index, "%5"] = price5/row["Durchschnittspreis"]-1
    if price10:
        df.at[index, "%10"] = price10/row["Durchschnittspreis"]-1
    if price20:
        df.at[index, "%20"] = price20/row["Durchschnittspreis"]-1
    if price30:
        df.at[index, "%30"] = price30/row["Durchschnittspreis"]-1

    print(index)

df.to_excel("C:/Users/FSX-P/Insider_DE-df1.xlsx", index=False)
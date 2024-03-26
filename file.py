import datetime
from datetime import timedelta, date
import yfinance as yf
import pandas as pd
import pytz

# df = pd.read_excel("C:/Users/FSX-P/InsiderDE_2023-2024.xlsx")
#
# holidays = ["2023-04-10", "2023-05-01", "2023-12-25", "2023-12-26", "2024-01-01", "2023-04-07"]
# holidays_dates = [datetime.datetime.strptime(x, "%Y-%m-%d") for x in holidays]
#
# def dateIsHoliday(date):
#     return date in holidays_dates
#
#
# def dateAfterDays(date, days):
#     newDate = date + timedelta(days=days)
#
#     if newDate.isoweekday() == 6:
#         newDate = newDate + timedelta(days=2)
#
#     if newDate.isoweekday() == 7:
#         newDate = newDate + timedelta(days=1)
#
#     if dateIsHoliday(newDate):
#         newDate = dateAfterDays(newDate, 1)
#
#     return newDate
#
#
# df = df.dropna()
#
# df["Aggregiertes Volumen"] = df["Aggregiertes Volumen"].str[:-4]
# df["Aggregiertes Volumen"] = df["Aggregiertes Volumen"].str.replace(".", "").replace(",", ".")
# df["Aggregiertes Volumen"] = (df["Aggregiertes Volumen"].str.replace(",", ".")).astype(float)
#
# df["Durchschnittspreis"] = df["Durchschnittspreis"].str[:-4]
# df["Durchschnittspreis"] = df["Durchschnittspreis"].str.replace(".", "").replace(",", ".")
# df["Durchschnittspreis"] = (df["Durchschnittspreis"].str.replace(",", ".")).astype(float)
#
# for index, row in df.iterrows():
#
#     dateOfTrade = row["Datum des Geschäfts"].to_pydatetime()
#     tradePrice = row["Durchschnittspreis"]
#     upperthreshold = round(tradePrice * 1.02, 2)
#     lowerthreshold = round(tradePrice * 0.92, 2)
#
#     date5 = dateAfterDays(dateOfTrade, 5)
#     date10 = dateAfterDays(dateOfTrade, 10)
#     date20 = dateAfterDays(dateOfTrade, 20)
#     date30 = dateAfterDays(dateOfTrade, 30)
#
#     if date5.date() > date.today() or date10.date() > date.today() or date20.date() > date.today() or date30.date() > date.today():
#         continue
#
#     ticker = yf.Ticker(row["Code"])
#
#     history = ticker.history(start=date5, end=date5 + timedelta(days=1))
#     price5 = None
#     for i, day in history.iterrows():
#         price5 = round(day["Close"], 2)
#
#     history = ticker.history(start=date10, end=date10 + timedelta(days=1))
#     price10 = None
#     for i, day in history.iterrows():
#         price10 = round(day["Close"], 2)
#
#     history = ticker.history(start=date20, end=date20 + timedelta(days=1))
#     price20 = None
#     for i, day in history.iterrows():
#         price20 = round(day["Close"], 2)
#
#     history = ticker.history(start=date30, end=date30 + timedelta(days=1))
#     price30 = None
#     for i, day in history.iterrows():
#         price30 = round(day["Close"], 2)
#
#     overThreshold = 0
#     underThreshold = 0
#     dayOfUpperThreshold = None
#     dayOfLowerThreshold = None
#
#     history = ticker.history(start=dateOfTrade + timedelta(days=1), end=date30 + timedelta(days=1))
#     for i, day in history.iterrows():
#
#         if day["High"] > upperthreshold:
#             overThreshold += 1
#             if overThreshold == 1:
#                 dayOfUpperThreshold = i
#                 df.at[index, "daysAfterTradeUpperTHR"] = (dayOfUpperThreshold.replace(tzinfo = None) - dateOfTrade).days
#
#         if day["Low"] < lowerthreshold:
#                 underThreshold += 1
#                 if underThreshold == 1:
#                     dayOfLowerThreshold = i
#                     df.at[index, "daysAfterTradeLowerTHR"] = (dayOfLowerThreshold.replace(tzinfo = None) - dateOfTrade).days
#
#     tradingDays = len(history)
#
#     lower = False
#
#     if dayOfUpperThreshold and dayOfLowerThreshold:
#         if dayOfUpperThreshold < dayOfLowerThreshold:
#             df.at[index, "ThresholdReachedFirst"] = "upper"
#         if dayOfUpperThreshold > dayOfLowerThreshold:
#             df.at[index, "ThresholdReachedFirst"] = "lower"
#             lower = True
#
#     if lower or (underThreshold > 0 and overThreshold == 0):
#         df.at[index, "KO"] = "KO"
#
#     df.at[index, "overThresholdIn30days"] = overThreshold
#     df.at[index, "underThresholdIn30days"] = underThreshold
#     df.at[index, "tradingDays"] = tradingDays
#
#     if price5:
#         df.at[index, "%5"] = price5 / row["Durchschnittspreis"] - 1
#     if price10:
#         df.at[index, "%10"] = price10 / row["Durchschnittspreis"] - 1
#     if price20:
#         df.at[index, "%20"] = price20 / row["Durchschnittspreis"] - 1
#     if price30:
#         df.at[index, "%30"] = price30 / row["Durchschnittspreis"] - 1
#
#     print(index)
#
# df.to_excel("C:/Users/FSX-P/InsiderDE_2023-2024_Result.xlsx", index=True, index_label="Index")

df = pd.read_excel("C:/Users/FSX-P/InsiderDE_2023-2024_Result.xlsx")

df = df.sort_values(by="Datum des Geschäfts", ascending=False)

df["clump"] = None
clumps = []
timeframe = 4
tradesInTimeframe = 3

for index, row in df.iterrows():
    code = row["Code"]

    tradeDateOuter = row["Datum des Geschäfts"].to_pydatetime()
    dateEnd = tradeDateOuter - timedelta(days=timeframe)
    clumpIndex = 0
    clumpToCode = []

    for sindex, srow in df.iterrows():

        if srow["Code"] == code and not srow["clump"]:
            tradeDateInner = srow["Datum des Geschäfts"].to_pydatetime()
            if tradeDateInner < dateEnd or tradeDateInner > tradeDateOuter:
                break
            clumpToCode.append(sindex)

    if len(clumpToCode) >= tradesInTimeframe and not df.loc[index, "clump"]:
        clumpName = code + "_" + str(clumpIndex)

        for clumpPart in clumpToCode:
            df.loc[clumpPart, "clump"] = clumpName

df.to_excel("C:/Users/FSX-P/InsiderDE_2023-2024_Result.xlsx", index=False)

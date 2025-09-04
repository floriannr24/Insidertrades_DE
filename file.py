import datetime
from datetime import timedelta, date

import numpy as np
import yfinance as yf
import pandas as pd
import copy

from yfinance.exceptions import YFException

holidays = ["2023-04-10", "2023-05-01", "2023-12-25", "2023-12-26", "2024-01-01", "2023-04-07"]
holidays_dates = [datetime.datetime.strptime(x, "%Y-%m-%d") for x in holidays]

def dateIsHoliday(date):
    return date in holidays_dates

def dateAfterDays(date, days):
    newDate = date + timedelta(days=days)

    if newDate.isoweekday() == 6:
        newDate = newDate + timedelta(days=2)

    if newDate.isoweekday() == 7:
        newDate = newDate + timedelta(days=1)

    if dateIsHoliday(newDate):
        newDate = dateAfterDays(newDate, 1)

    return newDate


def fetchData(df):

    historyCached = {
        "code": None,
        "lastDate": None,
        "history": None
    }

    for i, row in df.iterrows():

        code = row["Code"]

        if pd.isnull(code):
            continue

        dateOfTrade = row["Datum des Geschäfts"].to_pydatetime()

        date5 = dateAfterDays(dateOfTrade, 5)
        date10 = dateAfterDays(dateOfTrade, 10)
        date20 = dateAfterDays(dateOfTrade, 20)
        date30 = dateAfterDays(dateOfTrade, 30)
        date60 = dateAfterDays(dateOfTrade, 60)

        if not pd.isnull(df.loc[i, "DataFetched"]):
            continue

        if date5.date() > date.today() or date10.date() > date.today() or date20.date() > date.today() or date30.date() > date.today():
            continue

        if historyCached["code"] == code and historyCached["lastDate"] >= date30:
            history = historyCached["history"]
        else:
            ticker = yf.Ticker(code)
            history = ticker.history(start=dateOfTrade, end=date60 + timedelta(days=1))
            history.index = pd.to_datetime(history.index).date

            historyCached["code"] = code
            historyCached["lastDate"] = date60
            historyCached["history"] = history

        price5 = None
        price10 = None
        price20 = None
        price30 = None

        try:
            price5 = history.loc[date5.date(), "Open"]
            price10 = history.loc[date10.date(), "Open"]
            price20 = history.loc[date20.date(), "Open"]
            price30 = history.loc[date30.date(), "Open"]
        except KeyError:
            print(f"{code} Error while fetching price data")
            print("---------")
            continue

        tradePrice = row["Durchschnittspreis"]
        upperthreshold = round(tradePrice * 1.02, 2)
        lowerthreshold = round(tradePrice * 0.92, 2)

        # overThreshold = 0
        # underThreshold = 0
        # dayOfUpperThreshold = None
        # dayOfLowerThreshold = None
        #
        # history = ticker.history(start=dateOfTrade + timedelta(days=1), end=date30 + timedelta(days=1))
        # for i, day in history.iterrows():
        #
        #     if day["High"] > upperthreshold:
        #         overThreshold += 1
        #         if overThreshold == 1:
        #             dayOfUpperThreshold = i
        #             df_fetchedData.at[i, "daysAfterTradeUpperTHR"] = (
        #                         dayOfUpperThreshold.replace(tzinfo=None) - dateOfTrade).days
        #
        #     if day["Low"] < lowerthreshold:
        #         underThreshold += 1
        #         if underThreshold == 1:
        #             dayOfLowerThreshold = i
        #             df_fetchedData.at[i, "daysAfterTradeLowerTHR"] = (
        #                         dayOfLowerThreshold.replace(tzinfo=None) - dateOfTrade).days
        #
        # tradingDays = len(history)
        #
        # lower = False
        #
        # if dayOfUpperThreshold and dayOfLowerThreshold:
        #     if dayOfUpperThreshold < dayOfLowerThreshold:
        #         df_fetchedData.at[i, "ThresholdReachedFirst"] = "upper"
        #     if dayOfUpperThreshold > dayOfLowerThreshold:
        #         df_fetchedData.at[i, "ThresholdReachedFirst"] = "lower"
        #         lower = True
        #
        # if lower or (underThreshold > 0 and overThreshold == 0):
        #     df_fetchedData.at[i, "KO"] = "KO"
        #
        # df_fetchedData.at[i, "overThresholdIn30days"] = overThreshold
        # df_fetchedData.at[i, "underThresholdIn30days"] = underThreshold
        # df_fetchedData.at[i, "tradingDays"] = tradingDays

        if price5 and price10 and price20 and price30:
            df.at[i, "DataFetched"] = "yes"

        if price5:
            df.at[i, "%5"] = price5 / row["Durchschnittspreis"] - 1
        if price10:
            df.at[i, "%10"] = price10 / row["Durchschnittspreis"] - 1
        if price20:
            df.at[i, "%20"] = price20 / row["Durchschnittspreis"] - 1
        if price30:
            df.at[i, "%30"] = price30 / row["Durchschnittspreis"] - 1

        print(row["Code"], row["Mitteilungsdatum"])
        print("---------")

    return df


def fetchAndSaveData():

    df = loadDataframe()
    df_calculated = fetchData(df)
    df_calculated.to_excel("C:/Users/FSX-P/bafin/InsiderDE_2023-2024_Result1.xlsx", index=False)


def loadDataframe():
    df = pd.read_excel("C:/Users/FSX-P/bafin/Gesamt.xlsx")
    df = df.dropna(subset=["Durchschnittspreis"])
    df["Aggregiertes Volumen"] = df["Aggregiertes Volumen"].str[:-4]
    df["Aggregiertes Volumen"] = df["Aggregiertes Volumen"].str.replace(".", "").replace(",", ".")
    df["Aggregiertes Volumen"] = (df["Aggregiertes Volumen"].str.replace(",", ".")).astype(float)
    df["Durchschnittspreis"] = df["Durchschnittspreis"].str[:-4]
    df["Durchschnittspreis"] = df["Durchschnittspreis"].str.replace(".", "").replace(",", ".")
    df["Durchschnittspreis"] = (df["Durchschnittspreis"].str.replace(",", ".")).astype(float)
    df = df.sort_values(["Code", "Mitteilungsdatum"], ascending=[True, True])
    return df


fetchAndSaveData()



# df = pd.read_excel("C:/Users/FSX-P/InsiderDE_2023-2024_Result.xlsx")

# df = df.sort_values(by="Datum des Geschäfts", ascending=False)

# df["clump"] = None
# clumps = []
# timeframe = 4
# tradesInTimeframe = 3

# for index, row in df.iterrows():
#     code = row["Code"]

#     tradeDateOuter = row["Datum des Geschäfts"].to_pydatetime()
#     dateEnd = tradeDateOuter - timedelta(days=timeframe)
#     clumpIndex = 0
#     clumpToCode = []

#     for sindex, srow in df.iterrows():

#         if srow["Code"] == code and not srow["clump"]:
#             tradeDateInner = srow["Datum des Geschäfts"].to_pydatetime()
#             if tradeDateInner < dateEnd or tradeDateInner > tradeDateOuter:
#                 break
#             clumpToCode.append(sindex)

#     if len(clumpToCode) >= tradesInTimeframe and not df.loc[index, "clump"]:
#         clumpName = code + "_" + str(clumpIndex)

#         for clumpPart in clumpToCode:
#             df.loc[clumpPart, "clump"] = clumpName

# df.to_excel("C:/Users/FSX-P/InsiderDE_2023-2024_Result.xlsx", index=False)

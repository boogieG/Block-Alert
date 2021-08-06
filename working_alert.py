import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr
from scipy import stats
import matplotlib.pyplot as plt
import math
from datetime import date
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from collections import OrderedDict, defaultdict

yf.pdr_override()

lstTickers = ['QCOM', 'BABA', 'AMD']

start = dt.datetime(2017, 12, 1)
now = dt.datetime.now()

# leave 'inf' floats as upper and lower bounds to be sure to include 0% txn and 100+% txn
# program excludes lower limits and includes upper i.e. 0-10 would be every number except 0 to 10 including 10

bins = [-float('inf'), 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 99, float('inf')]
# bins= [-float('inf'), 9.99, 19.99, 29.99,39.99,49.99,59.99,69.99,79.99,89.99,99.99, float('inf')]

bindf = ['0-5', '6-10', '11-15', '16-20', '21-25', '26-30', '31-35', '36-40', '41-45', '46-50', '51-55', '56-60',
         '61-65', '66-70', '71-75', '76-80', '81-85', '86-90', '91-95', '96-99', '100+']
# bindf = ['0-9.99', '10-19.99', '20-29.99', '30-39.99', '40-49.99', '50-59.99', '60-69.99', '70-79.99', '80-89.99',
# '90-99.99', '100+']

bin_labels = pd.DataFrame(bindf)

# --------------------------------------------------------------------------------------------------
# read data

csv_df = pd.read_csv("C:/Users/bengo/PycharmProjects/pythonProject1/data/10.28-12.11.20_Blocks.csv")
csv_df = csv_df.replace(',', '', regex=True)
csv_df['Date'] = pd.to_datetime(csv_df['Date'])
csv_df[['Price', 'MoneyFlow', 'Size', '% of 14d']] = csv_df[['Price', 'MoneyFlow', 'Size', '% of 14d']].apply(
    pd.to_numeric)

# --------------------------------------------------------------------------------------------------
# create dictionary

data = defaultdict(OrderedDict)

for sym in lstTickers:

    block_df = csv_df.loc[csv_df.Symbol == sym]

    df = pdr.get_data_yahoo(sym, start, now)
    df = df.reset_index(inplace=False)
    df_list = df.values.tolist()

    bin_means, bin_edges, binnumber = stats.binned_statistic(block_df['% of 14d'],
                                                             block_df['Price'],
                                                             statistic='mean',
                                                             bins=bins)
    bin_means = pd.Series(bin_means, name='bin_means')
    bin_edges = pd.Series(bin_edges, name='bin_edges')
    binnumber = pd.Series(binnumber, name='binnumber')
    # bin_df = []
    # bin_df= ['0-9.99', '10-19.99', '20-29.99', '30-39.99', '40-49.99', '50-59.99', '60-69.99', '70-79.99',
    #                       '80-89.99', '90-99.99', '100+']
    # bin_labels = pd.DataFrame(bin_df)
    bin_df = pd.DataFrame(bin_means)
    bin_df.columns = ['Bin Mean']
    bin_df['% of 14d'] = bindf
    bins_bins = pd.cut(block_df['% of 14d'],
                       bins=bins, include_lowest=True,
                       labels=bindf, ordered=False)
    bin_count = pd.value_counts(bins_bins)
    bin_countdf = pd.DataFrame(bin_count)
    bin_countdf = bin_countdf.reset_index(inplace=False)
    bin_countdf.columns = ['% of 14d', 'Frequency']
    bin_info = bin_df.merge(bin_countdf, on='% of 14d')
    print(bin_info)

    for stat in [bin_means]:
        data[sym][stat.name] = stat
        # print(data)
        # print(stat)

        alert_price = df.iloc[-1, 5]
        print(alert_price)
        alert_date = df.iloc[-1, 0]
        last_price = df.iloc[-1, 5]
        last_price_2 = df.iloc[-2, 5]

        bin_0 = stat.iloc[0]
        bin_1 = stat.iloc[1]
        bin_2 = stat.iloc[2]
        bin_3 = stat.iloc[3]
        bin_4 = stat.iloc[4]
        bin_5 = stat.iloc[5]
        bin_6 = stat.iloc[6]
        bin_7 = stat.iloc[-4]
        bin_8 = stat.iloc[-3]
        bin_9 = stat.iloc[-2]
        bin_10 = stat.iloc[-1]

        bin_0_label = bin_labels.iloc[0]
        print(bin_0_label)
        bin_1_label = bin_labels.iloc[1]
        bin_2_label = bin_labels.iloc[2]
        bin_3_label = bin_labels.iloc[3]
        bin_4_label = bin_labels.iloc[4]
        bin_5_label = bin_labels.iloc[5]
        bin_6_label = bin_labels.iloc[6]
        bin_7_label = bin_labels.iloc[7]
        bin_8_label = bin_labels.iloc[8]
        bin_9_label = bin_labels.iloc[9]
        bin_10_label = bin_labels.iloc[10]
        print(bin_10_label)

        # --------------------------------------------------------------------------------------------------

        # Checking if price crossed up 0-9.99% bin level
        if last_price_2 < bin_0 < last_price:
            cond_0_Up = True
            print('Cross up true on: ' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(
                bin_0_label) + ' bin')
        if last_price_2 > bin_0 > last_price:
            cond_0_Down = True
            print('Cross down true on: ' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(
                bin_0_label) + ' bin')

        # Checking if price crossed 10-19.99% bin level
        if last_price_2 < bin_1 < last_price:
            cond_1_Up = True
            print('Cross Up True on: ' + str(sym) + ' on' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(
                bin_1_label) + ' bin')
        if last_price_2 > bin_1 > last_price:
            cond_1_Down = True
            print(
                'Cross down true on: ' + str(sym) + ' on' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(
                    bin_1_label) + ' bin')

        # Checking if price crossed 20-29.99% bin level
        if last_price_2 < bin_2 < last_price:
            cond_2_Up = True
            print('Cross Up True on: ' + str(sym) + ' on' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(
                bin_2_label) + ' bin')
        if last_price_2 > bin_2 > last_price:
            cond_2_Down = True
            print(
                'Cross down true on: ' + str(sym) + ' on' + str(alert_date) + ' at' + str(alert_price) + ' for ' + str(
                    bin_2_label) + ' bin')

        # Checking if price crossed 30-39.99% bin level
        if last_price_2 < bin_3 < last_price:
            cond_3_Up = True
            print(
                'Cross up True on: ' + str(sym) + ' on' + str(alert_date) + ' at' + str(alert_price) + ' for ' + str(
                    bin_3_label) + ' bin')
        if last_price_2 > bin_3 > last_price:
            cond_3_Down = True
            print(
                'Cross down true on: ' + str(sym) + ' on' + str(alert_date) + ' at' + str(alert_price) + ' for ' + str(
                    bin_3_label) + ' bin')

        # Checking if price crossed 40-49.99% bin level
        if last_price_2 < bin_4 < last_price:
            cond_4_Up = True
            print('Cross Up True on: ' + str(sym) + ' on' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(
                bin_4_label) + ' bin')
        if last_price_2 > bin_4 > last_price:
            cond_4_Down = True
            print(
                'Cross down true on: ' + str(sym) + ' on' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(
                    bin_4_label) + ' bin')

        # Checking if price crossed 50-59.99% bin level
        if last_price_2 < bin_5 < last_price:
            cond_5_Up = True
            print('Cross Up True on: ' + str(sym) + ' on' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(
                bin_5_label) + ' bin')
        if last_price_2 > bin_5 > last_price:
            cond_4_Down = True
            print(
                'Cross down true on: ' + str(sym) + ' on' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(
                    bin_5_label) + ' bin')

        # Checking if price crossed 60-69.99% bin level
        if last_price_2 < bin_6 < last_price:
            cond_6_Up = True
            print('Cross Up True on: ' + str(sym) + ' on' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(
                bin_6_label) + ' bin')
        if last_price_2 > bin_6 > last_price:
            cond_6_Down = True
            print(
                'Cross down true on: ' + str(sym) + ' on' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(
                    bin_6_label) + ' bin')

        # Checking if price crossed 70-79.99% bin level
        if last_price_2 < bin_7 < last_price:
            cond_7_Up = True
            print('Cross up True on: ' + str(sym) + ' on' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(
                bin_7_label) + ' bin')
        if last_price_2 > bin_7 > last_price:
            cond_7_Down = True
            print(
                'Cross down true on: ' + str(sym) + ' on' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(
                    bin_7_label) + ' bin')

        # Checking if price crossed 80-89.99% bin level
        if last_price_2 < bin_8 < last_price:
            cond_8_Up = True
            print('Cross Up True on: ' + str(sym) + ' on' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(
                bin_8_label) + ' bin')
        if last_price_2 > bin_8 > last_price:
            cond_8_Down = True
            print(
                'Cross down true on: ' + str(sym) + ' on' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(
                    bin_8_label) + ' bin')

        # Checking if price crossed 90-99.99% bin level
        if last_price_2 < bin_9 < last_price:
            cond_9_Up = True
            print(
                'Cross UpTrue on: ' + str(sym) + ' on' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(
                    bin_9_label) + ' bin')
        if last_price_2 > bin_9 > last_price:
            cond_0_Down = True
            print(
                'Cross down true on: ' + str(sym) + ' on' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(
                    bin_9_label) + ' bin')

        # Checking if price crossed 100+% bin level
        if last_price_2 < bin_10 < last_price:
            cond_10_Up = True
            print('Cross Up True on: ' + str(sym) + ' on' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(
                bin_10_label) + ' bin')
        if last_price_2 > bin_10 > last_price:
            cond_10_Down = True
            print(
                'Cross down true on: ' + str(sym) + ' on' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(
                    bin_0_label) + ' bin')

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# STOP HERE

print('\n')

# stat = pd.DataFrame(bin_means)
# stat.columns = ['Bin Mean']
# stat['% of 14d'] = [
#         '0-9.99',
#         '10-19.99',
#         '20-29.99',
#         '30-39.99',
#         '40-49.99',
#         '50-59.99',
#         '60-69.99',
#         '70-79.99',
#         '80-89.99',
#         '90-99.99',
#         '100+'

# alert_price = df.iloc[-1, 5]
# alert_date = df.iloc[-1, 0]
# last_price = df.iloc[-1, 5]
# last_price_2 = df.iloc[-2, 5]
#
# bin_0 = stat.iloc[0, 0]
# bin_1 = stat.iloc[1, 0]
# bin_2 = stat.iloc[2, 0]
# bin_3 = stat.iloc[3, 0]
# bin_4 = stat.iloc[4, 0]
# bin_5 = stat.iloc[5, 0]
# bin_6 = stat.iloc[6, 0]
# bin_7 = stat.iloc[7, 0]
# bin_8 = stat.iloc[8, 0]
# bin_9 = stat.iloc[9, 0]
# bin_10 = stat.iloc[10, 0]
#
# bin_0_label = stat.iloc[0, 1]
# bin_1_label = stat.iloc[1, 1]
# bin_2_label = stat.iloc[2, 1]
# bin_3_label = stat.iloc[3, 1]
# bin_4_label = stat.iloc[4, 1]
# bin_5_label = stat.iloc[5, 1]
# bin_6_label = stat.iloc[6, 1]
# bin_7_label = stat.iloc[7, 1]
# bin_8_label = stat.iloc[8, 1]
# bin_9_label = stat.iloc[9, 1]
# bin_10_label = stat.iloc[10, 1]
#
#
# # --------------------------------------------------------------------------------------------------
#
# # Checking if price crossed up 0-9.99% bin level
# if (last_price_2 < bin_0 < last_price):
#     cond_0_Up = True
#     print('Cross up true on: ' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(bin_0_label) + ' bin')
# if (last_price_2 > bin_0 > last_price):
#     cond_0_Down = True
#     print('Cross down true on: ' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(bin_0_label) + ' bin')
#
# # Checking if price crossed 10-19.99% bin level
# if (last_price_2 < bin_1 < last_price):
#     cond_1_Up = True
#     print('Cross Up True on: ' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(bin_1_label) + ' bin')
# if (last_price_2 > bin_1 > last_price):
#     cond_1_Down = True
#     print('Cross down true on: ' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(bin_1_label) + ' bin')
#
# # Checking if price crossed 20-29.99% bin level
# if (last_price_2 < bin_2 < last_price):
#     cond_2_Up = True
#     print('Cross Up True on: ' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(bin_2_label) + ' bin')
# if (last_price_2 > bin_2 > last_price):
#     cond_2_Down = True
#     print('Cross down true on: ' + str(alert_date) + ' at' + str(alert_price) + ' for ' + str(bin_2_label) + ' bin')
#
# # Checking if price crossed 30-39.99% bin level
# if (last_price_2 < bin_3 < last_price):
#     cond_3_Up = True
#     print('Cross up True on: ' + str(alert_date) + ' at' + str(alert_price) + ' for ' + str(bin_3_label) + ' bin')
# if (last_price_2 > bin_3 > last_price):
#     cond_3_Down = True
#     print('Cross down true on: ' + str(alert_date) + ' at' + str(alert_price) + ' for ' + str(bin_3_label) + ' bin')
#
# # Checking if price crossed 40-49.99% bin level
# if (last_price_2 < bin_4 < last_price):
#     cond_4_Up = True
#     print('Cross Up True on: ' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(bin_4_label) + ' bin')
# if (last_price_2 > bin_4 > last_price):
#     cond_4_Down = True
#     print('Cross down true on: ' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(bin_4_label) + ' bin')
#
# # Checking if price crossed 50-59.99% bin level
# if (last_price_2 < bin_5 < last_price):
#     cond_5_Up = True
#     print('Cross Up True on: ' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(bin_5_label) + ' bin')
# if (last_price_2 > bin_5 > last_price):
#     cond_4_Down = True
#     print('Cross down true on: ' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(bin_5_label) + ' bin')
#
# # Checking if price crossed 60-69.99% bin level
# if (last_price_2 < bin_6 < last_price):
#     cond_6_Up = True
#     print('Cross Up True on: ' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(bin_6_label) + ' bin')
# if (last_price_2 > bin_6 > last_price):
#     cond_6_Down = True
#     print('Cross down true on: ' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(bin_6_label) + ' bin')
#
# # Checking if price crossed 70-79.99% bin level
# if (last_price_2 < bin_7 < last_price):
#     cond_7_Up = True
#     print('Cross up True on: ' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(bin_7_label) + ' bin')
# if (last_price_2 > bin_7 > last_price):
#     cond_7_Down = True
#     print('Cross down true on: ' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(bin_7_label) + ' bin')
#
# # Checking if price crossed 80-89.99% bin level
# if (last_price_2 < bin_8 < last_price):
#     cond_8_Up = True
#     print('Cross Up True on: ' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(bin_8_label) + ' bin')
# if (last_price_2 > bin_8 > last_price):
#     cond_8_Down = True
#     print('Cross down true on: ' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(bin_8_label) + ' bin')
#
# # Checking if price crossed 90-99.99% bin level
# if (last_price_2 < bin_9 < last_price):
#     cond_9_Up = True
#     print('Cross UpTrue on: ' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(bin_9_label) + ' bin')
# if (last_price_2 > bin_9 > last_price):
#     cond_0_Down = True
#     print('Cross down true on: ' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(bin_9_label) + ' bin')
#
# # Checking if price crossed 100+% bin level
# if (last_price_2 < bin_10 < last_price):
#     cond_10_Up = True
#     print('Cross Up True on: ' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(bin_10_label) + ' bin')
# if (last_price_2 > bin_10 > last_price):
#     cond_10_Down = True
#     print('Cross down true on: ' + str(alert_date) + ' at ' + str(alert_price) + ' for ' + str(bin_0_label) + ' bin')

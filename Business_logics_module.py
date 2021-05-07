import PySimpleGUI as gui
from datetime import  date

import numpy
from plotly.subplots import make_subplots
from Folder_operations_module import  Folder_Operation

import datetime, calendar
from pandas import  DataFrame
import re
#from automated_finance_system.Option_Data_Processing import Option_Data
import pandas as pd
import matplotlib.pyplot as plt
import time
from Option_data_module import Option_Data
from NextDay_watchlist_summary import class_Next_Day_watchlist_summary

class Business_Logics:

    def Future_chart(self,stock_symbol_passed):
        pass
        # b_object = BusinessLogic.Future_data_processing()
        #
        # FilePath = b_object.get_Total_files()
        # Total_Number_of_Files = len(FilePath)
        #
        # dataFrame = [None] * Total_Number_of_Files
        # df_Contracts_and_OIchange_complete = [None] * Total_Number_of_Files
        # df_Contracts_and_OIchange_slice = [None] * Total_Number_of_Files
        # stock_symbol = stock_symbol_passed
        # cumulativeOI = []
        # for file_index in range(0, Total_Number_of_Files):
        #     dataFrame = pd.read_csv(FilePath[file_index])
        #     dataFrame_Consolidated_COI = dataFrame[(dataFrame['SYMBOL'] == stock_symbol.upper()) & ((dataFrame['INSTRUMENT'] == 'FUTSTK'))]
        #     dataFrame_Consolidated_COI = (
        #     dataFrame_Consolidated_COI[dataFrame_Consolidated_COI['EXPIRY_DT'] == '29-Oct-2020'])
        #     cumulativeOI.append(dataFrame_Consolidated_COI['OPEN_INT'].iloc[0])
        #
        # date_list = []
        # for i in range(len(FilePath)):
        #     date_list.append(FilePath[i].split("\\")[2].rstrip("bhav.csv").rstrip("2020").split("_")[1].lstrip("fo"))
        #
        # dates = date_list
        # COI = cumulativeOI
        #
        # fig = go.Figure(data=go.Bar(x=dates, y=COI))
        # fig.show()

    def Get_the_List_Of_Stocks(self):
        df_stock_list = pd.read_csv(Folder_Operation.stock_list_path)
        df_stock_list =df_stock_list[(df_stock_list['INSTRUMENT'] == 'FUTSTK')]
        total_list = list(df_stock_list['SYMBOL'])
        stock_list = []
        for i in total_list:
            if i not in stock_list:
                stock_list.append(i)
            stock_list.sort()
        return stock_list

    def Get_the_List_Of_cash_Stocks(self):
        df_stock_list = pd.read_csv(Folder_Operation.cash_stock_list_path)
        print(df_stock_list.columns)
        df_stock_list = df_stock_list[(df_stock_list[' SERIES'] == ' EQ')]
        total_list = list(df_stock_list['SYMBOL'])
        stock_list = []
        for i in total_list:
            if i not in stock_list:
                stock_list.append(i)
            stock_list.sort()
        return stock_list

    def Get_the_List_Of_MidCap_Stocks(self):
        df_stock_list = pd.read_csv(Folder_Operation.Nifty_400_stock_list_path)

        total_list = list(df_stock_list['Symbol'])
        stock_list = []
        for i in total_list:
            if i not in stock_list:
                stock_list.append(i)
            stock_list.sort()
        return stock_list

    def Plot_Futures_Data_chart(self):
        FilePath = Folder_Operation.Downloaded_FO_Bhav_CopyFiles(self)

        Total_Number_of_Files = len(FilePath)

        df_futures = [None] * Total_Number_of_Files
        df_Contracts_and_OIchange_complete = [None] * Total_Number_of_Files
        df_Contracts_and_OIchange_slice = [None] * Total_Number_of_Files

        for file_index in range(0, Total_Number_of_Files):
            # print(FilePath[file_index])
            df_futures[file_index] = pd.read_csv(FilePath[file_index])

            # df_Contracts_and_OIchange_complete[file_index]= df_futures[file_index][(df_futures[file_index]['INSTRUMENT'] == 'FUTSTK') & (df_futures[file_index]['EXPIRY_DT'] == '28-May-2020')]
            df_Contracts_and_OIchange_complete[file_index] = df_futures[file_index][
                (df_futures[file_index]['INSTRUMENT'] == 'FUTSTK') & (
                (df_futures[file_index]['EXPIRY_DT'] == '29-Oct-2020'))]
            # df_Contracts_and_OIchange_complete[file_index] = df_futures[file_index][(df_futures[file_index]['INSTRUMENT'] == 'FUTSTK') & (df_futures[file_index]['EXPIRY_DT'] == '30-Jul-2020')]
            df_Contracts_and_OIchange_slice[file_index] = df_Contracts_and_OIchange_complete[file_index][
                ['SYMBOL', 'CONTRACTS', 'CHG_IN_OI', 'CLOSE', 'OPEN_INT']]

        df_semi = [None] * Total_Number_of_Files
        df_semi[0] = pd.merge(df_Contracts_and_OIchange_slice[0], df_Contracts_and_OIchange_slice[1], on="SYMBOL",
                              how="left")
        df_semi[0].rename(
            columns={"CONTRACTS_x": "CONTRACTS_N", "CHG_IN_OI_x": "CHG_IN_OI_N", "CONTRACTS_y": "CONTRACTS_N_1",
                     "CHG_IN_OI_y": "CHG_IN_OI_N_1"}, inplace=True)

        for i in range(1, (Total_Number_of_Files - 1)):
            # print("sushen {}".format(i))
            df_semi[i] = pd.merge(df_semi[i - 1], df_Contracts_and_OIchange_slice[i + 1], on="SYMBOL", how="left")
            df_semi[i].rename(
                columns={"CONTRACTS": "CONTRACTS_N_{}".format(i + 1), "CHG_IN_OI": "CHG_IN_OI_N_{}".format(i + 1)},
                inplace=True)

        full_list = []
        for index, row in df_semi[(Total_Number_of_Files - 2)].iterrows():

            sub_list = []
            sub_list.append(row["SYMBOL"])

            sub_list.append(row["CHG_IN_OI_N"])
            for i in range(2, Total_Number_of_Files):
                sub_list.append(row["CHG_IN_OI_N_{0}".format(i)])

            sub_list.append(row["CONTRACTS_N"])
            for i in range(2, Total_Number_of_Files):
                sub_list.append(row["CONTRACTS_N_{0}".format(i)])

            full_list.append(sub_list)

        total_number_of_elemnts = len(full_list)
        for index in range(total_number_of_elemnts):
            stock_specific_data = full_list[index]

            if (stock_specific_data[0] == 'AXISBANK'):
                print(stock_specific_data)
                # sliced_data = stock_specific_data[(Total_Number_of_Files-1):(len(stock_specific_data)+1)]
                sliced_data = stock_specific_data[1:(Total_Number_of_Files + 1)]
                # print("{0}:{1}".format((Total_Number_of_Files),(len(stock_specific_data)+1)))

        date_list = []
        for i in range(len(FilePath)):
            date_list.append(FilePath[i].split("\\")[2].rstrip("bhav.csv").rstrip("2020").split("_")[1].lstrip("fo"))

        dates = date_list
        Open_interest = sliced_data
        # Open_interest = Open_interest[::-1]

        plt.ylabel('Change in Open Interest : Futures Derivatives')
        plt.xlabel('Date on which Data Recorded')
        plt.title("Trend of Change in Open Interest in Futures Data")
        plt.xticks(rotation=55)
        plt.legend(['SKDA'])
        plt.plot(dates, Open_interest)
        plt.grid(True, color='k', linestyle=':')

        plt.show()


    def Find_Expiry_Date_For_Current_Month(self,year,month):
        # Create a datetime.date for the last day of the given month
        daysInMonth = calendar.monthrange(year, month)[1]  # Returns (month, numberOfDaysInMonth)
        dt = datetime.date(year, month, daysInMonth)

        # Back up to the most recent Thursday
        offset = 4 - dt.isoweekday()
        if offset > 0: offset -= 7  # Back up one week if necessary
        dt += datetime.timedelta(offset)  # dt is now date of last Th in month

        # Throw an exception if dt is in the current month and occurred before today
        now = datetime.date.today()  # Get current date (local time, not utc)
        if dt.year == now.year and dt.month == now.month and dt < now:
            pass
            #raise Exception('Oops - missed the last Thursday of this month')
        x = datetime.datetime(dt.year,dt.month,dt.day)
        dt = x.strftime("%d-%b-%Y").upper()
        return dt

    def Process_Future_data_for_stock(self,stock_symbol,Consolidated_future__dataframe,expiry_Date_For_Current_Month,expiry_Date_For_Previous_Month):
      if stock_symbol in self.Get_the_List_Of_Stocks():
            # MainDataFrame = []
            # for filename in FO_Files_list:
            #     dataFrame = pd.read_csv(filename)
            #     dataFrame_Consolidated_COI = dataFrame[(dataFrame['SYMBOL'] == stock_symbol.upper()) & ((dataFrame['INSTRUMENT'] == 'FUTSTK'))]
            #     dataFrame["Cumlative COI"] = dataFrame_Consolidated_COI['OPEN_INT'].sum()
            #     MainDataFrame.append((dataFrame))
            # dataFrame = pd.concat(MainDataFrame)
            dataFrame = Consolidated_future__dataframe.copy(deep=True)
            dataFrame["Cumlative COI"] = dataFrame['OPEN_INT'].sum()
            dataFrame = dataFrame[((dataFrame['EXPIRY_DT'] == expiry_Date_For_Current_Month)|(dataFrame['EXPIRY_DT'] == expiry_Date_For_Previous_Month)) & (dataFrame['INSTRUMENT'] == 'FUTSTK')]
            dataFrame = dataFrame[dataFrame['SYMBOL'] == stock_symbol.upper()]
            dataFrame['PO_Ratio'] = dataFrame['CHG_IN_OI']/dataFrame['CONTRACTS']
            dataFrame['ClOP'] = dataFrame['CLOSE']-dataFrame['OPEN']
            dataFrame['HiLo'] = dataFrame['HIGH'] - dataFrame['LOW']
            dataFrame['Wick'] = (abs(abs(dataFrame['HiLo']) - abs(dataFrame['ClOP'])))
            dataFrame['ClOP_per'] = (100 - (((dataFrame['CLOSE'] - dataFrame['ClOP']) * 100) / dataFrame['CLOSE']))
            dataFrame['Wick_Per_On_Spot'] = (100 - (((dataFrame['CLOSE'] - dataFrame['Wick'])*100)/dataFrame['CLOSE']))
            dataFrame['HiLo_Percentage'] = ((dataFrame['HIGH']-dataFrame['LOW'])*100)/dataFrame['HIGH']
            dataFrame['vol_dis'] = dataFrame['CONTRACTS']/dataFrame['HiLo_Percentage']
            dataFrame['Alert'] = ""
            dataFrame.loc[(dataFrame['ClOP_per'] < dataFrame['Wick_Per_On_Spot']), ['Alert']] = "HIGH"

            dataFrame['vol_dis_old'] = dataFrame['vol_dis'].shift(1, fill_value=0, axis=0)
            dataFrame['Per_vol_Updown'] = ((dataFrame['vol_dis'] - dataFrame['vol_dis_old'])*100)/dataFrame['vol_dis']
            dataFrame['x_factor'] = (abs(abs(dataFrame['Wick_Per_On_Spot'])/abs(dataFrame['ClOP_per'])))
            dataFrame['COI_Percentage'] = (dataFrame['CHG_IN_OI']/dataFrame['OPEN_INT'])*100
            dataFrame["vol_dis"] = ((dataFrame["vol_dis"] / dataFrame["vol_dis"].mean()) * 100)


            dataFrame = dataFrame.round(2)
            data = []
            for index, row in dataFrame.iterrows():
                subdata = []
                subdata.append(row['TIMESTAMP'])
                subdata.append(row['CONTRACTS'])
                subdata.append(row['CLOSE'])
                subdata.append(row['vol_dis'])
                subdata.append(row['PO_Ratio'])
                subdata.append(row['CHG_IN_OI'])
                subdata.append(row['Cumlative COI'])
                data.append(subdata)
            return data
      else:
          data =[]
          data.append([0,0,0,0,0,0,0])

          return  data

    def Process_Cash_data_for_stock(self, stock_symbol,Consolidated_cash__dataframe):
        # MainDataFrame_cash = []
        # for filename in Cash_Files_list:
        #     dataFrame_cash = pd.read_csv(filename)
        #
        #     MainDataFrame_cash.append((dataFrame_cash))
        # dataFrame_cash = pd.concat(MainDataFrame_cash)
        dataFrame_cash = Consolidated_cash__dataframe.copy(deep=True)


        dataFrame_cash = dataFrame_cash[dataFrame_cash['SYMBOL'] == stock_symbol.upper()]


        dataFrame_cash[' DATE1'] = pd.to_datetime(dataFrame_cash[' DATE1'])
        dataFrame_cash = dataFrame_cash.sort_values(by=' DATE1')

        dataFrame_cash[' DELIV_PER'] = dataFrame_cash[' DELIV_PER'].astype(float)
        dataFrame_cash[' DELIV_QTY'] = dataFrame_cash[' DELIV_QTY'].astype(float)

        dataFrame_cash['CLO']=dataFrame_cash[' CLOSE_PRICE'] - dataFrame_cash[' OPEN_PRICE']
        dataFrame_cash['HiLo'] = dataFrame_cash[' HIGH_PRICE'] - dataFrame_cash[' LOW_PRICE']
        dataFrame_cash['Wick'] = (abs(abs(dataFrame_cash['HiLo']) - abs(dataFrame_cash['CLO'])))
        dataFrame_cash['ClOP_per'] = (100 - (((dataFrame_cash[' CLOSE_PRICE'] - dataFrame_cash['CLO']) * 100) / dataFrame_cash[' CLOSE_PRICE']))

        dataFrame_cash['Wick_Percentage'] = (100 - (((dataFrame_cash[' CLOSE_PRICE'] - dataFrame_cash['Wick']) * 100) / dataFrame_cash[' CLOSE_PRICE']))
        dataFrame_cash['HiLo_Percentage'] = ((dataFrame_cash[' HIGH_PRICE'] - dataFrame_cash[' LOW_PRICE']) * 100) / dataFrame_cash[' HIGH_PRICE']
        dataFrame_cash['vol_dis'] = dataFrame_cash[' TTL_TRD_QNTY'] / dataFrame_cash['HiLo_Percentage']
        dataFrame_cash['Alert'] = ""

        dataFrame_cash.loc[(dataFrame_cash['ClOP_per'] < dataFrame_cash['Wick_Percentage']), ['Alert']] = "HIGH"
        dataFrame_cash['vol_dis_old'] = dataFrame_cash['vol_dis'].shift(1, fill_value=0, axis=0)
        dataFrame_cash['Per_vol_Updown'] = ((dataFrame_cash['vol_dis'] - dataFrame_cash['vol_dis_old']) * 100) / dataFrame_cash['vol_dis']
        dataFrame_cash['Factor'] = (abs(abs(dataFrame_cash['Wick_Percentage']) / abs(dataFrame_cash['ClOP_per'])))
        dataFrame_cash["Factor"] = ((dataFrame_cash["Factor"] / dataFrame_cash["Factor"].mean()) * 100)

        dataFrame_cash['delivery_Factor'] = dataFrame_cash[' DELIV_QTY'] / dataFrame_cash['HiLo']
        dataFrame_cash['delivery_Factor_old'] = dataFrame_cash['delivery_Factor'].shift(1, fill_value=0, axis=0)
        dataFrame_cash['delivery_density'] = ((dataFrame_cash['delivery_Factor'] - dataFrame_cash['delivery_Factor_old']) * 100) / dataFrame_cash['delivery_Factor']
        dataFrame_cash["delivery_Factor"] = ((dataFrame_cash["delivery_Factor"]/dataFrame_cash["delivery_Factor"].mean()) * 100)

        # dataFrame_cash = dataFrame_cash.round(2)



        data = []
        for index, row in dataFrame_cash.iterrows():
            subdata = []
            subdata.append(row[' DATE1'])
            subdata.append(row['SYMBOL'])
            subdata.append(row[' SERIES'])
            subdata.append(row[' OPEN_PRICE'])
            subdata.append(row[' HIGH_PRICE'])
            subdata.append(row[' LOW_PRICE'])
            subdata.append(row[' CLOSE_PRICE'])
            subdata.append(row[' TTL_TRD_QNTY'])
            subdata.append(row[' NO_OF_TRADES'])
            subdata.append(row[' DELIV_QTY'])
            subdata.append(row[' DELIV_PER'])

            subdata.append(row['HiLo'])
            subdata.append(row['Wick'])
            subdata.append(row['ClOP_per'])
            subdata.append(row['Wick_Percentage'])
            subdata.append(row['HiLo_Percentage'])

            subdata.append(row['vol_dis'])
            subdata.append(row['Factor'])
            subdata.append(row['Per_vol_Updown'])

            subdata.append(row['delivery_Factor'])
            subdata.append(row['delivery_density'])
            data.append(subdata)
        return data

    def Process_Option_data_for_stock(self, stock_symbol, FO_Files_list, expiry_Date_For_Current_Month):
        if stock_symbol in self.Get_the_List_Of_Stocks():
            MainDataFrame = []
            for filename in FO_Files_list:
                dataFrame = pd.read_csv(filename)
                dataFrame_Consolidated_COI = dataFrame[(dataFrame['SYMBOL'] == stock_symbol.upper()) & ((dataFrame['INSTRUMENT'] == 'OPTSTK'))]

                MainDataFrame.append((dataFrame))
            dataFrame = pd.concat(MainDataFrame)
            dataFrame = dataFrame[((dataFrame['EXPIRY_DT'] == expiry_Date_For_Current_Month)) & (dataFrame['INSTRUMENT'] == 'OPTSTK')]
            dataFrame = dataFrame[dataFrame['SYMBOL'] == stock_symbol.upper()]


            data = []
            for index, row in dataFrame.iterrows():
                subdata = []
                subdata.append(row['TIMESTAMP'])
                subdata.append(row['SYMBOL'])
                subdata.append(row['EXPIRY_DT'])
                subdata.append(row['STRIKE_PR'])
                subdata.append(row['OPTION_TYP'])
                subdata.append(row['OPEN'])
                subdata.append(row['HIGH'])
                subdata.append(row['LOW'])
                subdata.append(row['CLOSE'])
                subdata.append(row['CONTRACTS'])
                subdata.append(row['VAL_INLAKH'])
                subdata.append(row['OPEN_INT'])
                subdata.append(row['CHG_IN_OI'])
                data.append(subdata)
            return data
        else:
            data = []
            data.append([0, 0, 0, 0, 0, 0, 0,0,0,0,0,0,0])

            return data

    def Convert_List_To_Dataframe(self,stock_data_list):


        # list_of_list_appended_with_StockName = []
        # for item in stock_data_list:
        #     item.append(stock_name)
        #     list_of_list_appended_with_StockName.append(item)
        #     item = []
        sub_dataFrame = DataFrame(stock_data_list,columns=["SYMBOL", "EXPIRY_DT", "STRIKE_PR", "PO_Ratio","Alert","CHG_IN_OI","Cumlative COI","CONTRACTS","CLOSE", "vol_dis","COI_Percentage","Per_vol_Updown","TIMESTAMP"])
        return sub_dataFrame

    def Convert_List_To_Dataframe_cash(self, stock_data_list):

        # list_of_list_appended_with_StockName = []
        # for item in stock_data_list:
        #     item.append(stock_name)
        #     list_of_list_appended_with_StockName.append(item)
        #     item = []
        sub_dataFrame = DataFrame(stock_data_list,
                                  columns=["SYMBOL", " DATE1", " SERIES", " OPEN_PRICE", " HIGH_PRICE", " LOW_PRICE",
                                           " CLOSE_PRICE", " TTL_TRD_QNTY", " NO_OF_TRADES", " DELIV_QTY", " DELIV_PER",
                                           "HiLo", "Wick", "ClOP_per", "Wick_Percentage", "HiLo_Percentage", "vol_dis",
                                           "Factor", "Per_vol_Updown", "delivery_Factor", "delivery_density"])
        return sub_dataFrame

    def Process_Future_data_for_All_Stocks_And_Make_DataFrame(self,stock_symbol,FO_Files_list,expiry_Date_For_Current_Month):
        MainDataFrame = []
        for filename in FO_Files_list:
            dataFrame = pd.read_csv(filename)
            dataFrame_Consolidated_COI = dataFrame[(dataFrame['SYMBOL'] == stock_symbol.upper()) & ((dataFrame['INSTRUMENT'] == 'FUTSTK'))]
            dataFrame["Cumlative COI"] = dataFrame_Consolidated_COI['CHG_IN_OI'].sum()
            MainDataFrame.append((dataFrame))
        dataFrame = pd.concat(MainDataFrame)

        dataFrame = dataFrame[(dataFrame['EXPIRY_DT'] == expiry_Date_For_Current_Month) & (dataFrame['INSTRUMENT'] == 'FUTSTK')]
        dataFrame = dataFrame[dataFrame['SYMBOL'] == stock_symbol.upper()]
        dataFrame['PO_Ratio'] = dataFrame['CHG_IN_OI']/dataFrame['CONTRACTS']
        dataFrame['ClOP'] = dataFrame['CLOSE']-dataFrame['OPEN']
        dataFrame['HiLo'] = dataFrame['HIGH'] - dataFrame['LOW']
        dataFrame['Wick'] = (abs(abs(dataFrame['HiLo']) - abs(dataFrame['ClOP'])))
        dataFrame['ClOP_per'] = (100 - (((dataFrame['CLOSE'] - dataFrame['ClOP']) * 100) / dataFrame['CLOSE']))
        dataFrame['Wick_Per_On_Spot'] = (100 - (((dataFrame['CLOSE'] - dataFrame['Wick'])*100)/dataFrame['CLOSE']))
        dataFrame['HiLo_Percentage'] = ((dataFrame['HIGH']-dataFrame['LOW'])*100)/dataFrame['HIGH']
        dataFrame['vol_dis'] = dataFrame['CONTRACTS']/dataFrame['HiLo_Percentage']
        dataFrame['Alert'] = ""
        dataFrame.loc[(dataFrame['ClOP_per'] < dataFrame['Wick_Per_On_Spot']), ['Alert']] = "HIGH"

        dataFrame['vol_dis_old'] = dataFrame['vol_dis'].shift(1, fill_value=0, axis=0)
        dataFrame['Per_vol_Updown'] = ((dataFrame['vol_dis'] - dataFrame['vol_dis_old'])*100)/dataFrame['vol_dis']


        dataFrame['x_factor'] = (abs(abs(dataFrame['Wick_Per_On_Spot'])/abs(dataFrame['ClOP_per'])))
        dataFrame['COI_Percentage'] = (dataFrame['CHG_IN_OI']/dataFrame['OPEN_INT'])*100
        dataFrame["vol_dis"] = ((dataFrame["vol_dis"] / dataFrame["vol_dis"].mean()) * 100)


        dataFrame = dataFrame.round(2)

        data = []
        for index, row in dataFrame.iterrows():
            subdata = []
            subdata.append(row['SYMBOL'])
            subdata.append(row['EXPIRY_DT'])
            subdata.append(row['STRIKE_PR'])

            subdata.append(row['PO_Ratio'])
            subdata.append(row['Alert'])
            subdata.append(row['CHG_IN_OI'])
            subdata.append(row['Cumlative COI'])

            subdata.append(row['CONTRACTS'])
            subdata.append(row['CLOSE'])
            subdata.append(row['vol_dis'])
            subdata.append(row['COI_Percentage'])
            subdata.append(row['Per_vol_Updown'])
            subdata.append(row['TIMESTAMP'])
            data.append(subdata)
        return data

    def Get_Today_Date(self):
        today = date.today()
        x = datetime.datetime(today.year, today.month, today.day)
        Today_Date = x.strftime("%d-%b-%Y").upper()
        return Today_Date

    def Get_Month_From_FileName(self,fileName):
        fileName = "D:\FObhavCopy_Data\fo04Jul32020bhav.csv"
        fileName = fileName.upper()
        pattern_First = re.compile(r'\d{2}[A-Z]{3}\d{4}')
        Extracted_Month_Along_withDate_And_Year = pattern_First.findall(fileName)
        pattern_Second = re.compile(r'[A-Z]{3}')
        month = pattern_Second.findall(Extracted_Month_Along_withDate_And_Year[0])[0]
        return month


    def Future_and_Cash_Data(self,FO_Files_list,Cash_Files_List):

        today = date.today()
        # x = datetime.datetime(today.year, today.month-1, today.day)
        expiry_Date_For_Current_Month = self.Find_Expiry_Date_For_Current_Month(today.year, today.month)
        expiry_Date_For_Current_Month = expiry_Date_For_Current_Month.replace(expiry_Date_For_Current_Month[3:6],expiry_Date_For_Current_Month[3:6].capitalize())

        expiry_Date_For_Previous_Month = self.Find_Expiry_Date_For_Current_Month(today.year, today.month-1)
        expiry_Date_For_Previous_Month = expiry_Date_For_Previous_Month.replace(expiry_Date_For_Current_Month[3:6],expiry_Date_For_Current_Month[3:6].capitalize())

        MainDataFrame = []
        Parent_dataframe = []
        for  filename in FO_Files_list:
             dataFrame = pd.read_csv(filename)
             MainDataFrame.append((dataFrame))
        dataFrame = pd.concat(MainDataFrame)
        #Steps to reduce memory Usage of Future consolidated DataFrame
        Consolidated_future__dataframe = dataFrame.copy(deep=True)
        Consolidated_future__dataframe['CONTRACTS'] = Consolidated_future__dataframe['CONTRACTS'].astype("int16")
        Consolidated_future__dataframe['OPEN_INT'] = Consolidated_future__dataframe['OPEN_INT'].astype("int32")
        Consolidated_future__dataframe['CHG_IN_OI'] = Consolidated_future__dataframe['CHG_IN_OI'].astype("int32")
        Consolidated_future__dataframe['OPEN'] = Consolidated_future__dataframe['OPEN'].astype("float16")
        Consolidated_future__dataframe['HIGH'] = Consolidated_future__dataframe['HIGH'].astype("float16")
        Consolidated_future__dataframe['LOW'] = Consolidated_future__dataframe['LOW'].astype("float16")
        Consolidated_future__dataframe['CLOSE'] = Consolidated_future__dataframe['CLOSE'].astype("float16")

        Consolidated_future__dataframe = pd.DataFrame(Consolidated_future__dataframe)
        Consolidated_future__dataframe.drop(['STRIKE_PR','SETTLE_PR','VAL_INLAKH'],axis=1,inplace=True)



        MainDataFrame_cash = []
        for filename in Cash_Files_List:
            dataFrame_cash = pd.read_csv(filename)
            MainDataFrame_cash.append((dataFrame_cash))
        dataFrame_cash  = pd.concat(MainDataFrame_cash)
        Consolidated_cash__dataframe = dataFrame_cash.copy(deep=True)

        # Steps to reduce memory Usage of Cash consolidated DataFrame
        Consolidated_cash__dataframe[' TTL_TRD_QNTY'] = Consolidated_cash__dataframe[' TTL_TRD_QNTY'].astype("int32")
        Consolidated_cash__dataframe[' NO_OF_TRADES'] = Consolidated_cash__dataframe[' NO_OF_TRADES'].astype("int32")
        Consolidated_cash__dataframe[' PREV_CLOSE'] = Consolidated_cash__dataframe[' PREV_CLOSE'].astype("float16")
        Consolidated_cash__dataframe[' OPEN_PRICE'] = Consolidated_cash__dataframe[' OPEN_PRICE'].astype("float16")
        Consolidated_cash__dataframe[' HIGH_PRICE'] = Consolidated_cash__dataframe[' HIGH_PRICE'].astype("float16")
        Consolidated_cash__dataframe[' LOW_PRICE'] = Consolidated_cash__dataframe[' LOW_PRICE'].astype("float16")

        Consolidated_cash__dataframe = pd.DataFrame(Consolidated_cash__dataframe)
        Consolidated_cash__dataframe.drop([' TURNOVER_LACS', ' AVG_PRICE'], axis=1, inplace=True)
        Consolidated_cash__dataframe = Consolidated_cash__dataframe[(Consolidated_cash__dataframe[' SERIES'] == " EQ")]





        dataFrame = dataFrame[((dataFrame['EXPIRY_DT'] == expiry_Date_For_Current_Month) | (dataFrame['EXPIRY_DT'] == expiry_Date_For_Previous_Month) ) & (dataFrame['INSTRUMENT'] == 'FUTSTK')  ]
        dataFrame = dataFrame[['SYMBOL','OPEN','HIGH','LOW','CLOSE','TIMESTAMP']]
        headings_future_Table = ['TIMESTAMP', 'CONTRACTS', 'CLOSE', 'vol_dis %', 'PO_Ratio', 'CHG_IN_OI','Cumlative COI']
        headings_Cash_Table = ['TIMESTAMP', 'vol_dis %', 'CLOSE_PRICE', 'Factor', 'delivery_Factor', 'delivery_density', 'DELIV_QTY','NO_OF_TRADES']
        headings_Option_Table = ['TIMESTAMP', 'SYMBOL', 'EXPIRY_DT', 'STRIKE_PR', 'OPTION_TYP', 'OPEN','HIGH', 'LOW','CLOSE','CONTRACTS', 'VAL_INLAKH','OPEN_INT', 'CHG_IN_OI']
        headings_Rollover_Table = ['RollOver']


        data = []
        roll_over_data = []
        for index,row in dataFrame.iterrows():
            subdata = []
            roll_over_subdata = []
            subdata.append(row['SYMBOL'])
            subdata.append(row['OPEN'])
            subdata.append(row['HIGH'])
            subdata.append(row['LOW'])
            subdata.append(row['CLOSE'])
            subdata.append(row['TIMESTAMP'])
            subdata.append(row['HIGH'])
            subdata.append(row['LOW'])
            subdata.append(row['CLOSE'])
            roll_over_subdata.append('1')


            roll_over_data.append(roll_over_subdata)
            data.append(subdata)

        raw_option_data = [[0,0,0,0,0,0,0,0,0,0,0,0,0]]

        main_list_of_stocks = self.Get_the_List_Of_Stocks()
        list_splits = numpy.array_split(main_list_of_stocks, 7)
        list_of_stocks_part_1 = list_splits[0]
        list_of_stocks_part_2 = list_splits[1]
        list_of_stocks_part_3 = list_splits[2]
        list_of_stocks_part_4 = list_splits[3]
        list_of_stocks_part_5 = list_splits[4]
        list_of_stocks_part_6 = list_splits[5]
        list_of_stocks_part_7 = list_splits[6]


        Table_Panel = [
            [gui.Text("StockName : ", font=('MS Sans Serif', 10, 'bold'), text_color='Blue', background_color='white'),
             gui.DropDown(values=self.Get_the_List_Of_MidCap_Stocks(),auto_size_text=True,enable_events=True,size=(20,30),),
             gui.Button("Process Stocks Data", font=('MS Sans Serif', 10, 'bold'), button_color=('Blue', 'white'), ),

             gui.ProgressBar(len(self.Get_the_List_Of_cash_Stocks()), orientation='h', size=(20, 20), key='progbar'),


             gui.Button("Watchlist Summary", font=('MS Sans Serif', 10, 'bold'), button_color=('white', 'blue')),
             gui.Button("Cash Chart", font=('MS Sans Serif', 10, 'bold'), button_color=('white', 'blue')),
             gui.Button("Option Chart", font=('MS Sans Serif', 10, 'bold'), button_color=('white', 'blue')),

             gui.Frame(
                 layout=[
                           [gui.Text("1 :LONG  3:SHORT 5:REVERSE ", font=('MS Sans Serif', 10, 'bold'), text_color='Blue',background_color='white')],
                           [gui.Text("2 :LPB   4:SPB   6:NO IDEA ", font=('MS Sans Serif', 10, 'bold'), text_color='Blue',background_color='white')]

                        ], title="ROLL_OVER_DATA_LEGEND",title_color="White", relief=gui.RELIEF_RAISED
                     ),
             gui.Text("MonthlyExpiry : ", font=('MS Sans Serif', 10, 'bold'), text_color='Blue', background_color='white'),
             gui.DropDown(values=self.Get_the_List_Of_MidCap_Stocks(), auto_size_text=True, enable_events=True,
                          size=(20, 30), ),
             gui.Text("WeeklyExpiry : ", font=('MS Sans Serif', 10, 'bold'), text_color='Blue',
                      background_color='white'),
             gui.DropDown(values=self.Get_the_List_Of_MidCap_Stocks(), auto_size_text=True, enable_events=True,
                          size=(20, 30), ),


             ],
            [gui.HorizontalSeparator()],
            [gui.Button(stocks_part_1, font=('MS Sans Serif', 10, 'bold'), button_color=('red', 'grey')) for stocks_part_1 in list_of_stocks_part_1 ],
            [gui.Button(stocks_part_2, font=('MS Sans Serif', 10, 'bold'), button_color=('red', 'grey')) for stocks_part_2 in list_of_stocks_part_2],
            [gui.Button(stocks_part_3, font=('MS Sans Serif', 10, 'bold'), button_color=('red', 'grey')) for stocks_part_3 in list_of_stocks_part_3],
            [gui.Button(stocks_part_4, font=('MS Sans Serif', 10, 'bold'), button_color=('red', 'grey')) for stocks_part_4 in list_of_stocks_part_4],
            [gui.Button(stocks_part_5, font=('MS Sans Serif', 10, 'bold'), button_color=('red', 'grey')) for stocks_part_5 in list_of_stocks_part_5],
            [gui.Button(stocks_part_6, font=('MS Sans Serif', 10, 'bold'), button_color=('red', 'grey')) for stocks_part_6 in list_of_stocks_part_6],
            [gui.Button(stocks_part_7, font=('MS Sans Serif', 10, 'bold'), button_color=('red', 'grey')) for stocks_part_7 in list_of_stocks_part_7],
            [gui.HorizontalSeparator()],




            [gui.Table(values=data,
                       headings=headings_future_Table,

                       auto_size_columns=True,
                       justification='right',
                       key='-TABLE_FO-',
                       alternating_row_color='blue',
                       num_rows=min(len(data), 72), vertical_scroll_only=False),

             gui.Table(values=roll_over_data,
                       headings=headings_Rollover_Table,

                       auto_size_columns=True,
                       justification='right',
                       key='-TABLE_ROLL_OVER_DATA-',
                       alternating_row_color='brown',
                       num_rows=min(len(data), 72), vertical_scroll_only=False),

             gui.Table(values=data,
                       headings=headings_Cash_Table,
                       auto_size_columns=True,
                       justification='right',
                       key='-TABLE_CASH-',
                       alternating_row_color='red',
                       num_rows=min(len(data), 72), vertical_scroll_only=False),

                gui.Table(values=raw_option_data,
                       headings=headings_Option_Table,
                       auto_size_columns=True,
                       justification='right',
                       key='-TABLE_OPTION-',
                       alternating_row_color='brown',
                       num_rows=min(len(data), 72), vertical_scroll_only=False)

             ]
        ]
        window_Tabel_FO_Data = gui.Window('Table', Table_Panel, grab_anywhere=False, resizable=True,size=[500,500])

        while True:
            event_Tabel_FO_Data, values = window_Tabel_FO_Data.read()
            if event_Tabel_FO_Data == 0:
                    stock_specific_values_FO = self.Process_Future_data_for_stock(values[0],Consolidated_future__dataframe,expiry_Date_For_Current_Month,expiry_Date_For_Previous_Month)
                    stock_specific_values_CASH = self.Process_Cash_data_for_stock(values[0],Consolidated_cash__dataframe)
                    stock_specific_values_OPTION = self.Process_Option_data_for_stock(values[0], FO_Files_list,expiry_Date_For_Current_Month)


                    window_Tabel_FO_Data['-TABLE_FO-'].update(values=stock_specific_values_FO)
                    window_Tabel_FO_Data['-TABLE_CASH-'].update(values=stock_specific_values_CASH)
                    window_Tabel_FO_Data['-TABLE_OPTION-'].update(values=stock_specific_values_OPTION)

            if event_Tabel_FO_Data == "Watchlist Summary":
                    Object_NextDay_watchlist = class_Next_Day_watchlist_summary()
                    Object_NextDay_watchlist.GUI_formation()

            if event_Tabel_FO_Data == "Cash Chart":
                self.Future_chart(values[0])

            for item in self.Get_the_List_Of_Stocks():
                if event_Tabel_FO_Data == item:
                    start_time = time.time()
                    stock_specific_values_FO = self.Process_Future_data_for_stock(event_Tabel_FO_Data,Consolidated_future__dataframe,expiry_Date_For_Current_Month,expiry_Date_For_Previous_Month)
                    stock_specific_values_CASH = self.Process_Cash_data_for_stock(event_Tabel_FO_Data,Consolidated_cash__dataframe)
                    stock_specific_values_OPTION = self.Process_Option_data_for_stock(event_Tabel_FO_Data, FO_Files_list,expiry_Date_For_Current_Month)
                    window_Tabel_FO_Data['-TABLE_FO-'].update(values=stock_specific_values_FO)
                    window_Tabel_FO_Data['-TABLE_CASH-'].update(values=stock_specific_values_CASH)
                    window_Tabel_FO_Data['-TABLE_OPTION-'].update(values=stock_specific_values_OPTION)
                    end_time= time.time()
                    print(f"Total time taken : {end_time-start_time }")



            if event_Tabel_FO_Data == "Option Chart":
                o = Option_Data()
                o.Option_GUI_Formation()

            if event_Tabel_FO_Data == "Process Stocks Data":
                gui.popup_auto_close("Data Processing Starts . Please wait for the process to complete")
                list_of_Stocks = self.Get_the_List_Of_Stocks()
                list_of_cash_Stocks = self.Get_the_List_Of_cash_Stocks()

                Cumlative_DataFrame = []
                Cumlative_DataFrame_Cash = []
                i = 0
                for stock_name in list_of_cash_Stocks[0:len(list_of_cash_Stocks)]:
                    i = i + 1
                    window_Tabel_FO_Data['progbar'].update_bar(i)
                    # stock_specific_values_FO = self.Process_Future_data_for_All_Stocks_And_Make_DataFrame(stock_name, FO_Files_list,expiry_Date_For_Current_Month)
                    stock_specific_values_CASH = self.Process_Cash_data_for_stock (stock_name,Consolidated_cash__dataframe)
                    # dataFrame_new = self.Convert_List_To_Dataframe(stock_specific_values_FO)
                    dataFrame_new_Cash = self.Convert_List_To_Dataframe_cash(stock_specific_values_CASH)
                    # Cumlative_DataFrame.append(dataFrame_new)
                    Cumlative_DataFrame_Cash.append(dataFrame_new_Cash)


                # data_frames_of_all_Stocks_Post_Data_Processing = pd.concat(Cumlative_DataFrame)
                # data_frames_of_all_Stocks_Post_Data_Processing.to_csv("Koko.csv")

                data_frames_of_all_Stocks_Post_Data_cash_Processing = pd.concat(Cumlative_DataFrame_Cash)

                data_frames_of_all_Stocks_Post_Data_cash_Processing = data_frames_of_all_Stocks_Post_Data_cash_Processing[["SYMBOL"," DATE1"," CLOSE_PRICE","HiLo_Percentage","delivery_Factor","vol_dis"]]

                data_frames_of_all_Stocks_Post_Data_cash_Processing.to_csv("cash.csv")



            if event_Tabel_FO_Data == "Filter":


                if (values['COI_Percentage_enabled'] & (not values['Percentage_volume_enabled'])):

                    # data_frames_of_all_Stocks_Post_Data_Processing = pd.read_csv("Koko.csv")
                    #print(data_frames_of_all_Stocks_Post_Data_Processing.info())
                    filtered_Data_frame = data_frames_of_all_Stocks_Post_Data_Processing[
                        (data_frames_of_all_Stocks_Post_Data_Processing['TIMESTAMP'] == self.Get_Today_Date()) & (
                                    data_frames_of_all_Stocks_Post_Data_Processing['COI_Percentage'] > float(values['_COI_INPUT_Value_']))]
                    filtered_Data_frame.to_csv("FilteredData.csv")

                elif (values['Percentage_volume_enabled'] & (not values['COI_Percentage_enabled'])):

                    data_frames_of_all_Stocks_Post_Data_Processing = pd.read_csv("Koko.csv")

                    filtered_Data_frame = data_frames_of_all_Stocks_Post_Data_Processing[
                        (data_frames_of_all_Stocks_Post_Data_Processing['TIMESTAMP'] == self.Get_Today_Date()) & (
                                data_frames_of_all_Stocks_Post_Data_Processing['Per_vol_Updown'] > float(values[
                            '_Percentage_SLIDER_Value_']))]
                    filtered_Data_frame.to_csv("FilteredData.csv")

                elif (values['Percentage_volume_enabled'] & (values['COI_Percentage_enabled'])):

                    data_frames_of_all_Stocks_Post_Data_Processing = pd.read_csv("Koko.csv")

                    filtered_Data_frame = data_frames_of_all_Stocks_Post_Data_Processing[(data_frames_of_all_Stocks_Post_Data_Processing['TIMESTAMP'] == self.Get_Today_Date()) & (data_frames_of_all_Stocks_Post_Data_Processing['Per_vol_Updown'] > float(values['_Percentage_SLIDER_Value_'])) & (data_frames_of_all_Stocks_Post_Data_Processing['COI_Percentage'] > float(values[
                                '_COI_INPUT_Value_']))]
                    print("uepp0 ;",self.Get_Today_Date())
                    filtered_Data_frame.to_csv("FilteredData.csv")

            elif (event_Tabel_FO_Data == gui.WIN_CLOSED):
                    break
        window_Tabel_FO_Data.close()









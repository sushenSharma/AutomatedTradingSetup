import PySimpleGUI as gui
from datetime import  date
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pyautogui
import pandas as pd

from Folder_operations_module import Folder_Operation

coordinates = pyautogui.size()
width_of_screen = coordinates[0]
height_of_screen = coordinates[1]
import datetime, calendar
from pandas import  DataFrame
import re


class Option_Data:
    def Get_the_List_Of_Stocks(self):
        df_stock_list = pd.read_csv(Folder_Operation.stock_list_path)
        df_stock_list = df_stock_list[(df_stock_list['INSTRUMENT'] == 'FUTSTK')]
        total_list = list(df_stock_list['SYMBOL'])
        stock_list = []
        for i in total_list:
            if i not in stock_list:
                stock_list.append(i)
            stock_list.sort()
        return stock_list


    def Process_Option_data_for_stock(self, stock_symbol, FO_Files_list, expiry_Date_For_Current_Month):
        if stock_symbol in self.Get_the_List_Of_Stocks():
            print("available")
            MainDataFrame = []
            for filename in FO_Files_list:
                dataFrame = pd.read_csv(filename)
                dataFrame_Consolidated_COI = dataFrame[
                    (dataFrame['SYMBOL'] == stock_symbol.upper()) & ((dataFrame['INSTRUMENT'] == 'OPTSTK'))]

                MainDataFrame.append((dataFrame))
            dataFrame = pd.concat(MainDataFrame)
            dataFrame = dataFrame[
                ((dataFrame['EXPIRY_DT'] == expiry_Date_For_Current_Month)) & (dataFrame['INSTRUMENT'] == 'OPTSTK')]
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
            data.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

            return data




    def Option_GUI_Formation(self):
        headings_Option_Table = ['TIMESTAMP', 'SYMBOL', 'EXPIRY_DT', 'STRIKE_PR', 'OPTION_TYP', 'OPEN', 'HIGH', 'LOW',
                                 'CLOSE', 'CONTRACTS', 'VAL_INLAKH', 'OPEN_INT', 'CHG_IN_OI']
        raw_option_data = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        layout12 = [
                        [gui.Text("StockName : ", font=('MS Sans Serif', 7, 'bold'), text_color='red', background_color='white'),
                        gui.DropDown(values=self.Get_the_List_Of_Stocks(), auto_size_text=True, enable_events=True,size=(40, 30)),
                        gui.Button("GetSheet", font=('MS Sans Serif', 10, 'bold'), button_color=('red', 'white')),
                        ],

                               [gui.Table(values=raw_option_data,
                                    headings=headings_Option_Table,
                                    auto_size_columns=True,
                                    justification='right',
                                    key='-TABLE_FO-',
                                    alternating_row_color='green',
                                    num_rows=min(len(raw_option_data), 20), vertical_scroll_only=False),
                                ],

                    ]
        window_great = gui.Window('Bramahastra', layout12, size=(width_of_screen,height_of_screen))

        while True:
            event, values = window_great.read()
            print("event", event)
            print("values", values)
            if (event == gui.WIN_CLOSED) or (event == "Exit"):
                break
            elif event=="GetSheet":
                list_of_FO_files_Downloaded = self.Folder_Operation.Downloaded_FO_Bhav_CopyFiles()
                print(list_of_FO_files_Downloaded)
                #stock_specific_values_OPTION = self.Process_Option_data_for_stock(values[0], FO_Files_list,expiry_Date_For_Current_Month)


                #window_great['-TABLE_OPTION-'].update(values=stock_specific_values_OPTION)

        window_great.close()


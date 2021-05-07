import PySimpleGUI as gui
from nsetools import Nse
import plotly.graph_objects as go
import pyautogui
import pandas as pd

cash_file_path = "cash.csv"
sector_file = "Stock_list/ind_nifty500list.csv"


coordinates = pyautogui.size()
width_of_screen = coordinates[0]
height_of_screen = coordinates[1]





class class_Next_Day_watchlist_summary:

    def Read_and_Summarise_watchlist(self,date_selected):
        watchlist_data = pd.read_csv("Actual_result_daily.csv")
        watchlist_data["Date_Selected"] = date_selected
        return  watchlist_data.values.tolist()


    def get_Graph_resultant_array(stock, list_of_stocks_shortlisted):
        total_graphs = 3
        resultant = [False] * (len(list_of_stocks_shortlisted) * total_graphs)
        req_index = -1
        n = total_graphs

        for index, value in enumerate(list_of_stocks_shortlisted):
            if stock == value:
                req_index = index * n
                break

        while n:
            resultant[req_index] = True
            req_index += 1
            n -= 1

        return resultant

    def Summarize_Cash_data(self,Cash_file_path,date_selected):
            nse = Nse()
            fig = go.Figure()
            Parent_dataFrame_To_Store_Each_Stock_DataFrame = []
            Parent_dataFrame_To_Store_Each_Stock_Symbol_and_DeliveryFactor = []
            list_of_Dictionary_object_to_passTo_Update_figure = []
            column_names = ["StockName", "Sector", "Mean_value_hilo", "Compression Number", "Return_Today","Nifty_return", "Repeat Days"]
            FinalDataFrame = pd.DataFrame(columns=column_names)


            data = pd.read_csv(Cash_file_path)
            sector = pd.read_csv(sector_file)

            data.rename(columns={'SYMBOL': 'Date'}, inplace=True)
            data.rename(columns={' DATE1': 'Symbol'}, inplace=True)
            Shortlisted_DataFrame_With_Corresponding_Sectors = pd.merge(data, sector, on="Symbol")
            print(Shortlisted_DataFrame_With_Corresponding_Sectors["Date"])
            temp_result = Shortlisted_DataFrame_With_Corresponding_Sectors[(Shortlisted_DataFrame_With_Corresponding_Sectors["Date"] == date_selected) & (Shortlisted_DataFrame_With_Corresponding_Sectors["delivery_Factor"] > 100)]
            temp_result = temp_result[["Date", "Symbol", "delivery_Factor", "Industry"]]




            list_of_stocks_shortlisted = list(temp_result["Symbol"])

            for stock_name in list_of_stocks_shortlisted:
                Stock_DataFrame = Shortlisted_DataFrame_With_Corresponding_Sectors[
                    Shortlisted_DataFrame_With_Corresponding_Sectors["Symbol"] == stock_name]
                Parent_dataFrame_To_Store_Each_Stock_DataFrame.append(Stock_DataFrame)

            for dataFrame in Parent_dataFrame_To_Store_Each_Stock_DataFrame:
                Parent_dataFrame_To_Store_Each_Stock_Symbol_and_DeliveryFactor.append(
                    dataFrame[["Date", "Symbol", " CLOSE_PRICE", "vol_dis", "delivery_Factor"]])

            for each_stock in Parent_dataFrame_To_Store_Each_Stock_Symbol_and_DeliveryFactor:

                if (each_stock[" CLOSE_PRICE"].mean() < 100):
                    Scaled_Down_ratio_of_vol_dis = list(map(lambda x: x / 1000000, each_stock["vol_dis"].to_list()))
                elif ((each_stock[" CLOSE_PRICE"].mean() > 100) and (each_stock[" CLOSE_PRICE"].mean() <= 1000)):
                    Scaled_Down_ratio_of_vol_dis = list(map(lambda x: x / 100000, each_stock["vol_dis"].to_list()))
                elif ((each_stock[" CLOSE_PRICE"].mean() > 1000) and (each_stock[" CLOSE_PRICE"].mean() <= 100000)):
                    Scaled_Down_ratio_of_vol_dis = list(map(lambda x: x / 10000, each_stock["vol_dis"].to_list()))

                fig.add_trace(go.Bar(
                    x=each_stock["Date"].to_list(),
                    y=Scaled_Down_ratio_of_vol_dis,
                    showlegend=True,
                    name="Vol_Dis"

                ))
                fig.add_trace(go.Bar(
                    x=each_stock["Date"].to_list(),
                    y=each_stock["delivery_Factor"].to_list(),
                    showlegend=True,
                    name="Delivery Factor"
                ))
                fig.add_trace(go.Scatter(
                    x=each_stock["Date"].to_list(),
                    y=each_stock[" CLOSE_PRICE"].to_list(),
                    showlegend=True,
                    line=dict(color="#33CFA5"),
                    name="Closing Price"
                ))

            Graph_visible_pattern_list = []
            for stock in list_of_stocks_shortlisted:
                Graph_visible_pattern_list.append(self.get_Graph_resultant_array(stock))

            for item in zip(list_of_stocks_shortlisted, Graph_visible_pattern_list):
                dict_object = dict(
                    label=item[0],
                    method="update",
                    args=[
                        {"visible": item[1]},
                        {"title": "IntraDay Watchlist",
                         "annotations": []}
                    ]
                )

                list_of_Dictionary_object_to_passTo_Update_figure.append(dict_object)

            fig.update_layout(
                updatemenus=[go.layout.Updatemenu(
                    active=0,
                    buttons=list(
                        list_of_Dictionary_object_to_passTo_Update_figure
                    )
                )
                ])

            # send_email()
            #fig.show()
            counter = 0
            NiftyChange_Percentage = (nse.get_index_quote("NIFTY 50")["pChange"])
            narrowRange_days = 0
            for stock_name in list_of_stocks_shortlisted:
                Stock_DataFrame = Shortlisted_DataFrame_With_Corresponding_Sectors[Shortlisted_DataFrame_With_Corresponding_Sectors["Symbol"] == stock_name]

                Name_of_stock = list(Stock_DataFrame["Symbol"])
                list_Hilow_of_stock = (list(Stock_DataFrame["HiLo_Percentage"]))[::-1]
                list_delivery_factor_of_stock = (list(Stock_DataFrame["delivery_Factor"]))[::-1]
                Mean_Value_of_Hilow = Stock_DataFrame["HiLo_Percentage"].mean()
                Sector_of_stock = list(Stock_DataFrame["Industry"])

                if (list_Hilow_of_stock[0] < Mean_Value_of_Hilow):
                    narrowRange_days = 0
                    for highlow_value in list_Hilow_of_stock:
                        if (highlow_value < Mean_Value_of_Hilow):
                            narrowRange_days = narrowRange_days + 1
                        else:
                            break
                if (list_delivery_factor_of_stock[0] > 90):
                    Repeat_days = 0
                    for del_fac_value in list_delivery_factor_of_stock:
                        if (del_fac_value > 90):
                            Repeat_days = Repeat_days + 1
                        else:
                            break

                row = {'StockName': Name_of_stock[0], 'Sector': Sector_of_stock[0],'Mean_value_hilo': Mean_Value_of_Hilow, 'Compression Number': narrowRange_days,'Return_Today': ((str)((nse.get_quote(Name_of_stock[0]))["pChange"])),'Nifty_return': NiftyChange_Percentage, 'RepeatDays': Repeat_days}
                FinalDataFrame = FinalDataFrame.append(row, ignore_index=True)

            fin_resu = FinalDataFrame.groupby(['Sector', 'StockName'])

            fin_resu = fin_resu[["Return_Today", "Compression Number", "RepeatDays"]]

            print(fin_resu.first())
            fin_resu.first().to_csv("Actual_result_daily.csv")
            Sector_List = FinalDataFrame["Sector"].to_list()
            Sector_List_with_Counter = [[x,Sector_List.count(x)] for x in set(Sector_List)]
            return Sector_List_with_Counter








    def GUI_formation(self):
        gui.theme('TealMono')

        headings_Table_Complete_watchlist = ['SECTOR_NAME','SYMBOL','ReturnToday','COMPRESSION NUMBER','REPEAT DAYS','Date']
        raw_data_Complete_watchlist = [[0, 0, 0, 0,0,0]]

        headings_Sector_counter_Table = ['SECTOR_NAME','Counter']
        raw_data_Sector_counter = [[0, 0]]

        layout12 = [
                        [
                            gui.Text('Select Date', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN),
                            gui.Input(key='-Date_Selected-'),
                        ],
                        [
                            gui.CalendarButton('Pick the Date', target='-Date_Selected-',close_when_date_chosen=True)
                        ],

                        [
                            gui.Button("Get Summary Report", font=('MS Sans Serif', 10, 'bold'), button_color=('red', 'white')),
                        ],

            [gui.Table(values=raw_data_Complete_watchlist,
                       headings=headings_Table_Complete_watchlist,
                       auto_size_columns=False,
                       justification='right',
                       key='-WATCHLIST_SUMMARY-',
                       alternating_row_color="yellow",
                       num_rows=max(len(raw_data_Complete_watchlist), 40)),

             gui.Table(values=raw_data_Sector_counter,
                        headings=headings_Sector_counter_Table,
                        auto_size_columns=False,
                        justification='right',
                        key='-Sector_Counter-',
                        alternating_row_color="brown",
                        num_rows=max(len(raw_data_Sector_counter),40)),
             ],

        ]
        window_great = gui.Window('Bramahastra', layout12, size=(width_of_screen, height_of_screen))

        while True:
            event, values = window_great.read()

            if (event == gui.WIN_CLOSED) or (event == "Exit"):
                break


            elif event=="Get Summary Report":
                if (str(values["-Date_Selected-"]) == ""):
                   gui.popup_ok("Please Select The Date First", background_color="black",text_color="yellow")

                else:
                    full_format_date_selected = str(values["-Date_Selected-"])
                    date_selected = (full_format_date_selected.split(" "))[0]


                    watchlist_summary_report = self.Summarize_Cash_data(cash_file_path,date_selected)
                    raw_data_Complete_watchlist = self.Read_and_Summarise_watchlist(date_selected)

                    window_great['-WATCHLIST_SUMMARY-'].update(values=raw_data_Complete_watchlist)
                    window_great['-Sector_Counter-'].update(values=watchlist_summary_report)

        window_great.close()
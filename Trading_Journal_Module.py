import PySimpleGUI as gui
from nsetools import Nse
import plotly.graph_objects as go
import pyautogui
import sqlite3
import pandas as pd

coordinates = pyautogui.size()
width_of_screen = coordinates[0]
height_of_screen = coordinates[1]


class TradingJournal:
    def DatabaseConnection_String_Setup(self):
        conn = sqlite3.connect('TradingJournal.db')
        return conn

    def DatabaseConnection_cursor_Setup(self, conn):
        connection_cursor = conn.cursor()
        return connection_cursor

    def CreateTableSwingTrade(self, connection_string, connection_cursor):

        connection_cursor.execute("""CREATE TABLE SwingTrade_Ledger
                                              (        Stock_Symbol text,
                                                       Type_of_Trade text,
                                                       Amount text,
                                                       Buy_Price text,
                                                       Stop_Loss text,
                                                       Target text,
                                                       R_multiple text,
                                                       Status text
                                               )
                                 """)
        connection_string.commit()

    def CreateTableIntradayTrade(self, connection_string, connection_cursor):

        connection_cursor.execute("""CREATE TABLE Intraday_Ledger
                                               (       Stock_Symbol text,
                                                       Type_of_Trade text,
                                                       Amount text,
                                                       Buy_Price text,
                                                       Stop_Loss text,
                                                       Target text,
                                                       R_multiple text,
                                                       Status text
                                               )
                                    """)
        connection_string.commit()

    def Check_If_Table_Exists(self, connection_string, Connection_cursor, tableName):
        Connection_cursor.execute(f"""
                                        SELECT name FROM sqlite_master WHERE type='table' AND name='{tableName}';
                                 """)
        result = Connection_cursor.fetchall()
        connection_string.commit()
        return len(result)

    def Insert_Data_In_Table(self, connection_string, Connection_cursor, tableName, list_of_values):
        Connection_cursor.execute(f"""
                                    INSERT INTO {tableName} VALUES (   
                                                                    '{list_of_values[0].capitalize()}','{list_of_values[1].capitalize()}','{list_of_values[2]}',
                                                                    '{list_of_values[3]}','{list_of_values[4]}','{list_of_values[5]}','{list_of_values[6]}','{list_of_values[7]}'
                                                                    )
                                  """)
        connection_string.commit()

    def Show_Data_from_table(selfs, connection_string, Connection_cursor, tableName):
        Connection_cursor.execute(f"""
                                
                                SELECT * FROM {tableName}
                                
                                """)
        result = Connection_cursor.fetchall()
        connection_string.commit()
        return result

    def Gui_Formation(self):
        gui.theme('TealMono')
        connection_string = self.DatabaseConnection_String_Setup()
        connection_cursor = self.DatabaseConnection_cursor_Setup(connection_string)

        if self.Check_If_Table_Exists(connection_string, connection_cursor,
                                      "SwingTrade_Ledger") < 1:  # Checking If table Exist ,by checking return count from method Check_if_table_exist
            self.CreateTableSwingTrade(connection_string, connection_cursor)

        if self.Check_If_Table_Exists(connection_string, connection_cursor,
                                      "Intraday_Ledger") < 1:  # Checking If table Exist ,by checking return count from method Check_if_table_exist
            self.CreateTableIntradayTrade(connection_string, connection_string)

        gui.SetOptions(element_padding=(width_of_screen / 150, height_of_screen / 150))

        result_values = self.Show_Data_from_table(connection_string, connection_cursor, "Intraday_Ledger")
        Intermediate_Process_result_values = list(map(lambda x: [x], result_values))
        Initial_Processed_Result_Values = list(map(lambda x: list(x[0]), Intermediate_Process_result_values))

        Swing_trading_result_values = self.Show_Data_from_table(connection_string, connection_cursor, "SwingTrade_Ledger")
        Swing_trading_Intermediate_Process_result_values = list(map(lambda x: [x], Swing_trading_result_values))
        Swing_Trading_Initial_Processed_Result_Values = list(map(lambda x: list(x[0]), Swing_trading_Intermediate_Process_result_values))

        header_list = ["Stock_Symbol", "Type_of_Trade", "Amount", "Entry_Price", "Stop_Loss", "Exit_Price", "R_Multiple","Status"]
        layout = [
            [
                gui.Frame(
                    layout=[
                        [gui.Text('Stock Symbol', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN),gui.Input(key='-INTRADAY_STOCK_SYMBOL-')],
                        [gui.Text('Type of Trade', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN),
                         gui.Text('Intraday', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN)],
                        [gui.Text('Amount', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN), gui.Input(key='-INTRADAY_AMOUNT-')],
                        [gui.Text('Entry Price', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN),gui.Input(key='-INTRADAY_BUY_PRICE-')],
                        [gui.Text('Stop Loss', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN),gui.Input(key='-INTRADAY_STOP_LOSS-')],
                        [gui.Text('Exit Price', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN), gui.Input(key='-INTRADAY_TARGET-')],
                        [gui.Text('Status', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN), gui.Input(key='-INTRADAY_STATUS-')],
                        [gui.Button('Add Record', enable_events=True), gui.Button('Clear Record')]

                    ], title="INTRADAY LEDGER", title_color="Black", relief=gui.RELIEF_SOLID,
                    background_color="light green", border_width=10
                ),
                gui.Frame(
                    layout=[
                        [gui.Text('Stock Symbol', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN),gui.Input(key='-SWINGTRADE_STOCK_SYMBOL-')],
                        [gui.Text('Type of Trade', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN),
                         gui.Text('Swing Trade', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN)],
                        [gui.Text('Amount', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN), gui.Input(key='-SWINGTRADE_AMOUNT-')],
                        [gui.Text('Entry Price', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN),gui.Input(key='-SWINGTRADE_BUY_PRICE-')],
                        [gui.Text('Stop Loss', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN),gui.Input(key='-SWINGTRADE_STOP_LOSS-')],
                        [gui.Text('Exit Price', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN), gui.Input(key='-SWINGTRADE_TARGET-')],
                        [gui.Text('Status', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN), gui.Input(key='-SWINGTRADE_STATUS-')],
                        [gui.Button('Add Record'), gui.Button('Clear Record')]

                    ], title="SWING TRADE LEDGER", title_color="Black", relief=gui.RELIEF_SOLID,
                    background_color="LIGHT PINK", border_width=10
                ),
            ],
            [gui.Table(values=Initial_Processed_Result_Values,
                       headings=header_list,
                       display_row_numbers=True,
                       auto_size_columns=False,
                       key='-INTRADAY_LEDGER_TABLE-',
                       num_rows=max(55, len(Initial_Processed_Result_Values))),

             gui.Table(values=Swing_Trading_Initial_Processed_Result_Values,
                       headings=header_list,
                       display_row_numbers=True,
                       auto_size_columns=False,
                       key='-SWINGTRADE_LEDGER_TABLE-',
                       num_rows=max(55, len(Initial_Processed_Result_Values)))

             ]
        ]

        window = gui.Window('Bramahastra', layout, size=(width_of_screen, height_of_screen))

        while True:
            event, values = window.read()



            if (event == gui.WIN_CLOSED) or (event == "Exit"):
                break
            elif (event == "Add Record"):  # Intraday Add Record
                if (str(values['-INTRADAY_STOCK_SYMBOL-']) == "") or (str(values['-INTRADAY_AMOUNT-']) == "") or (str(values['-INTRADAY_BUY_PRICE-']) == "") or (str(values['-INTRADAY_STOP_LOSS-']) == "") or (str(values['-INTRADAY_TARGET-']) == "") or (str(values['-INTRADAY_STATUS-']) == ""):
                    gui.popup_ok("Please Fill All the Values", background_color="black",text_color="yellow")

                else:
                    list_of_values = []
                    Intraday_Stock_symbol = values['-INTRADAY_STOCK_SYMBOL-']
                    Type_of_Trade = "Intrady"
                    Amount = values['-INTRADAY_AMOUNT-']
                    Buy_price = (float)(values['-INTRADAY_BUY_PRICE-'])
                    Stop_loss = (float)(values['-INTRADAY_STOP_LOSS-'])
                    Target = float(values['-INTRADAY_TARGET-'])
                    Risk = Buy_price - Stop_loss
                    Reward = Target - Buy_price
                    Status = values['-INTRADAY_STATUS-']
                    R_Multiple = float("{:.2f}".format(Reward / Risk))
                    R_Multiple = str(R_Multiple) + "R"


                    list_of_values.append(Intraday_Stock_symbol)
                    list_of_values.append(Type_of_Trade)
                    list_of_values.append(Amount)
                    list_of_values.append(str(Buy_price))
                    list_of_values.append(str(Stop_loss))
                    list_of_values.append(str(Target))
                    list_of_values.append(R_Multiple)
                    list_of_values.append(Status)




                    self.Insert_Data_In_Table(connection_string, connection_string, "Intraday_Ledger", list_of_values)

                    result_values = self.Show_Data_from_table(connection_string, connection_cursor, "Intraday_Ledger")
                    Intermediate_Process_result_values = list(map(lambda x: [x], result_values))
                    Final_Processed_Result_Values = list(map(lambda x: list(x[0]),  Intermediate_Process_result_values))


                    window.Element('-INTRADAY_LEDGER_TABLE-').update(values= Final_Processed_Result_Values)
                    window['-INTRADAY_STOCK_SYMBOL-'].update('')
                    window['-INTRADAY_AMOUNT-'].update('')
                    window['-INTRADAY_BUY_PRICE-'].update('')
                    window['-INTRADAY_STOP_LOSS-'].update('')
                    window['-INTRADAY_TARGET-'].update('')
                    window['-INTRADAY_STATUS-'].update('')

            elif (event == "Clear Record"):  # Intraday Clear Record
                window['-INTRADAY_STOCK_SYMBOL-'].update('')
                window['-INTRADAY_AMOUNT-'].update('')
                window['-INTRADAY_BUY_PRICE-'].update('')
                window['-INTRADAY_STOP_LOSS-'].update('')
                window['-INTRADAY_TARGET-'].update('')
                window['-INTRADAY_STATUS-'].update('')

            elif (event == "Add Record0"):  # Swing Trade Add Record
                if (str(values['-SWINGTRADE_STOCK_SYMBOL-']) == "") or (str(values['-SWINGTRADE_AMOUNT-']) == "") or (str(values['-SWINGTRADE_BUY_PRICE-']) == "") or (str(values['-SWINGTRADE_STOP_LOSS-']) == "") or (str(values['-SWINGTRADE_TARGET-']) == "") or (str(values['-SWINGTRADE_STATUS-']) == ""):
                    gui.popup_ok("Please Fill All the Values", background_color="black",text_color="yellow")

                else:
                    list_of_values = []
                    Intraday_Stock_symbol = values['-SWINGTRADE_STOCK_SYMBOL-']
                    Type_of_Trade = "Swing Trade"
                    Amount = values['-SWINGTRADE_AMOUNT-']
                    Buy_price = (float)(values['-SWINGTRADE_BUY_PRICE-'])
                    Stop_loss = (float)(values['-SWINGTRADE_STOP_LOSS-'])
                    Target = float(values['-SWINGTRADE_TARGET-'])
                    Risk = Buy_price - Stop_loss
                    Reward = Target - Buy_price
                    Status = values['-SWINGTRADE_STATUS-']
                    R_Multiple = float("{:.2f}".format(Reward / Risk))
                    R_Multiple = str(R_Multiple) + "R"


                    list_of_values.append(Intraday_Stock_symbol)
                    list_of_values.append(Type_of_Trade)
                    list_of_values.append(Amount)
                    list_of_values.append(str(Buy_price))
                    list_of_values.append(str(Stop_loss))
                    list_of_values.append(str(Target))
                    list_of_values.append(R_Multiple)
                    list_of_values.append(Status)




                    self.Insert_Data_In_Table(connection_string, connection_string, "SwingTrade_Ledger", list_of_values)

                    result_values = self.Show_Data_from_table(connection_string, connection_cursor, "SwingTrade_Ledger")
                    Intermediate_Process_result_values = list(map(lambda x: [x], result_values))
                    Final_Processed_Result_Values = list(map(lambda x: list(x[0]),  Intermediate_Process_result_values))


                    window.Element('-SWINGTRADE_LEDGER_TABLE-').update(values= Final_Processed_Result_Values)
                    window['-SWINGTRADE_STOCK_SYMBOL-'].update('')
                    window['-SWINGTRADE_BUY_PRICE-'].update('')
                    window['-SWINGTRADE_AMOUNT-'].update('')
                    window['-SWINGTRADE_STOP_LOSS-'].update('')
                    window['-INTRADAY_STOP_LOSS-'].update('')
                    window['-SWINGTRADE_TARGET-'].update('')
                    window['-SWINGTRADE_STATUS-'].update('')

            elif (event == "Clear Record1"):  # Swing Trade Clear Record
                window['-SWINGTRADE_STOCK_SYMBOL-'].update('')
                window['-SWINGTRADE_BUY_PRICE-'].update('')
                window['-SWINGTRADE_AMOUNT-'].update('')
                window['-SWINGTRADE_STOP_LOSS-'].update('')
                window['-INTRADAY_STOP_LOSS-'].update('')
                window['-SWINGTRADE_TARGET-'].update('')
                window['-SWINGTRADE_STATUS-'].update('')

        connection_string.close()
        window.close()

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
                                            (       Stock_Symbol text,
                                                    Type_of_Trade text,
                                                    Amount text,
                                                    Buy_Price text,
                                                    Stop_Loss text,
                                                    Target text,
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

        connection_string = self.DatabaseConnection_String_Setup()
        connection_cursor = self.DatabaseConnection_cursor_Setup(connection_string)

        if self.Check_If_Table_Exists(connection_string, connection_cursor,
                                      "SwingTrade_Ledger") < 1:  # Checking If table Exist ,by checking return count from method Check_if_table_exist
            self.CreateTableSwingTrade(connection_string, connection_cursor)

        if self.Check_If_Table_Exists(connection_string, connection_cursor,
                                      "Intraday_Ledger") < 1:  # Checking If table Exist ,by checking return count from method Check_if_table_exist
            self.CreateTableIntradayTrade(connection_string, connection_string)

        gui.SetOptions(element_padding=(width_of_screen / 150, height_of_screen / 150))
        data = [['0', '1', '2', '3', '4', '5', '6', '7']]

        # data = [self.Show_Data_from_table(connection_string,connection_cursor,"Intraday_Ledger")]
        header_list = ["Stock_Symbol", "Type_of_Trade", "Amount", "Buy_Price", "Stop_Loss", "Target", "R_Multiple",
                       "Status"]
        layout = [
            [
                gui.Frame(
                    layout=[
                        [gui.Text('Stock Symbol', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN),
                         gui.Input()],
                        [gui.Text('Type of Trade', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN),
                         gui.Text('Intraday', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN)],
                        [gui.Text('Amount', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN), gui.Input()],
                        [gui.Text('Buy Price', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN),
                         gui.Input()],
                        [gui.Text('Stop Loss', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN),
                         gui.Input()],
                        [gui.Text('Target', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN), gui.Input()],
                        [gui.Text('Status', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN), gui.Input()],
                        [gui.Button('Add Record', enable_events=True), gui.Button('Clear Record')]

                    ], title="INTRADAY LEDGER", title_color="Black", relief=gui.RELIEF_SOLID,
                    background_color="light green", border_width=10
                ),
                gui.Frame(
                    layout=[
                        [gui.Text('Stock Symbol', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN),
                         gui.Input()],
                        [gui.Text('Type of Trade', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN),
                         gui.Text('Swing Trade', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN)],
                        [gui.Text('Amount', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN), gui.Input()],
                        [gui.Text('Buy Price', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN),
                         gui.Input()],
                        [gui.Text('Stop Loss', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN),
                         gui.Input()],
                        [gui.Text('Target', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN), gui.Input()],
                        [gui.Text('Status', text_color="black", size=(20, 1), relief=gui.RELIEF_SUNKEN), gui.Input()],
                        [gui.Button('Add Record'), gui.Button('Clear Record')]

                    ], title="SWING TRADE LEDGER", title_color="Black", relief=gui.RELIEF_SOLID,
                    background_color="LIGHT PINK", border_width=10
                ),
            ],
            [gui.Table(values=data,
                       headings=header_list,
                       display_row_numbers=True,
                       auto_size_columns=False,
                       key='-INTRADAY_LEDGER_TABLE-',
                       num_rows=min(25, len(data))),

             gui.Table(values=data,
                       headings=header_list,
                       display_row_numbers=True,
                       auto_size_columns=False,
                       key='-SWINGTRADE_LEDGER_TABLE-',
                       num_rows=min(25, len(data)))

             ]
        ]

        window = gui.Window('Bramahastra', layout, size=(width_of_screen, height_of_screen))

        while True:
            event, values = window.read()
            print(f"event : {event} and values:{values}")
            print(type(values))
            print(values[0])

            if (event == gui.WIN_CLOSED) or (event == "Exit"):
                break
            elif (event == "Add Record"):  # Intraday Add Record
                list_of_values = []
                Intraday_Stock_symbol = values[0]
                Type_of_Trade = "Intrady"
                Amount = values[1]
                Buy_price = (int)(values[2])
                Stop_loss = int(values[3])
                Target = int(values[4])
                Risk = Buy_price - Stop_loss
                Reward = Target - Buy_price
                Status = values[5]
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
                print(result_values)
                a = [['Drreddy', 'Intrady', 'Intrady', 'Intrady', 'v', 'Intrady', 'Intrady', 'profit']]

                window('-INTRADAY_LEDGER_TABLE-').update(values=a)

                pass
            elif (event == "Clear Record"):  # Intraday Clear Record
                pass
            elif (event == "Add Record0"):  # Swing Trade Add Record
                pass
            elif (event == "Clear Record1"):  # Swing Trade Clear Record
                pass

        connection_string.close()
        window.close()

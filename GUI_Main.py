import PySimpleGUI as gui
import numpy
import pyautogui #GetSystemMetrics is used to get Currently set Screen Resolution ,so that application window should open accordingly the screen size
from PySimpleGUI import WIN_CLOSED
from Download_Raw_data_module import class_Download_raw_data_Operation
from PromoterSetup_module import Promoter_setup
from Trading_Journal_Module import TradingJournal



#Creating Objects for imported Class
object_Download_raw_data_operation = class_Download_raw_data_Operation()
object_Promoter_Strategy_operation = Promoter_setup()
object_Trading_journal = TradingJournal()


gui.theme('tanblue')
coordinates = pyautogui.size()
width_of_screen = coordinates[0]
height_of_screen = coordinates[1]
text_color_variable_value = "yellow"
background_color_variable_value = "black"

layout = [
            [
                gui.Button("Download",font=('MS Sans Serif', 10, 'bold'),button_color=('red', 'white')),
                gui.Button("Promoter Setup",font=('MS Sans Serif', 10, 'bold'),button_color=('red', 'white')),
                gui.Button("Swing Trading Setup",font=('MS Sans Serif', 10, 'bold'),button_color=('red', 'white')),
                gui.Button("Trading Journal",font=('MS Sans Serif', 10, 'bold'),button_color=('red', 'white')),
                gui.Button("Configuration",font=('MS Sans Serif', 10, 'bold'),button_color=('red', 'white')),
                gui.Button("Read Logs",font=('MS Sans Serif', 10, 'bold'),button_color=('red', 'white')),
                gui.Button("Exit",font=('MS Sans Serif', 10, 'bold'),button_color=('red', 'white'))
            ]
          ]

window = gui.Window('Bramahastra',layout,size=(width_of_screen,height_of_screen))

while True:
    event,values = window.read()

    if (event == gui.WIN_CLOSED) or (event == "Exit"):
        break
    elif event == "Download":
        object_Download_raw_data_operation.download()
        gui.popup_ok("Data Downloaded",background_color=background_color_variable_value,text_color=text_color_variable_value)
    elif event == "Read Logs":
        gui.popup_scrolled(object_Download_raw_data_operation.ReadLogs())
    elif event == "Configuration":
         gui.theme_previewer()
    elif event == "Trading Journal":
        object_Trading_journal.Gui_Formation()

    elif event == "Promoter Setup":
        object_Promoter_Strategy_operation.main()


    elif event == "Swing Trading Setup":
        object_Download_raw_data_operation.Show_Fo_bhav_Copy()



window.close()

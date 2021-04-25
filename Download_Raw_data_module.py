import requests
import logging

import PySimpleGUI as gui
from datetime import  date

from Business_logics_module import Business_Logics
from Folder_operations_module import Folder_Operation


import pandas as pd
import datetime



class class_Download_raw_data_Operation():
    object_folder_operation = Folder_Operation()
    business_logic_object = Business_Logics()
    def __init__(self):
        Log_FilePath = class_Download_raw_data_Operation.object_folder_operation.Create_Folder_to_Stor_ApplicationLogs_IfDoesnot_Exist()
        print(Log_FilePath)
        logging.basicConfig(filename=Log_FilePath+"/"+"ApplicationLogs.log",format='%(asctime)s %(levelname)-8s %(message)s',level=logging.DEBUG,datefmt='%d-%m-%Y %H:%M:%S')
        f = Folder_Operation()





    def download(self):
        today = date.today()
        x = datetime.datetime(today.year, today.month, today.day)
        Derivative_Date_Format = x.strftime("%d%b%Y").upper()
        Cash_Date_Format = x.strftime("%d%m%Y").upper()

        url_list  = ["https://archives.nseindia.com/content/historical/DERIVATIVES/2021/APR/fo{0}bhav.csv.zip".replace("{0}",Derivative_Date_Format),"https://archives.nseindia.com/products/content/sec_bhavdata_full_{0}.csv".replace("{0}",Cash_Date_Format)]
        print(url_list)
        Parent_file_Path = class_Download_raw_data_Operation.object_folder_operation.Create_DownloadFolder_ifDoesnot_Exist()
        for url in url_list:
            r = ''
            try:
                r = requests.get(url,allow_redirects=False) #allow_redirects set to False ,to avoid going to NSE 404 error page and then finding out file doesn't exist
            except:
                print("###########################################in Excpetion#########################################################")
                gui.popup_ok("Oops ! Some error occured ,Close The Application and Start Again")
                #self.download()
            if (r.status_code == 200):
                if (len(url.split("/")[-1]) > 0):
                    logging.info("File Exists and it is downloadable")
                    open(Parent_file_Path+"/"+url.split("/")[-1],'wb').write(r.content)
                    if "zip" in url.split("/")[-1]:
                      class_Download_raw_data_Operation.object_folder_operation.unzip_operation(Parent_file_Path+"/"+url.split("/")[-1])
                      class_Download_raw_data_Operation.object_folder_operation.remove_zip_file_after_extraction(Parent_file_Path+"/"+url.split("/")[-1])
                else:
                    logging.debug("There is some Issue with Downloading URL or check with sushen to debug the issue")

            else:
                   logging.warning("File Not Downloadable,because It Doesn't Exist")

    def ReadLogs(self):
        Log_FilePath = class_Download_raw_data_Operation.object_folder_operation.Create_Folder_to_Stor_ApplicationLogs_IfDoesnot_Exist()
        f = open(Log_FilePath+"/"+"ApplicationLogs.log", "r")
        text = f.read()
        return text

    def Show_Fo_bhav_Copy(self):
        list_of_FO_files_Downloaded = self.object_folder_operation.Downloaded_FO_Bhav_CopyFiles()
        list_of_Cash_files_Downloaded = self.object_folder_operation.Downloaded_Cash_Files()
        self.business_logic_object.Future_and_Cash_Data(list_of_FO_files_Downloaded,list_of_Cash_files_Downloaded)


    def Experiment_Show_Fo_bhav_Copy(self):
        list_of_FO_files_Downloaded = self.object_folder_operation.Downloaded_FO_Bhav_CopyFiles()
        list_of_Cash_files_Downloaded = self.object_folder_operation.Downloaded_Cash_Files()
        self.business_logic_object.Experiment_Future_Data_Processing(list_of_FO_files_Downloaded)
        # Event_Operation.business_logic_object.Future_and_Cash_Data()






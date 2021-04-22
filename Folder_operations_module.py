import  os
import zipfile
import glob
class Folder_Operation():
    path = 'FObhavCopy_Data'
    LogPath = 'ApplicationLogs'
    stock_list_path = 'Stock_list//fo19MAR2021bhav.csv'
    Nifty_400_stock_list_path = 'Stock_list//ind_nifty500list.csv'
    def Create_DownloadFolder_ifDoesnot_Exist(self):

        if not os.path.exists(Folder_Operation.path):
            print("not exits")
            os.mkdir(Folder_Operation.path)
            return Folder_Operation.path
        else:
            print("exists")
            return Folder_Operation.path

    def Create_Folder_to_Stor_ApplicationLogs_IfDoesnot_Exist(self):
        if not os.path.exists(Folder_Operation.LogPath):
            os.mkdir(Folder_Operation.LogPath)
            return Folder_Operation.LogPath
        else:
            return Folder_Operation.LogPath


    def unzip_operation(self,filepath):
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(Folder_Operation.path)

    def remove_zip_file_after_extraction(self,filepath):
        if os.path.exists(filepath):
            os.remove(filepath)

    def Downloaded_FO_Bhav_CopyFiles(self):
        filelist = []
        for name in glob.glob('FObhavCopy_Data//FO_Files//[0-9][0-9]_fo*bhav.csv'):
            filelist.append(name)
        print(filelist)
        return filelist

    def Downloaded_Cash_Files(self):
        filelist = []
        for name in glob.glob('FObhavCopy_Data//[0-9][0-9]_sec_bhavdata_full_*.csv'):
            filelist.append(name)

        for name in glob.glob('FObhavCopy_Data//[0-9][0-9][0-9]_sec_bhavdata_full_*.csv'):
            filelist.append(name)

        return filelist



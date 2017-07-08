import glob, os
import pandas as pd
import general_utils as Ugen
import csv
import chardet

##GET DATA
#GET FILES
main_dir=os.getcwd()

allFiles1 = glob.glob(main_dir.split('/Studies')[0]+'/toronto_parking_data'+ "/*.csv")
allFiles = glob.glob(main_dir.split('/Studies')[0]+'/toronto_parking_data/extra'+ "/*.csv")

# LOAD TO DATAFRAME
list_ = []
for file_path in allFiles1:#allFiles[-3:]: --the following works for all but 2008,2010
    try:
        df = pd.read_csv(file_path,index_col=None,quoting=2,error_bad_lines=False) #quoting=2
        list_.append(df)
        print ('successfully loaded: '+ file_path)
    except Exception as err:
        if 'EOF following escape character' in str(err):
            try:
                df = pd.read_csv(file_path,index_col=None,encoding='utf-16',error_bad_lines=False) #quoting=2
                list_.append(df)
                print ('successfully loaded: '+ file_path)
            except Exception as err:
                print ('NOT loaded: '+ file_path)
                print (str(err))
        else:
            print ('NOT loaded: '+ file_path)
            print (str(err))
#
# #LOAD TO DATAFRAME
# list_ = []
# for file_path in allFiles:#allFiles[-3:]:
#     try:
#         df = pd.read_csv(file_path,index_col=None,encoding='utf-8',error_bad_lines=False) #quoting=2
#         list_.append(df)
#         print ('successfully loaded: '+ file_path)
#     except Exception as err:
#         if 'EOF following escape character' in str(err):
#             try:
#                 df = pd.read_csv(file_path,index_col=None,encoding='utf-16',error_bad_lines=False) #quoting=2
#                 list_.append(df)
#                 print ('successfully loaded: '+ file_path)
#             except Exception as err:
#                 print ('NOT loaded: '+ file_path)
#                 print (str(err))
#         else:
#             print ('NOT loaded: '+ file_path)
#             print (str(err))


df=None
list_=None

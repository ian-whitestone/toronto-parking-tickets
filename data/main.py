import general_utils as Ugen
import pandas as pd
import glob, os


##IDEAS
#1) Location based profitability
#2) most profitable ticket types
#3) most common time of infraction

## GET DATA
# GET FILES
main_dir = os.getcwd()
allFiles = glob.glob(main_dir +'/src' + "/*.csv")

#LOAD TO DATAFRAME
list_ = []
for file_path in allFiles[-7:]:#allFiles: #START WITH 2014/2015 DATA
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

tpt_df = pd.concat(list_)


##CLEAN DF
#get rid of unnecessary columns
tpt_df = tpt_df.drop(['tag_number_masked','location3','location4','province'],axis=1)
tpt_df['date'] = tpt_df['date_of_infraction'].apply(lambda x: datetime.datetime.strptime(str(x),'%Y%m%d'))

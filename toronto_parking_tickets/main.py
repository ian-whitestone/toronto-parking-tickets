import general_utils as Ugen
import matplotlib.pyplot as plt
import pandas as pd
import math
from pandas.tools.plotting import scatter_matrix
import numpy as np
import glob, os


##IDEAS
#1) Location based profitability
#2) most profitable ticket types
#3) most common time of infraction
#4)

##GET DATA
#GET FILES
main_dir=os.getcwd()
allFiles = glob.glob(main_dir+'/toronto_parking_data'+ "/*.csv")

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
tpt_df=tpt_df.drop(['tag_number_masked','location3','location4','province'],axis=1)
#drop rows with missing location2
tpt_df=tpt_df[pd.notnull(tpt_df_mod['location2'])]


##CREATE NEW DF
tpt_grouped_df=pd.DataFrame({'count' : tpt_df.groupby( ['infraction_code','location2'] ).size()}).reset_index()

##now calculate total amount...
##create dict of infraction_code:fine_amount
fine_amount_dict={ic:{'fine_amt':tpt_df[tpt_df['infraction_code']==ic].set_fine_amount.median(),
                      'fine_descp':tpt_df[tpt_df['infraction_code']==ic].infraction_description.iloc[0]}
                          for ic in infraction_ids}

def calc_fine_sum(df):
    return df['count']*fine_amount_dict[df['infraction_code']]['fine_amt']

def get_fine_descrp(df):
    return fine_amount_dict[df['infraction_code']]['fine_descp']






##

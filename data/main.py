import general_utils as Ugen
import pandas as pd
import glob, os
import logging as log
import database_operations as dbo
import config
import datetime
import DataCleaning

log.basicConfig(
    format='%(asctime)s  - %(module)s - %(levelname)s - %(message)s',
    level=log.DEBUG, # Change debug level to choose how verbose you want logging to be
    )


## IDEAS
#1) Location based profitability
#2) most profitable ticket types
#3) most common time of infraction



## GET DATA

# GET FILES
main_dir = os.getcwd()
allFiles = glob.glob(main_dir +'/src' + "/*.csv")

#LOAD TO DATAFRAME
print ('Attempting to load files')

dfs = []
for file_path in [allFiles[2]]:
    try:
        df = pd.read_csv(file_path,index_col=None,quoting=2,
                            error_bad_lines=False) #quoting=2
        dfs.append(df)
        print ('successfully loaded: '+ file_path)
    except Exception as err:
        if 'EOF following escape character' in str(err):
            try:
                df = pd.read_csv(file_path,index_col=None,
                                        encoding='utf-16',error_bad_lines=False)
                dfs.append(df)
                print ('successfully loaded: '+ file_path)
            except Exception as err:
                print ('NOT loaded: '+ file_path)
                print (str(err))
        else:
            print ('NOT loaded: '+ file_path)
            print (str(err))

tpt_df = pd.concat(dfs)


## CLEAN DF
# get rid of unnecessary columns
tpt_df = tpt_df.drop(['tag_number_masked','location3','location4'],axis=1)

print ('Creating date column')
tpt_df['date'] = tpt_df['date_of_infraction'].apply(
    lambda x: datetime.datetime.strptime(str(x),'%Y%m%d'))

tpt_df = tpt_df.where((pd.notnull(tpt_df)), None)

def cleanRecord(record):
    fields = []
    for field in config.FIELD_MAP:
        val = record.get(field['name'], None)
        if val:
            cleaned_val = getattr(DataCleaning, field['func'])(val=val,
                            length=field.get('length',0))
        else:
            cleaned_val = None
        fields.append(cleaned_val)

    return fields

print ('Converting to dict')
records = tpt_df.to_dict('records')


print ('Creating records list')
data = []
for record in records:
    cleaned_record = cleanRecord(record)
    data.append(cleaned_record)

print ('Loading to Postgres')
conn = dbo.getConnection()
dbo.postgres_load(conn, 'tickets', data)

dbo.closeConnection(conn)

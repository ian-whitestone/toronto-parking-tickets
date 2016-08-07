import unicodecsv
import seaborn as sns
import datetime as dt
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
import matplotlib as mpl
import configparser  

def read_csv(filename):
    with open(filename, 'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)

def seaborn_plot(df,plot_type='pairplot',columns=False):
	sns.set()
	mpl.rc("figure", figsize=(16, 8.65))
	plotting_df=(df[columns] if columns else df)
	if plot_type=='pairplot':
		sns.pairplot(plotting_df)
	elif plot_type=='corr_plot':
		sns.corrplot(plotting_df)
	sns.plt.show()
	return

def explore_list(list_name,num_iter):
	for entry,i in zip(list_name,range(num_iter)):
		print (entry)

def parse_data_type(data,data_type):
	if data=='':
		return None
	elif data_type=='float':
		return float(data)
	elif data_type=='int':
		return int(data)
	else:
		return data

def parse_date(date,date_format): #requires expected date format '%Y-%m-%d'
	if date=='':
		return None
	else:
		return dt.datetime.strptime(date,date_format)

def ConfigSectionMap(section):
	Config = configparser.ConfigParser()
	config_path = '/Users/whitesi/Documents/Programming/Python/db.ini'
	Config.read(config_path)
	dict1 = {}
	options = Config.options(section)
	for option in options:
	    try:
	        dict1[option] = Config.get(section, option)
	        if dict1[option] == -1:
	            DebugPrint("skip: %s" % option)
	    except:
	        print("exception on %s!" % option)
	        dict1[option] = None
	return dict1

def convert_csv_entries(csv_list,int_fields,float_fields,date_fields): #Need to add int fields option and func
	for entry in csv_list:
		for key,value in entry.items():
			try:
				if key in float_fields:
					entry[key]=parse_data_type(value,'float')
				elif key in int_fields:
					entry[key]=parse_data_type(value,'int')
				elif key in date_fields:
					entry[key]=parse_date(value)
			except: #exception handler was added to find out which fields were meant to be floats..
				print ('error converting: %s' % key)
	return csv_list

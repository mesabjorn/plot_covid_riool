import pandas as pd
import sys
import matplotlib.pyplot as plt

def load_csv(city):
	df = pd.read_csv("./COVID-19_rioolwaterdata.csv",sep=";",index_col="Date_measurement")
	
	dfsel = df.loc[df.RWZI_AWZI_name==city]
	
	f,ax = plt.subplots(1,1,figsize=(10,7))
	#ax[0].plot(dfsel.index,dfsel.RNA_per_ml)
	ax.plot(dfsel.index,dfsel.RNA_flow_per_100000,'o-',label="RNA_per_ml")
	plt.xticks(rotation=30,ha="right")
	ax.set_ylabel("RNA per ml")
	ax.set_title(city)
	plt.show()
	


if __name__=="__main__":	
	if(len(sys.argv)==2):
		city = sys.argv[1]
	else:
		city="Ursem"
	load_csv(city)
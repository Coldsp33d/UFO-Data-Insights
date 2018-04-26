import pandas as pd

# --- distance versus duration -- #
df = pd.read_csv('../Data/ufo_awesome_v2.csv', compression='gzip', low_memory=False) 
v = df.dropna(subset=['airport_distance'])
i = pd.cut(
        pd.to_numeric(v.duration, errors='coerce'), 
        bins=[0, 60, 300, 3600], 
        labels=['<1min', '1-5 min', '1hr'])
j = pd.cut(
        v.airport_distance, 
        bins=[0, 5, 10, 15, 20, 25, pd.np.inf], 
        labels=['<5mi', '5-10mi', '10-15mi', '15-20mi', '20-25mi', '>25mi']
)

i.groupby(j).value_counts().unstack(-1, fill_value=0).to_csv('../ufo.usc.edu/Data/horizontal_stacked_distance_duration.tsv',sep='\t',index=False)
#convert tsv to js file

jsObjectLabels =  ['#<5mi#', '#5-10mi#', '#10-15mi#', '#15-20mi#', '#20-25mi#', '#>25mi#']

fpath = '../ufo.usc.edu/Data/horizontal_stacked_distance_duration.tsv'
df = pd.read_csv(fpath, sep='\t')

tempDict1 = {}
tempDict2 = {}
tempDict3 = {}

for index,row in df.iterrows():

	
	if 'label' not in tempDict1:
		tempDict1['label'] = '#<1min#'
	if 'values' not in tempDict1:
		tempList = []
		tempList.append(row['<1min'])
		tempDict1['values'] = tempList
	else:
		tempList = tempDict1['values']
		tempList.append(row['<1min'])
		tempDict1['values'] = tempList
	##########
	
	if 'label' not in tempDict2:
		tempDict2['label'] = '#1-5 min#'
	if 'values' not in tempDict2:
		tempList = []
		tempList.append(row['1-5 min'])
		tempDict2['values'] = tempList
	else:
		tempList = tempDict2['values']
		tempList.append(row['1-5 min'])
		tempDict2['values'] = tempList
	####
	if 'label' not in tempDict3:
		tempDict3['label'] = '#1hr#'
	if 'values' not in tempDict3:
		tempList = []
		tempList.append(row['1hr'])
		tempDict3['values'] = tempList
	else:
		tempList = tempDict3['values']
		tempList.append(row['1hr'])
		tempDict3['values'] = tempList
	
	#print(row['<1min'],row['1-5 min'],row['1hr'])
finalDict = {}
if 'labels' not in finalDict:
	finalDict['labels'] =  jsObjectLabels
	
if 'series' not in finalDict:
	tempList = []
	tempList.append(tempDict1)
	tempList.append(tempDict2)
	tempList.append(tempDict3)
	finalDict['series'] = tempList
tempStr = "var data = "+str(finalDict).replace("'","").replace("#","'")

f2=open("../ufo.usc.edu/Data/horizontal_stacked_distance_duration.js","w")
f2.write(tempStr)
f2.close()
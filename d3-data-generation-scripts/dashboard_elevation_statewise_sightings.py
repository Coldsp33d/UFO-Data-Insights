import pandas
import numpy as np 
df = pandas.read_csv("../Data/ufo_awesome_v2.csv",compression='gzip')
df1 = df[np.isfinite(df['elevation'])]
df2 = df[['state','elevation']]
mask = (df2['elevation'] > 0.0) & (df2['elevation'] <= 500.0)
df3 =df2.loc[mask]
df4  = df3.groupby(['state'],as_index = False).elevation.agg({'upto500':'size'})
mask = (df2['elevation'] > 500.0) & (df2['elevation'] <= 1000.0)
df3 =df2.loc[mask]
df5  = df3.groupby(['state'],as_index = False).elevation.agg({'upto1000':'size'})
mask = (df2['elevation'] > 1000.0) 
df3 =df2.loc[mask]
df6  = df3.groupby(['state'],as_index = False).elevation.agg({'greaterthan1000':'size'})
dffinal = pandas.merge(df4,df5,on='state',how ='outer')
dffinal = pandas.merge(dffinal,df6,on='state',how ='outer')
dffinal = dffinal.fillna(0)
dffinal['Total']= dffinal.iloc[:, -4:-1].sum(axis=1)
dffinal = dffinal.sort_values(['Total'],ascending = False)
dffinal = dffinal.head(10)
data = dffinal.iloc[:,0:4].set_index('state').groupby(level=0).apply(lambda x:dict(zip(x.columns,x.iloc[0]))).to_dict()
import json
with open('../Data/dashboard_elevation_statewise_sightings.json','w')as j:
	json.dump(data,j)
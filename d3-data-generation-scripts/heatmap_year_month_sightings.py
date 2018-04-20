import pandas

df = pandas.read_csv("../Data/ufo_awesome_v2.csv",compression='gzip')
df['sighted_at']= pandas.to_datetime(df.sighted_at,errors='coerce')
mask = (df['sighted_at'] > '2005-1-1') & (df['sighted_at'] <= '2016-1-1')
df2 =df.loc[mask]
df2['month'] = df2.sighted_at.dt.month
df2['year']= df2.sighted_at.dt.year
df3  = df2.groupby(['month','year'],as_index = False).country.agg({'sightings':'size'})
df3.to_csv("../Data/heatmap_year_month_sightings.tsv", sep ='\t',index=False)

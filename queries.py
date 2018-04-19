import pandas as pd

# get the relative frequency of the top-10 sighted UFO shapes
df = pd.read_csv('Data/Resources/ufo_awesome_v2.csv', compression='gzip', low_memory=False)

v = (df['shape']
	 .str.title()
	 .str.split(r',\s*', expand=True)
	 .stack()
	 .value_counts()
	 .head(10)
)

(v / v.sum() * 100).rename_axis('Shape').reset_index(name='Frequency').to_csv('Data/shape-freq-dist.csv')

# --- distance versus duration -- # 
v = df.dropna(subset=['airport_distance'])
i = pd.cut(
        pd.to_numeric(v.duration, errors='coerce'), 
        bins=[0, 60, 300, 3600, pd.np.inf], 
        labels=['<1min', '1-5 min', '1hr', '>1hr'])
j = pd.cut(
        v.airport_distance, 
        bins=[0, 5, 10, 15, 20, 25, pd.np.inf], 
        labels=['<5mi', '5-10mi', '10-15mi', '15-20mi', '20-25mi', '>25mi']
)

i.groupby(j).value_counts().unstack(-1, fill_value=0).to_csv('Data/dur-vs-dist.csv')

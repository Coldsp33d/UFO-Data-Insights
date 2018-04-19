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


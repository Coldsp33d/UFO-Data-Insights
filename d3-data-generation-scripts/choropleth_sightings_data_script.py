import pandas as pd
ufo_awesome_v2 = pd.read_csv('../Data/ufo_awesome_v2.csv',compression='gzip')
country_sightings_data = ufo_awesome_v2.groupby('country', as_index=False).state.agg({'sightings':'size'})
country_sightings_data.to_csv('../ufo.usc.edu/Data/country_sightings_data.tsv',sep='\t',index=False)
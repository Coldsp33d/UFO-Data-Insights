import pandas as pd

# --- temp v/s precipitation --- #
pd.np.random.seed(0)
df = pd.read_csv('../Data/ufo_awesome_v2.csv', compression='gzip', low_memory=False)
st = df.state.value_counts().nlargest(3).index
(df.query('state in @st')[['precipitation', 'temp_avg', 'state']]
   .dropna()
   .sample(n=500)
   .to_csv('../ufo.usc.edu/Data/scatterplot_temperature_precipitation.tsv',sep='\t',index=False)
)
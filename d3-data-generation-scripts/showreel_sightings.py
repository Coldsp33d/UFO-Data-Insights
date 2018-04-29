import pandas as pd
from pandas.tseries.offsets import MonthBegin


df = pd.read_csv('../Data/Resources/ufo_awesome_v2.csv', compression='gzip', low_memory=False)
today = pd.to_datetime('today')
# --- showreel dataset --- #
cnt = df.country.value_counts().nlargest(4).index
v = df[['country', 'sighted_at']].dropna().query('country in @cnt')
v['sighted_at'] = (
	pd.to_datetime(v['sighted_at'], errors='coerce').dt.floor('D').clip_upper(today)
)
v = v[(v.sighted_at >= '2010-01-01') & (v.sighted_at <= today)]

v = (v.groupby(['country', v.sighted_at.dt.strftime('%b %Y')])
 .country
 .agg({'sightings': 'count'})
 .reset_index()
)
v['sighted_at'] = pd.to_datetime(v.sighted_at)
v = v.sort_values(['country', 'sighted_at'])
m1, m2 = v.sighted_at.agg(['min', 'max'])
idx = pd.date_range(m1, m2, inclusive=True, freq='M') + MonthBegin(-1)
v = v.set_index('sighted_at').groupby('country', group_keys=False).apply(lambda x: x.reindex(idx)).rename_axis('sighted_at').reset_index()
v.country = v.country.ffill()
v.sightings = v.sightings.fillna(0).astype(int)

v['sighted_at'] = v.sighted_at.dt.strftime('%b %Y')


v[['country', 'sighted_at', 'sightings']].to_csv('../Data/shoreel-summary.csv', index=False, header=None)
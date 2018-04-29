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
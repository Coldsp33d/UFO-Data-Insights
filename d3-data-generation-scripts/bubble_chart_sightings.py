import pandas as pd
import json
# --- urban v/s rural --- #
df = pd.read_csv('../Data/Resources/ufo_awesome_v2.csv', compression='gzip', low_memory=False)
states = json.load(open('../Data/Resources/states.json'))
v = df.assign(abbr=df['state'])[['state', 'abbr']]
v['state'] = v['state'].map(states)
v = v.dropna(subset=['state'])
(v.groupby(['state', 'abbr'])
  .size()
  .sort_values(ascending=False)
  .reset_index(name='count')[['state', 'count', 'abbr']]
  .to_csv('../Data/bubble_chart_sightings.csv', index=False)
)
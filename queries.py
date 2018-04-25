import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer

from pandas.tseries.offsets import MonthBegin

lemmatizer = WordNetLemmatizer()
today = pd.to_datetime('today')

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


# --- temp v/s precipitation --- #
np.random.seed(0)
st = df.state.value_counts().nlargest(3).index
(df.query('state in @st')[['precipitation', 'temp_avg', 'state']]
   .dropna()
   .sample(n=500)
   .to_csv('Data/temp-vs-precip.csv')
)

# --- wordcloud --- #
with open('Data/Resources/stopwords.txt') as f:
	stopwords = set(
		itertools.chain.from_iterable(x.split('\t') for x in f.read().splitlines())
	)

sentences = df.summary.dropna().str.lower().str.replace(r'[^a-z\s]', '').tolist()
common_words = Counter(itertools.chain.from_iterable(
	([lemmatizer.lemmatize(w) for w in set(sent.split()) - stopwords] for sent in sentences)
)).most_common(100)

pd.DataFrame(common_words, columns=['text', 'size']).to_json('Data/wordcloud-data.json', orient='records')


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


v[['country', 'sighted_at', 'sightings']].to_csv('Data/shoreel-summary.csv', index=False, header=None)


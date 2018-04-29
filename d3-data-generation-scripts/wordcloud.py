with open('Data/Resources/stopwords.txt') as f:
	stopwords = set(
		itertools.chain.from_iterable(x.split('\t') for x in f.read().splitlines())
	)

sentences = df.summary.dropna().str.lower().str.replace(r'[^a-z\s]', '').tolist()
common_words = Counter(itertools.chain.from_iterable(
	([lemmatizer.lemmatize(w) for w in set(sent.split()) - stopwords] for sent in sentences)
)).most_common(100)

pd.DataFrame(common_words, columns=['text', 'size']).to_json('Data/wordcloud-data.json', orient='records')
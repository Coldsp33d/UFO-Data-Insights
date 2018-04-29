import pandas as pd
# --- urban v/s rural --- #
df = pd.read_csv('../Data/Resources/ufo_awesome_v2.csv', compression='gzip', low_memory=False)
df['is_urban'].map({True: 'urban', False : 'rural' }).value_counts(normalize=True).to_csv('../Data/urban-rural-ratio.csv')

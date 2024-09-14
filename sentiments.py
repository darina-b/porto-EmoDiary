SQL:
SELECT state, count(name)
FROM df
GROUP BY state
ORDER BY state;

Here’s the near-equivalent in pandas:
n_by_state = df.groupby("state")["last_name"].count()
n_by_state.head(10)


from datetime import datetime, timedelta
from pathlib import Path
#### from textblob import TextBlob
from random import choice, shuffle
import re
import nltk
nltk.download(["stopwords","twitter_samples","movie_reviews","vader_lexicon","punkt", "punkt_tab","tagset"])
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.help.upenn_tagset()
#############################################################
# MODEL 2 # SENTIMENT EVALUATION MODEL:

### Reading the Dataset ###
import pandas as pd

# Selecting a subset of data to be faster in demonstration
train_df = pd.read_csv('../input/imdb-dataset-sentiment-analysis-in-csv-format/Train.csv').head(4000)
valid_df = pd.read_csv('../input/imdb-dataset-sentiment-analysis-in-csv-format/Valid.csv').head(500)
test_df = pd.read_csv('../input/imdb-dataset-sentiment-analysis-in-csv-format/Test.csv').head(500)
print('Train: '+ str(len(train_df)))
print('Valid: '+ str(len(valid_df)))
print('Test: '+ str(len(test_df)))
train_df.head(10)

### Text pre-processing ###
# Turnig all text to lowercase
train_df['text'] = train_df['text'].str.lower()
valid_df['text'] = valid_df['text'].str.lower()
test_df['text'] = test_df['text'].str.lower()
train_df.head()

# Removing punctuation
import string

exclude = set(string.punctuation) 

def remove_punctuation(x): 
    try: 
        x = ''.join(ch for ch in x if ch not in exclude) 
    except: 
        pass 
    return x 

train_df['text'] = train_df['text'].apply(remove_punctuation)
valid_df['text'] = valid_df['text'].apply(remove_punctuation)
test_df['text'] = test_df['text'].apply(remove_punctuation)
train_df.head()

# Removing stopwords
from nltk.corpus import stopwords

stop = stopwords.words('english')

train_df['text'] = train_df['text'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))
valid_df['text'] = valid_df['text'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))
test_df['text'] = test_df['text'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))
train_df.head()

### Sentences as Bag of Words ### Classical Model with TF-IDF and SVM ###
from sklearn.feature_extraction.text import TfidfVectorizer

# Create feature vectors for every sentence
vectorizer = TfidfVectorizer(#min_df = 5,
                             #max_df = 0.8,
                             max_features = 20000,
                             sublinear_tf = True,
                             use_idf = True)#, stop_words='english')#vocabulary = list(embeddings_index.keys()

train_vectors = vectorizer.fit_transform(train_df['text'])
valid_vectors = vectorizer.transform(valid_df['text'])
test_vectors = vectorizer.transform(test_df['text'])

from sklearn import svm
# SVM
classifier_linear = svm.SVC(kernel='linear')
#Train
classifier_linear.fit(train_vectors, train_df['label'])

from sklearn.metrics import classification_report

predictions = classifier_linear.predict(test_vectors)
# results
report = classification_report(test_df['label'], predictions)
print(report)

#####################################################################################
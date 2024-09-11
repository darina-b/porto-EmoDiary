        if self.entry_sentiment['neu']>=0.6:
            return '50' #== Mood/Day: average
        else:
            if self.entry_sentiment['compound']<-0.5:
                return '0' #== Mood/Day: bad
            if self.entry_sentiment['compound']>0.5:
                return '100' #== Mood/Day: good    
            else:
                if self.entry_sentiment['neg']>0.4:
                    return '0' #== Mood/Day: bad
                else:
                    return '50' #== Mood/Day: averag      



def mood_checker (self):
        if -1<=self.entry_sentiment['compound']<=-0.7:
            return ('1', 'emo') #== Mood/Day: pretty bad
        elif -0.7<self.entry_sentiment['compound']<=-0.4:
            return ('2', 'emo') #== Mood/Day: Ok
        elif 0.4<self.entry_sentiment['compound']<=0.7:
            return ('3', 'emo') #== Mood/Day: average
        elif 0.7<self.entry_sentiment['compound']<=1:
            return ('4', 'emo') #== Mood/Day: great
        else:
            return ('0','neutral')

######################
nltk.download([
    #"names",
    "stopwords",
    #"state_union",
    "twitter_samples",
    "movie_reviews",
    #"averaged_perceptron_tagger",
    "vader_lexicon",
    "punkt",
    ])
from nltk.sentiment import SentimentIntensityAnalyzer

# NLTK - VADER: [from: https://realpython.com/python-nltk-sentiment-analysis/]
from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
sia.polarity_scores("Wow, NLTK is really powerful!") # <<<< Use YOUR own STR!!!!
# the line above returns a dict: {'neg': 0.0, 'neu': 0.295, 'pos': 0.705, 'compound': 0.8012}

#You’ll get back a dictionary of different scores. The negative, neutral, and positive scores are related: 
# They all add up to 1 and can’t be negative. The compound score is calculated differently. 
# It’s not just an average, and it can range from -1 to 1.

# Now you’ll put it to the test against real data using two different corpora. 
# First, load the twitter_samples corpus into a list of strings, making a replacement 
# to render URLs inactive to avoid accidental clicks:
tweets = [t.replace("://", "//") for t in nltk.corpus.twitter_samples.strings()]
# Now use the .polarity_scores() function of your SentimentIntensityAnalyzer instance to classify tweets:
from random import shuffle

def is_positive(tweet: str) -> bool:
    """True if tweet has positive compound sentiment, False otherwise."""
    return sia.polarity_scores(tweet)["compound"] > 0

shuffle(tweets)
for tweet in tweets[:10]:
    print(">", is_positive(tweet), tweet)
# In this case, is_positive() uses only the positivity of the compound score to make the call. 
# You can choose any combination of VADER scores to tweak the classification to your needs.
positive_review_ids = nltk.corpus.movie_reviews.fileids(categories=["pos"])
negative_review_ids = nltk.corpus.movie_reviews.fileids(categories=["neg"])
all_review_ids = positive_review_ids + negative_review_ids
# .fileids() exists in most, if not all, corpora. In the case of movie_reviews, 
# each file corresponds to a single review. Note also that you’re able to filter 
# the list of file IDs by specifying categories. This categorization is a feature 
# specific to this corpus and others of the same type.
# 
# Next, redefine is_positive() to work on an entire review. You’ll need to obtain 
# that specific review using its file ID and then split it into sentences before rating:
from statistics import mean

def is_positive(review_id: str) -> bool:
    """True if the average of all sentence compound scores is positive."""
    text = nltk.corpus.movie_reviews.raw(review_id)
    scores = [
        sia.polarity_scores(sentence)["compound"]
        for sentence in nltk.sent_tokenize(text)
    ]
    return mean(scores) > 0
# .raw() is another method that exists in most corpora. By specifying a file ID or a list of file IDs, 
# you can obtain specific data from the corpus. Here, you get a single review, then use nltk.sent_tokenize() 
# to obtain a list of sentences from the review. Finally, is_positive() calculates the average compound score 
# for all sentences and associates a positive result with a positive review.
# You can take the opportunity to rate all the reviews and see how accurate VADER is with this setup:
>>> shuffle(all_review_ids)
>>> correct = 0
>>> for review_id in all_review_ids:
...     if is_positive(review_id):
...         if review_id in positive_review_ids:
...             correct += 1
...     else:
...         if review_id in negative_review_ids:
...             correct += 1
...
>>> print(F"{correct / len(all_review_ids):.2%} correct")
64.00% correct


##############################################################################
# SENTIMENT EVALUATION MODEL:
from textblob import TextBlob 
wiki = TextBlob("Python is a high-level, general-purpose programming language.") # creates a blob out of text
# sentiment analysis: 
#The sentiment property returns a named tuple of the form Sentiment(polarity, subjectivity). 
#The polarity score is a float within the range [-1.0, 1.0]. 
#The subjectivity is a float within the range [0.0, 1.0] 
# where 0.0 is very objective and 1.0 is very subjective.

testimonial = TextBlob("Textblob is amazingly simple to use. What great fun!")
testimonial.sentiment
# >> Sentiment(polarity=0.39166666666666666, subjectivity=0.4357142857142857)
testimonial.sentiment.polarity
# >> 0.39166666666666666
testimonial.sentiment.subjectivity

# Ranges:
# ??? FILTER -need or not ?: subjectivity >= 0.5 == to cut off the most objective ones???

# polarity -1<=p<=-0.5 == 'Mood:pretty bad' 'one of those days', 'down', 'upset'
# polarity -0.5<p<=0 == 'Mood: Ok''could be better', 'not the best day', 'need to smile more'
# polarity 0<p<=0.5 == 'Mood: will do' 'not too bad', 'you are really trying despite all', 'nailing it'
# polarity 0.5<p<=1 == 'Mood: feeling great' 'happy', 'in a good mood', 'good to see you smiling'

# WORD -of-the-year/month? noun//verb//adjective 
monty.words.count('ekki') # == non-case-sensitive search
# You can specify whether or not the search should be case-sensitive (default is False):
monty.words.count('ekki', case_sensitive=True)

# Part-of-speech tags can be accessed through the tags property:
wiki.tags
# >> [('Python', 'NNP'), ('is', 'VBZ'), ('a', 'DT'), ('high-level', 'JJ'), ('general-purpose', 'JJ'), ('programming', 'NN'), ('language', 'NN')]

# +++ BRING WordNet - to explain the most popular words:
from textblob import Word
Word("octopus").definitions
# >> ['tentacles of octopus prepared as food', 'bottom-living cephalopod having a soft oval body with eight long tentacles']

#############################################################    



def mood_checker (self):
        #if self.entry_sentiment.subjectivity >= 0.7: # looks into the more subjective sentiments ('me' over 'day')
            #if -1<=self.entry_sentiment.polarity<=-0.7:
                #return ('1', 'me') #== 'Mood: pretty bad', 'Feeling down today? Big hug!', 'Looks like you might be upset about something. Remember, no storm lasts forever.'
            #elif -0.7<self.entry_sentiment.polarity<=-0.4:
                #return ('2', 'me') #== 'Mood: Ok', 'Be optimistic, it can always be worse ;)', 'Prescribing you more self-care and more self-love today!'
            #elif 0.4<self.entry_sentiment.polarity<=0.7:
                #return ('3', 'me') #== 'Mood: not bad' 'You are really trying and it shows!', 'You are nailing it, love!'
            #elif 0.7<self.entry_sentiment.polarity<=1.0:
                #return ('4', 'me') #== 'Mood: feeling great' 'Oh! Someone is in a good mood today?! Happy for you!', 'So good to see you smiling, dear!'
            #else:
                #return ('0','neutral')

        if 0.7<=self.entry_sentiment.subjectivity <= 0.3: # looks into the more objective sentiments ('day' over 'me')
            if -1<=self.entry_sentiment.polarity<=-0.7:
                return ('1', 'emo') #== 'Day: pretty bad' 'Sh*t happens. Tomorrow you'll try again.', 'Some days are genuinely f*cked and cannot be unf*cked, so go home and sleep.'
            elif -0.7<self.entry_sentiment.polarity<=-0.4:
                return ('2', 'emo') #== 'Day: Ok', 'Not the best day? Good news: not the worst either ;)', 'Not every day is a good day. And you know what? That's Ok too.'
            elif 0.4<self.entry_sentiment.polarity<=0.7:
                return ('3', 'emo') #== 'Day: average' 'So, it's not such a bad day, after all?', 'Perhaps, tomorrow will be even better, who knows...'
            elif 0.7<self.entry_sentiment.polarity<=1:
                return ('4', 'emo') #== 'Day: great', 'It's been a fantastic day today. Have many more of those!', 'Looks like you've had a great day. Well done!'
            else:
                return ('0','neutral')
            
        else: #== neutral statements
            return ('0','neutral') #== 'Mood/Day: hard to say' 'Hopefully, all is good, dear?', 'Is everything alright, love?', 'Just some ususal....[day-of-week]', 'Still hope it's agood day for you.'
        

    def entry_reaction (self, entry: Entry): # choosing words of reaction/support to the entry content
        self.entry=entry
        # reactions to a subjective 'me'-entry:
        #me={
            #'1':["Mood evaluation: pretty bad.", "Feeling down today? Big hug!", "Looks like you might be upset about something. Remember, no storm lasts forever."],
            #'2':["Mood evaluation: Ok.", "Be optimistic, it can always be worse ;)", "Prescribing you more self-care and more self-love today!"],
            #'3':["Mood evaluation: not bad.", "You are really trying and it shows!", "You are nailing it, love!"],
            #'4':["Mood evaluation: feeling great.", "Oh! Someone is in a good mood today?! Happy for you!", "So good to see you smiling, dear!"],
            #}
        # reactions to an objective 'day'-entry:
        emo={
            '1':["Mood/Day evaluation: pretty bad." "Sh*t happens. You'll try again tomorrow.", "Some days are genuinely f*cked and cannot be unf*cked, so go home and sleep."],
            '2':["Mood/Day evaluation: Ok.", "Not the best day? Good news: not the worst either ;)", "Not every day is a good day. And you know what? That's Ok too."],
            '3':["Mood/Day evaluation: average.", "So, it's not such a bad day, after all?", "Perhaps, tomorrow will be even better, who knows..."],
            '4':["Mood/Day evaluation: great." "It's been a fantastic day today. Have many more of those!", "Looks like you've had a great day. Well done!"],
            }
        # reactions to a 'neutral' entry:
        neutral=["Mood/Day evaluation: hard to say", "Hopefully, all is good, dear?", "Is everything alright, love?", f"Just some usual {self.entry.entry_date_time.strftime("%A")}, huh?", "Still hope it's a good day for you."]

        #support_words=choice([1,2]) # random choice of reaction phrase from 2 extra options

        #printing the right reaction based on the entry's sentiment value:
        #if self.entry.emo_meter[1]=='me':            
            #x=self.entry.emo_meter[0]
            #print (me[x][0])
            #print (me[x][support_words])


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

##################################################################################### FULL CODE ON BLOB:
##################################################################################### FULL CODE ON BLOB:
##################################################################################### FULL CODE ON BLOB:

# Let's make a simple diary app. 
# In this diary, you can read, add, delete, and modify your entries.  

# Import the necessary tools:
from datetime import datetime, timedelta
from pathlib import Path
from textblob import TextBlob
from random import choice, shuffle
import re
import nltk
nltk.download(["stopwords","twitter_samples","movie_reviews","vader_lexicon","punkt", "punkt_tab"])
from nltk.sentiment import SentimentIntensityAnalyzer
from random import shuffle

###################
#testimonial = TextBlob("Textblob is amazingly simple to use. What great fun!")
#testimonial.sentiment
# >> Sentiment(polarity=0.39166666666666666, subjectivity=0.4357142857142857)
#testimonial.sentiment.polarity
# >> 0.39166666666666666
#testimonial.sentiment.subjectivity
# Ranges:
# ??? FILTER -need or not ?: subjectivity >= 0.5 == to cut off the most objective ones???

# polarity -1<=p<=-0.5 == 'Mood:pretty bad' 'one of those days', 'down', 'upset'
# polarity -0.5<p<=0 == 'Mood: Ok''could be better', 'not the best day', 'need to smile more'
# polarity 0<p<=0.5 == 'Mood: will do' 'not too bad', 'you are really trying despite all', 'nailing it'
# polarity 0.5<p<=1 == 'Mood: feeling great' 'happy', 'in a good mood', 'good to see you smiling'
###################

class Entry: # == the basic unit of the diary list
    def __init__ (self, entry_date_time: datetime, entry_content: str):
        self.entry_date_time=entry_date_time
        self.entry_content=entry_content
        self.entry_sentiment=TextBlob(entry_content).sentiment
        self.emo_meter=self.mood_checker()

    def mood_checker (self):
        if -1<=self.entry_sentiment.polarity<=-0.7:
            return ('1', 'emo') #== 'Day: pretty bad' 'Sh*t happens. Tomorrow you'll try again.', 'Some days are genuinely f*cked and cannot be unf*cked, so go home and sleep.'
        elif -0.7<self.entry_sentiment.polarity<=-0.4:
            return ('2', 'emo') #== 'Day: Ok', 'Not the best day? Good news: not the worst either ;)', 'Not every day is a good day. And you know what? That's Ok too.'
        elif 0.4<self.entry_sentiment.polarity<=0.7:
            return ('3', 'emo') #== 'Day: average' 'So, it's not such a bad day, after all?', 'Perhaps, tomorrow will be even better, who knows...'
        elif 0.7<self.entry_sentiment.polarity<=1:
            return ('4', 'emo') #== 'Day: great', 'It's been a fantastic day today. Have many more of those!', 'Looks like you've had a great day. Well done!'
        else:
            return ('0','neutral')
        
    def __str__(self):
        return f"> {self.entry_date_time.day:02g}.{self.entry_date_time.month:02g}.{self.entry_date_time.year} [{self.entry_date_time.hour:02g}:{self.entry_date_time.minute:02g}:{self.entry_date_time.second:02g}] {self.entry_content}"
    
class Diary(Entry): # == a collection of Entries written into a .txt file
    def __init__ (self, file_name: str):
        self.file_name=file_name
        self.diary_list=[]
        self.entry_list_from_file()

    def entry_list_from_file(self): # == converts .txt file into a list of Entries        
        with open(self.file_name) as my_diary:
            contents=my_diary.read().split('> ')[1:] # splitting its contents by line
        
        for c in contents:    
            c_entry_date_time=datetime.strptime(c.split(']')[0].replace(' [', ' '),"%d.%m.%Y %H:%M:%S") # separate entry's date and convert it into a datetime object
            c_entry_content=c.split(']')[1].strip() # separate entry's date and convert it into a datetime object
            entry_from_c=Entry(c_entry_date_time,c_entry_content)
            self.diary_list.append(entry_from_c)

class Diary_app(Diary): # == interface to manage the Diary and the Entries in it
    def __init__ (self):        
        self.path=self.path_checked()            
        self.__diary=Diary(self.path)
        self.changes=False

    def path_checked(self): # == makes sure the file with such diary name exists
        diary_name=input("What is the name of your diary? ")+'.txt'
        if Path('./'+diary_name).is_file():
            return diary_name
        else:
            print("There is no diary with this name in the current folder.")
            answer=input('Would you like to create a new diary? Type in "Yes" or "No": ')
            if answer.lower()=='yes':
                diary_name=input("Please, enter the name of your new diary: ")+'.txt'
                open(diary_name,'w').close()
                return diary_name
            else:
                self.quit()
        
    def menu(self): # == displays the menu
        print("\nPlease, choose what you want to do:\n0 - exit this app\n1 - add an entry\n2 - read entries for the last few days\n3 - change an entry\n4 - delete an entry")    
        try:
            choice=int(input("\nYour choice: "))
            if choice in [0,1,2,3,4]:
                return choice
        except:        
            print("ValueError: Only numbers listed above are accepted. No letters, symbols, or extra spaces")
    
    def file_update(self): # == overwrites the txt file
        if self.changes==True:
            with open(self.__diary.file_name, "w") as diary_file:
                for e in self.__diary.diary_list:  
                    diary_file.write(f"\n> {e.entry_date_time.strftime("%d.%m.%Y [%H:%M:%S]")} {e.entry_content}") 
    
    def date_check(self, given_str: str): # == checks that the input DATE is legit
        try:
            re.search(r'\d{2}\.\d{2}\.\d{4}', given_str)
            datetime.strptime(given_str,"%d.%m.%Y")
            return True
        except:
            print("Invalid date! Please, type in a valid date. Check the format >> dd.mm.yyyy")
            return False
    
    def time_check(self, given_str: str): # check that the input TIME is legit 
        try:
            re.search(r'\d{2}\:\d{2}\:\d{2}', given_str)
            datetime.strptime(given_str,'%H:%M:%S')
            return True
        except:
            print("Invalid time! Please, type in a valid time. Check the format >> hh:mm:ss")
            return False
        
    def find_entry (self): # checks that the ENTRY EXISTS in the diary
        while True:
            old_entry_date=input("Entry's date (dd.mm.yyyy): ").strip()
            if self.date_check(old_entry_date):
                break
            else:
                continue
        while True:
            old_entry_time=input("Entry's time: (hh:mm:ss) ").strip()
            if self.time_check(old_entry_time):
                break
            else:
                continue

        old_entry_date_time=datetime.strptime(f"{old_entry_date} {old_entry_time}",'%d.%m.%Y %H:%M:%S')

        for e in self.__diary.diary_list:
            if e.entry_date_time == old_entry_date_time:
                return e

    def entry_reaction (self, entry: Entry): # choosing words of reaction/support to the entry content
        self.entry=entry
        # reactions to an entry:
        emo={
            '1':["Mood/Day evaluation: pretty bad." "Sh*t happens. You'll try again tomorrow.", "Some days are genuinely f*cked and cannot be unf*cked, so go home and sleep."],
            '2':["Mood/Day evaluation: Ok.", "Not the best day? Good news: not the worst either ;)", "Not every day is a good day. And you know what? That's Ok too."],
            '3':["Mood/Day evaluation: average.", "So, it's not such a bad day, after all?", "Perhaps, tomorrow will be even better, who knows..."],
            '4':["Mood/Day evaluation: great." "It's been a fantastic day today. Have many more of those!", "Looks like you've had a great day. Well done!"],
            }
        # reactions to a 'neutral' entry:
        neutral=["Mood/Day evaluation: hard to say", "Hopefully, all is good, dear?", "Is everything alright, love?", f"Just some usual {self.entry.entry_date_time.strftime("%A")}, huh?", "Still hope it's a good day for you."]

        if self.entry.emo_meter[1]=='emo':
            x=self.entry.emo_meter[0]
            print (emo[x][0])
            print (choice(emo[x][1:]))

        elif self.entry.emo_meter[1]=='neutral':
            x=self.entry.emo_meter[0]
            print (neutral[0])
            print (choice(neutral[1:]))

        else:
            raise ValueError('Something is wrong with the "emo_meter" tuple!') ### DELETE???

    # When you EXIT the app (==0):
    def quit(self):
        print("Alright, till next time then, bye!")
        quit()
          
    # To ADD an entry (==1):
    def new_entry(self):
        notes=input("Diary entry: ")        
        #diary_entry=Entry(new_entry_time, notes)
        diary_entry=Entry(datetime.now(), notes)
        self.__diary.diary_list.append(diary_entry)
        self.changes=True
        print("Your diary entry was added:")
        print(diary_entry)
        self.entry_reaction(diary_entry)

    # To READ entries for the last N days (==2):
    def read_entries(self):
        n_days=int(input("How many days of your diary entries would you like to read? "))
        n_days_ago=datetime.now()-timedelta(days=n_days)
        count=0

        print(f"\nEntries for the last {n_days} days ({n_days_ago.strftime("%d.%m.%Y")} - {datetime.now().strftime("%d.%m.%Y")}):")       
        for e in self.__diary.diary_list:                   
            if e.entry_date_time >= n_days_ago: # check if the entry was written within the last N days
                count += 1
                print(e)

        day_pl = lambda a: ('day' if str(a)[-1]=='1' and a!=11 else 'days')
        entry_pl = lambda a: ('entry' if str(a)[-1]=='1' and a!=11 else 'entries')
        print(f"\n[Overall, you've had {count} {entry_pl(count)} in the last {n_days} {day_pl(n_days)}]")

    # To CHANGE an entry - based on its time&date (==3):
    def change_entry(self):
        print("Please specify below, which entry you wish to change")
        entry=self.find_entry()
        if entry == None:
            print("You have entered valid date and time, but there is no diary entry matching them")
        else:
            changed_entry_content=input("Please, type new content for this entry: ")
            entry.entry_content=changed_entry_content
            self.changes=True
            print("The entry was changed")

    # To DELETE an entry - based on its time&date (==4):
    def delete_entry(self):
        print("Please specify below, which entry you wish to delete")
        entry=self.find_entry()
        if entry == None:
            print("You have entered valid date and time, but there is no diary entry matching them")
        else:
            self.__diary.diary_list.remove(entry)
            self.changes=True
            print("The entry was removed")

    def execute(self):
        # MAIN LOOP:
        while True:
            self.file_update()       
            menu=self.menu()
            
            # To quit:
            if menu==0:
                self.quit()
                break

            # To add an entry:
            if menu==1:
                self.new_entry()
                
            # To read entries for the last N days:
            if menu==2:
                self.read_entries()

            # To change an entry:    
            if menu==3:
                self.change_entry()

            # To delete an entry:    
            if menu==4:
                self.delete_entry()      

# to RUN the app:
app=Diary_app()
app.execute()


#############################################################
# SENTIMENT EVALUATION MODEL:

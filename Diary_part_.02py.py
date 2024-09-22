''' 
PROJECT: EmoDiary /STUDENT: Darina Bunak /COURSE: Programming //Professional Diploma in Data Analytics and Finnish Language 2024

1. IDEA >>>   This is a simple diary app meant to evaluate user's emotional dynamics over time and provide some daily support.
2. SOLUTION >>>   The sentiment analysis of the entries is based on NLTK modules and a txt-file, where the data is stored.
    The code is based on objects of custom classes. Analytical part uses pandas for speed and reliability.
    Collecting mood evaluation grades provided by user shall help calibrate sentiment analysis and improve auto-evaluation in the future.
3. FUNCTIONALITY >>>  Start = RUN. Exit = '0', Ctrl+C. User can: add an entry, read entries for several days, check stats on language, check stats on moods.
4. COMMENTS >>>   Although NLTK is widely recommended for language and sentiment analysis, in this case, it shows very poor reliability.
    Its basic built-in functions, e.g. tagging, raise a lot of questions. Part-of-speech evaluation is too often incorrect. 
    So is sentiment evaluation (I tried to adjust 'manually' but still pretty poor results). Despite the flaws, I decided to keep it for now 
    (too much time spent already) and replace it with a better module (e.g.BERT) later. So, expect strange results when choosing '3'.
5. TESTING >>> When prompted, use file name 'TEST' (file TEST.txt attached)
'''

streamlit run https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/master/streamlit_app.py

### Import the necessary tools:
#pip install --user -U nltk # << unhash for the very first time
from datetime import datetime, timedelta
from pathlib import Path
from random import choice, shuffle
import re
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import RegexpTokenizer
nltk.download(["stopwords","twitter_samples","movie_reviews","vader_lexicon","punkt", "punkt_tab", "averaged_perceptron_tagger_eng"]) # << unhash for the very first time

### Code:
class Entry: ### == the basic unit of the diary list
    def __init__ (self, entry_date_time: datetime, entry_content: str, emo_meter=None, emo_grade=None):
        self.entry_date_time=entry_date_time
        self.entry_content=entry_content
        self.emo_meter=emo_meter # auto-evaluated sentiment
        self.emo_grade=emo_grade # sentiment grade given by user

        if self.emo_meter==None:
            self.emo_meter = self.mood_checker() # assigns mood grades to distribute responses

    def mood_checker (self): # Hope to replace its content by a better evaluation model in the future without too much redo        
        sia = SentimentIntensityAnalyzer()
        self.entry_sentiment=sia.polarity_scores(self.entry_content) # objective evaluation of entry sentiment values by Vader
        # self.entry_sentiment is a dict, eg: {'neg': 0.0, 'neu': 0.295, 'pos': 0.705, 'compound': 0.8012} 
        # usually sentence's sentiment is evaluated by 'compound' returned (cp): if cp>0 ==>pos, if cp<0 ==> neg
        # this simple approach did not work on my own entries, so I tried to adjust it a bit, based on my conclusions (still not too good):

        if self.entry_sentiment['neu']>=0.6:
            if self.entry_sentiment['pos']<0.05:
                return '0-29' # Mood/Day: bad
            else:
                return '30-70' # Mood/Day: average
        else:
            if self.entry_sentiment['compound']<-0.5:
                if self.entry_sentiment['pos']>0.00:
                    return '30-70' # Mood/Day: average
                else:
                    return '0-29' # Mood/Day: bad
            if self.entry_sentiment['compound']>0.5:
                return '71-100' # Mood/Day: good    
            else:
                if self.entry_sentiment['neg']>0.4:
                    return '0-29' # Mood/Day: bad
                else:
                    return '30-70' # Mood/Day: averag  
       
    def __str__(self):        
        return f"> {self.entry_date_time.day:02g}.{self.entry_date_time.month:02g}.{self.entry_date_time.year} [{self.entry_date_time.hour:02g}:{self.entry_date_time.minute:02g}:{self.entry_date_time.second:02g}] {self.entry_content}"
        #for testing==includes both evaluation scores:
        #return f"> {self.entry_date_time.day:02g}.{self.entry_date_time.month:02g}.{self.entry_date_time.year} [{self.entry_date_time.hour:02g}:{self.entry_date_time.minute:02g}:{self.entry_date_time.second:02g}] {self.entry_content} (auto-grade: {self.emo_meter}, user-grade: {self.emo_grade})"    

class Diary(Entry): ### == a collection of Entries written into a .txt file
    def __init__ (self, file_name: str):
        self.file_name=file_name
        self.diary_list=[]
        self.entry_list_from_file()

    def entry_list_from_file(self): ### == converts .txt file into a list of Entries        
        with open(self.file_name) as my_diary:
            contents=my_diary.read().split('> ')[1:] # splitting contents by line
        
            for c in contents: 
                d=c.split(']')[0].split(' [')[0]
                t=c.split(']')[0].split(' [')[1]
                if self.date_check(d) and self.time_check(t):

                    c_entry_date_time=datetime.strptime(c.split(']')[0].replace(' [', ' '),"%d.%m.%Y %H:%M:%S") # separate entry's date and convert it into a datetime object
                    c_entry=c.split(']')[1]

                    find_01=re.search('\(auto\-grade\: ',c_entry)
                    find_02=re.search(', user\-grade\: ',c_entry)
                    find_03=re.search('user\-grade\: .*\)',c_entry)

                    c_entry_content=c_entry[:find_01.start()].strip()       
                    c_entry_emo_meter=c_entry[find_01.end():find_02.start()].strip()
                    c_entry_emo_grade=c_entry[find_02.end():find_03.end()-1].strip()

                    entry_from_c=Entry(c_entry_date_time,c_entry_content,c_entry_emo_meter,c_entry_emo_grade)
                    self.diary_list.append(entry_from_c)
                else:
                    raise ValueError (f"Invalid date: '{d}' or time: {t}. File '{self.file_name}' was corrupted!")

    def date_check(self, given_str: str): ### ==checks that the input DATE is legit
        re.search(r'\d{2}\.\d{2}\.\d{4}', given_str)
        try:
            datetime.strptime(given_str,"%d.%m.%Y")
            return True
        except ValueError:
            return False
    
    def time_check(self, given_str: str): ### == checks that the input TIME is legit 
        re.search(r'\d{2}\:\d{2}\:\d{2}', given_str)
        try:
            datetime.strptime(given_str,'%H:%M:%S')
            return True
        except ValueError:
            return False

class Diary_app(Diary): ### == interface to manage the Diary and the Entries in it
    def __init__ (self):        
        self.path=self.path_checked()            
        self.__diary=Diary(self.path)
        self.changes=False

    def path_checked(self): #### == makes sure the file with such diary name exists
        diary_name=input("Hi! Welcome to EmoNotes. What is the name of your diary? ")+'.txt'
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
        
    def menu(self): ### == displays the menu
        print()
        print("Please, choose what you want to do:\n0 - exit this app\n1 - add an entry\n2 - read entries for the last few days\n3 - check stats on your language\n4 - check stats on your moods")    
        try:
            choice=int(input("\nYour choice: "))
            if choice in [0,1,2,3,4]:
                return choice
        except:        
            print("ValueError: Only numbers listed above are accepted. No letters, symbols, or extra spaces")
    
    def file_update(self): ### == overwrites the .txt file
        if self.changes==True:
            with open(self.__diary.file_name, "w") as diary_file:
                for e in self.__diary.diary_list:  
                    diary_file.write(f"\n> {e.entry_date_time.strftime("%d.%m.%Y [%H:%M:%S]")} {e.entry_content} (auto-grade: {e.emo_meter}, user-grade: {e.emo_grade})")  
  
    def check_entry(self): ### checks if the new entry is correct, otherwise changes it
        notes=input("How have you been today? Write about your feelings and events here: ") 
        print("\nYou won't be able to change this entry later, so please read it carefully now: ")
        print(notes)
        while True:
            checked=input("\nIf everything is alright >> press ENTER.\nIf not >> type in the NEW VERSION: ")
            if checked != '':
                print(f'New version: {checked}')
                notes=checked
                pass                
            else:
                break
        return notes
        
    def entry_reaction (self, entry: Entry): ### == chooses words of support based on automatic mood evaluation
        self.entry=entry
        
        emo={     # all possible support-reactions to an entry
            '0-29':["Looks like it's not the best day ever?", 
                 "Sh*t happens. You'll try again tomorrow.", 
                 "As a wise man said...Some days are genuinely f*cked and cannot be unf*cked, so go home and sleep.", 
                 "Big HUG!", 
                 "Remember, no storm lasts forever.", 
                 "Good news: not the worst either ;)", 
                 "Not every day is a good day. And you know what? That's Ok too.", 
                 "Be optimistic, it can always be worse ;)", 
                 "Prescribing you more self-care and more self-love today!"],

            '30-70':[f"Perhaps, you think it's been just an average {self.entry.entry_date_time.strftime("%A")}, but" , 
                  "objectively speaking, all is good, right? ;)", 
                  "think of all the bad things that did not happen today. See how lucky you are?", 
                  "you are really trying and it shows!", 
                  "in fact, you are nailing it, love!"],
            '71-100':["It seems you've had a pretty good day.", 
                   "Congrats! Keep going!", 
                   "Be proud of yourself!", 
                   "Tomorrow might be even better!", 
                   "Have many more of them!", 
                   "Well done!", 
                   "I'm so happy for you!", 
                   "So good to see you smiling, dear!"],
            }

        # printing one of the above:
        x=self.entry.emo_meter
        print (f"{emo[x][0]} {choice(emo[x][1:])}")

        # asking the user to evaluate their day themselves >> to use the grade in training this evaluation model in the future:
        while self.entry.emo_grade==None:
            grade=input("How do you rate this day yourself? Give it a score from 0 to 100: ")
            if grade.isdigit() and 0<=int(grade)<=100:
                self.entry.emo_grade=grade
                break
            else:
                print("Please, enter a number from 0 to 100")
        
        # brief assessment of the accuracy:
        by_user=int(self.entry.emo_grade)
        by_app=self.entry.emo_meter
        print(f'My guess was: {by_app}.')
        if (by_user<30 and by_app=='0-29') or (30<=by_user<=70 and by_app=='30-70') or (by_user>70 and by_app=='71-100'):
            print('So, I guessed correctly.\nThank you!')
        else:
            print('I see that I was wrong. Your rate will help me guess better in the future.\nThank you! ')

    ### TO EXIT the app (==0):
    def quit(self):
        print("See you soon, bye!")
        quit()
          
    ### TO ADD an entry (==1):
    def new_entry(self):
        diary_entry=Entry(datetime.now(), self.check_entry()) # datetime.now((tz=None))
        self.__diary.diary_list.append(diary_entry)
        self.changes=True
        print("\nThe entry you added:")
        print(diary_entry)
        self.entry_reaction(diary_entry)

    ### TO READ entries for the last N days (==2):
    def read_entries(self):
        stat=self.stat('your diary entries')
        df=stat[0]
        days=stat[1]

        df['entry_date'] = pd.to_datetime(df['entry_date'], format='%Y-%m-%d').dt.strftime('%d.%m.%Y') # converting the dates into str
        df['entry_time'] = pd.to_datetime(df['entry_time'],format='%H:%M:%S').dt.strftime('%H:%M:%S') # converting the times into str

        print() # had to use strings to print nicely
        for e in range (0,df.shape[0]):
            print(f'> {df.iloc[e,0]} [{df.iloc[e,1]}] {df.iloc[e,2]}')
            
        day_pl = lambda a: ('day' if str(a)[-1]=='1' and a!=11 else 'days')
        entry_pl = lambda a: ('entry' if str(a)[-1]=='1' and a!=11 else 'entries')
        print(f"\n[Overall, you've had {df.shape[0] } {entry_pl(df.shape[0] )} in the last {days} {day_pl(days)}]")
    
    def stat (self, str_patch='statistics'):    # creating a dataframe for statistics
        self.str_patch=str_patch
        data=[[e.entry_date_time.date(), e.entry_date_time.time().replace(microsecond=0), (e.entry_content+" "), e.emo_meter,int(e.emo_grade)] for e in self.__diary.diary_list]
        df = pd.DataFrame(data, columns=['entry_date', 'entry_time', 'entry_content', 'emo_meter', 'emo_grade'])

        nn=(datetime.now().date()-df.loc[0,'entry_date']).days # how many days ago the diary started
        nn+=1 # including today (e.g. if diary started 4 days ago > you have 5 days to see: 4 days + today)
        print(f"\nToday is day {nn} of your diary.")
        n_days=int(input(f"How many days of {str_patch} do you want to see? Please, give a number: "))
        while n_days>nn:
            n_days=int(input(print(f"That's too many days. Your diary started only {nn} days ago\nPlease, give a realistic number: ")))

        start_date=datetime.now().date()-timedelta(days=n_days)
        df_stat=df[df['entry_date'] > start_date]
        return df_stat, n_days

    ### TO SEE STATISTICS - LANGUAGE (==3):   
    def stat_lang(self):
        stat=self.stat()
        df=stat[0]
        days=stat[1]
        words = df['entry_content'].sum()

        tokenizer = RegexpTokenizer(r'\w+')
        stop_words = stopwords.words('english')
        all_words=[w.lower() for w in tokenizer.tokenize(words) if not w.lower() in stop_words] # tockenizing (=dividing word-by-word) + lowering case

        all_tags = nltk.pos_tag(all_words) # tagging ==> list of tuples (word, part of speech)    
        value_tockens=[['NN','NNS'],['VB','VBZ','VBP','VBN','VBG','VBD'],['JJ','JJR','JJS'],['RB','RBR','RBS'],['UH']] # parts of speech to be used: tags
        value_dfs=['nouns','verbs','adjectives','adverbs','interjections'] # parts of speech to be used: names
        value_tags=[tag for tag in all_tags if (tag[1] in sum(value_tockens,[]) and len(tag[0])>2)] # filtering useful tuples from all tags
        tagged_df=pd.DataFrame(value_tags, columns=['word','tag']) # converting the list of useful tags into a df      
        
        print(f'\nLanguage statistics for {days} days (main parts of speech)')
        print()

        # printing by part-of-speech, separately:
        for x in range(0,len(value_dfs)):
            y=tagged_df[tagged_df['tag'].isin(value_tockens[x])] # creating a dedicated df (eg 'nonuns')
            print(f'{value_dfs[x].capitalize()}: {y.shape[0]}. ',end='') 
            if y.shape[0] != 0:
                print(f'Top-5 {value_dfs[x]}: ',end='')
                y_top5=y.groupby(['word']).size().reset_index(name='count').sort_values(by='count', ascending=False).head(5) # sorting words by nr of repetitions, cutting top-5
                print(*y_top5['word'].values.tolist(), sep = ", ")
            else:
                pass
        print()
    
    ### TO SEE STATISTICS - MOOD (==4):
    def stat_mood(self): #return df_stat, n_days
        df_days = self.stat()
        df=df_days[0] # columns=['entry_date', 'entry_time', 'entry_content', 'emo_meter', 'emo_grade']
        days=df_days[1]

        print()
        print(f'MOOD STATS for the last {days} days (based on your own assessment)')
        print(f'\na) Average mood grade - for the requested period: {df['emo_grade'].mean()}')
        print(f'\nb) Same, by day-of-week:')

        df['entry_date'] = pd.to_datetime(df['entry_date'], format='%Y-%m-%d') # converting the dates to pandas datetime objects
        df['entry_time'] = pd.to_datetime(df['entry_time'],format='%H:%M:%S') # converting the times to pandas datetime objects
        df['day_of_week'] = df['entry_date'].dt.day_name() # adding a new column to store the day of the week
        days=df[['day_of_week','emo_grade']].groupby(['day_of_week'],observed=False).mean().reset_index().sort_values(by='emo_grade', ascending=False)
        print(days.to_string(header=False, index=False))

        print(f'\nc) Same, by time-of-day:') 
        df['time_of_day'] = df['entry_time'].dt.hour # converting the times to pandas datetime objects 
        df['time_of_day']=pd.cut(x=df['time_of_day'], bins=[0,6,12,18,24],right=False, labels=['night (00:00-05:59)','morning (06:00-11:59)','day (12:00-17:59)','evening (18:00-23:59)'])        
        print(df[['time_of_day','emo_grade']].groupby(['time_of_day'],observed=False).mean().reset_index().sort_values(by='emo_grade', ascending=False).reindex(columns=['emo_grade','time_of_day']).replace(np.nan,'-',regex = True).to_string(header=False, index=False))

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

            # To see language statistics:    
            if menu==3:
                self.stat_lang()

            # To see mood statistics:    
            if menu==4:
                self.stat_mood() 

### to RUN the app:
app=Diary_app()
app.execute()
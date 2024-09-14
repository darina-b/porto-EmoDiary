# Let's make a simple diary app. 
# In this diary, you can read, add, delete, and modify your entries.  

# Import the necessary tools:
############################
from datetime import datetime, timedelta
from pathlib import Path
#### from textblob import TextBlob
from random import choice, shuffle
import re
import pandas as pd
import nltk
#nltk.download(["stopwords","twitter_samples","movie_reviews","vader_lexicon","punkt", "punkt_tab", "averaged_perceptron_tagger_eng"]) ### UNCOMMENT for the FIRST TIME!
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import RegexpTokenizer

class Entry: # == the basic unit of the diary list
    def __init__ (self, entry_date_time: datetime, entry_content: str, emo_meter=None, emo_grade=None):
        self.entry_date_time=entry_date_time
        self.entry_content=entry_content
        self.emo_meter=emo_meter # evaluated sentiment
        self.emo_grade=emo_grade # sentiment grade given by user

        if self.emo_meter==None:
            self.emo_meter = self.mood_checker() # assigns mood grades to distribute responses

    def mood_checker (self): # Hope to replace its content by a better evaluation model in the future without too much redo
        sia = SentimentIntensityAnalyzer()
        self.entry_sentiment=sia.polarity_scores(self.entry_content) # objective evaluation of entry sentiment values by Vader
        # self.entry_sentiment is a dict, eg: {'neg': 0.0, 'neu': 0.295, 'pos': 0.705, 'compound': 0.8012} 
        # usually sentence's sentiment is evaluated by 'compound' returned (cp): if cp>0 ==>pos, if cp<0 ==> neg
        # this simple approach did not work on my own entries, so I <tried> to adjust it a bit, based on my conclusions (still not too good)

        if self.entry_sentiment['neu']>=0.6:
            if self.entry_sentiment['pos']<0.05:
                return '0-29' #== Mood/Day: bad
            else:
                return '30-70' #== Mood/Day: average
        else:
            if self.entry_sentiment['compound']<-0.5:
                if self.entry_sentiment['pos']>0.00:
                    return '30-70' #== Mood/Day: average
                else:
                    return '0-29' #== Mood/Day: bad
            if self.entry_sentiment['compound']>0.5:
                return '71-100' #== Mood/Day: good    
            else:
                if self.entry_sentiment['neg']>0.4:
                    return '0-29' #== Mood/Day: bad
                else:
                    return '30-70' #== Mood/Day: averag  
       
    def __str__(self):
        # below is __str__ for checking (incl evaluation scores):
        return f"> {self.entry_date_time.day:02g}.{self.entry_date_time.month:02g}.{self.entry_date_time.year} [{self.entry_date_time.hour:02g}:{self.entry_date_time.minute:02g}:{self.entry_date_time.second:02g}] {self.entry_content} (auto-grade: {self.emo_meter}, user-grade: {self.emo_grade})"
        #return f"> {self.entry_date_time.day:02g}.{self.entry_date_time.month:02g}.{self.entry_date_time.year} [{self.entry_date_time.hour:02g}:{self.entry_date_time.minute:02g}:{self.entry_date_time.second:02g}] {self.entry_content}"
    
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
            c_entry=c.split(']')[1]

            find_01=re.search('\(auto\-grade\: ',c_entry)
            find_02=re.search(', user\-grade\: ',c_entry)
            find_03=re.search('user\-grade\: .*\)',c_entry)

            c_entry_content=c_entry[:find_01.start()].strip() # separate entry's content            
            c_entry_emo_meter=c_entry[find_01.end():find_02.start()].strip()
            c_entry_emo_grade=c_entry[find_02.end():find_03.end()-1].strip()

            entry_from_c=Entry(c_entry_date_time,c_entry_content,c_entry_emo_meter,c_entry_emo_grade)
            self.diary_list.append(entry_from_c)

class Diary_app(Diary): # == interface to manage the Diary and the Entries in it
    def __init__ (self):        
        self.path=self.path_checked()            
        self.__diary=Diary(self.path)
        self.changes=False

    def path_checked(self): # == makes sure the file with such diary name exists
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
        
    def menu(self): # == displays the menu
        print("\nPlease, choose what you want to do:\n0 - exit this app\n1 - add an entry\n2 - read entries for the last few days\n3 - check stats on your language\n4 - check stats on your moods")    
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
                    diary_file.write(f"\n> {e.entry_date_time.strftime("%d.%m.%Y [%H:%M:%S]")} {e.entry_content} (auto-grade: {e.emo_meter}, user-grade: {e.emo_grade})") 
    
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
        
    ###def find_entry (self): # checks that the ENTRY EXISTS in the diary
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
   
    def check_entry(self): # checking if the new entry is correct, otherwise changing it:    >>>>>>>>>>>>>>>>>>>>>>>> ADD A LOOP!!!!
        notes=input("How have you been today? Write about your feelings and events here: ") 
        print("\nYou won't be able to change this entry later, so please read it carefully now:")
        print(f'"{notes}"')
        checked=input("\nIf everything is alright >> press Enter.\nIf not >> type in the new version:")
        if checked == '':
            return notes
        else:
            return checked
        
    def entry_reaction (self, entry: Entry): # choosing words of reaction/support to the entry content based on automatic evaluation
        self.entry=entry

        # all possible support-reactions to an entry:
        emo={
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

        # Printing one of the above:
        x=self.entry.emo_meter
        #print(self.entry.entry_sentiment) ### DELETE AFTER!!!
        #print(x)  ### DELETE AFTER!!!
        print (f"{emo[x][0]} {choice(emo[x][1:])}")

        # Asking the user to evaluate their day themselves >> to use the grade in training this evaluation model in the future:
        while self.entry.emo_grade==None:
            grade=input("How do you rate this day yourself? Give it a score from 0 to 100: ")
            if grade.isdigit() and 0<=int(grade)<=100:
                self.entry.emo_grade=grade
                break
            else:
                print("Please, enter a number from 0 to 100")
        
        # Brief assessment of the accuracy:
        by_user=int(self.entry.emo_grade)
        by_app=self.entry.emo_meter
        print(f'My guess was: {by_app}.')
        if (by_user<30 and by_app=='0-29') or (30<=by_user<=70 and by_app=='30-70') or (by_user>70 and by_app=='71-100'):
            print('So, I guessed correctly.\nThank you!')
        else:
            print('I see that I was wrong. Your rate will help me guess better in the future.\nThank you! ')

    # When you EXIT the app (==0):
    def quit(self):
        print("See you soon, bye!")
        quit()
          
    # To ADD an entry (==1):
    def new_entry(self):
        #notes=input("Diary entry: ")  
        diary_entry=Entry(datetime.now(), self.check_entry()) # datetime.now((tz=None))
        self.__diary.diary_list.append(diary_entry)
        self.changes=True
        print("\nThe entry you added:")
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

    # creating a dataframe for statistics:
    def stat (self):
        data=[[e.entry_date_time.date(), e.entry_date_time.time().replace(microsecond=0), (e.entry_content+" "), e.emo_meter,int(e.emo_grade)] for e in self.__diary.diary_list]
        df = pd.DataFrame(data, columns=['entry_date', 'entry_time', 'entry_content', 'emo_meter', 'emo_grade'])
        #print(df)

        nn=(datetime.now().date()-df.loc[0,'entry_date']).days # how many days ago the diary started
        print(f"\nYou diary started {nn} days ago.")
        n_days=int(input("For HOW MANY DAYS do you want to see statistics? Please, give a number: "))

        while n_days>nn:
            n_days=int(input(print(f"That's too many days. Your diary started only {nn} days ago\nPlease, give a realistic number: ")))

        start_date=datetime.now().date()-timedelta(days=n_days)
        #print(start_date)
        df_stat=df[df['entry_date'] > start_date]
        #print(df_stat)
        return df_stat, n_days

    # STATISTICS - LANGUAGE (==3):   
    def stat_lang(self):
        stat=self.stat()
        df=stat[0]
        days=stat[1]
        words = df['entry_content'].sum()

        tokenizer = RegexpTokenizer(r'\w+')
        all_words=[i.lower() for i in tokenizer.tokenize(words)] # tockenizing + lowering case
        
        value_tockens=[['NN', 'NNS'], ['VB', 'VBZ', 'VBP', 'VBN', 'VBG', 'VBD'], ['JJ', 'JJR', 'JJS'], ['RB', 'RBR', 'RBS'],['UH']]
        #value_tockens=['NN', 'NNS', 'VB', 'VBZ', 'VBP', 'VBN', 'VBG', 'VBD', 'JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS', 'UH']

        #extracting:
        all_tags = nltk.pos_tag(all_words)
        print(all_tags)
        value_tags=[tag for tag in all_tags if tag[1] in sum(value_tockens,[])]
        print(value_tags)
        tagged_df=pd.DataFrame(all_tags, columns=['word','tag']) # converting the list of low-case tockens into a DF
        
        #print(tagged_df)
        tagged_df['count'] = 1
        tagged_df = tagged_df.groupby(['word','tag'])['count'].count().reset_index()
        print(tagged_df.head(10))
        print(tagged_df.sort_values(by='count', ascending=False).head(3))
        #sorted_df=pd.DataFrame(all_tags, columns=['word','tag','count'])

        nouns_df= tagged_df[tagged_df['tag'].isin(value_tockens[0])] 
        verbs_df= tagged_df[tagged_df['tag'].isin(value_tockens[1])] 
        adjectives_df= tagged_df[tagged_df['tag'].isin(value_tockens[2])]
        adverbs_df= tagged_df[tagged_df['tag'].isin(value_tockens[3])]
        interjections_df= tagged_df[tagged_df['tag'].isin(value_tockens[4])]

        #all_valuable=nouns+verbs+adjectives+adverbs+interjections
        #print(all_valuable)
        #nr1_word=all_valuable.most_common(1) # returns a list of n(==1) most common elements

        nr1_noun=nouns.most_common(1)
        nr1_verb=verbs.most_common(1)
        nr1_adjective=adjectives.most_common(1)
        nr1_adverb=adverbs.most_common(1)
        nr1_interjection=interjections.most_common(1)

        print(f'Days included in analysis: {days}')
        #print(f'The word you used most (apat from auxiliary parts of speech): {nr1_word}')
        print('\nIn this time period, the most used words were (by part of speech):')
        print(f'Noun: {nr1_noun[0]}, used {nr1_noun[1]} times')
        print(f'Verb: {nr1_verb[0]}, used {nr1_verb[1]} times')
        print(f'Adjective: {nr1_adjective[0]}, used {nr1_adjective[1]} times')
        print(f'Adverb: {nr1_adverb[0]}, used {nr1_adverb[1]} times')
        print(f'Interjection: {nr1_interjection[0]}, used {nr1_interjection[1]} times')

        #sum_row = df.iloc[0].sum(axis=0)
        #entry_from_c=Entry(c_entry_date_time,c_entry_content,c_entry_emo_meter,c_entry_emo_grade)
        #self.diary_list.append(entry_from_c)

        #df = pd.read_csv("data.txt", sep="\s+", header = None, names=['Name', 'Age', 'Height'])
        #train_df = pd.read_txt('../input/imdb-dataset-sentiment-analysis-in-csv-format/Train.csv').head(4000)

        #return f"> {self.entry_date_time.day:02g}.{self.entry_date_time.month:02g}.{self.entry_date_time.year} [{self.entry_date_time.hour:02g}:{self.entry_date_time.minute:02g}:{self.entry_date_time.second:02g}] {self.entry_content} (auto-grade: {self.emo_meter}, user-grade: {self.emo_grade})"
        #return f"> {self.entry_date_time.day:02g}.{self.entry_date_time.month:02g}.{self.entry_date_time.year} [{self.entry_date_time.hour:02g}:{self.entry_date_time.minute:02g}:{self.entry_date_time.second:02g}] {self.entry_content}"
    
        #start_date=start_date.strftime("%Y-%m-%d")
        #rslt_df = dataframe[dataframe['Percentage'] > 70] 
        #holiday = ['1 January 2018','26 January 2018','2 March 2018','30 March 2018']
        #df.query('date==@holiday')

    # STATISTICS - MOOD (==4):
    #def stat_mood(self):
        #df = self.stat()


####################################################### OLD STUFF ################################################################################
    #def delete_entry(self):
        #print("Please specify below, which entry you wish to delete")
        #entry=self.find_entry()
        #if entry == None:
            #print("You have entered valid date and time, but there is no diary entry searching them")
        #else:
            #self.__diary.diary_list.remove(entry)
            #self.changes=True
            #print("The entry was removed")
##################################################################################################################################################




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
                self.stat()

            # To see mood statistics:    
            if menu==4:
                self.stat_lang() 

# to RUN the app:
app=Diary_app()
app.execute()

#############################################################
# SENTIMENT EVALUATION MODEL:

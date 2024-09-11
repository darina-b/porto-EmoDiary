# Let's make a simple diary app. 
# In this diary, you can read, add, delete, and modify your entries.  

# Import the necessary tools:
############################
from datetime import datetime, timedelta
from pathlib import Path
#### from textblob import TextBlob
from random import choice, shuffle
import re
import nltk
# nltk.download(["stopwords","twitter_samples","movie_reviews","vader_lexicon","punkt", "punkt_tab"])
from nltk.sentiment import SentimentIntensityAnalyzer

###################
# Ranges:
# ??? FILTER -need or not ?: subjectivity >= 0.5 == to cut off the most objective ones???

# polarity -1<=p<=-0.5 == 'Mood:pretty bad' 'one of those days', 'down', 'upset'
# polarity -0.5<p<=0 == 'Mood: Ok''could be better', 'not the best day', 'need to smile more'
# polarity 0<p<=0.5 == 'Mood: will do' 'not too bad', 'you are really trying despite all', 'nailing it'
# polarity 0.5<p<=1 == 'Mood: feeling great' 'happy', 'in a good mood', 'good to see you smiling'
###################

class Entry: # == the basic unit of the diary list
    def __init__ (self, entry_date_time: datetime, entry_content: str, emo_meter=None, emo_grade=None):
        self.entry_date_time=entry_date_time
        self.entry_content=entry_content
        self.emo_meter=emo_meter
        self.emo_grade=emo_grade

# the line above returns a dict: {'neg': 0.0, 'neu': 0.295, 'pos': 0.705, 'compound': 0.8012}
# You’ll get back a dictionary of different scores. The negative, neutral, and positive scores are related: 
# They all add up to 1 and can’t be negative. The compound score is calculated differently. 
# It’s not just an average, and it can range from -1 to 1.
### PLAY WITH EVALUATION!!!! ###:
        if self.emo_meter==None:
            self.emo_meter = self.mood_checker() # assigns mood grades to distribute responses
    def mood_checker (self):
        sia = SentimentIntensityAnalyzer()
        self.entry_sentiment=sia.polarity_scores(self.entry_content) # objective evaluation of entry sentiment values by Vader
        # self.entry_sentiment is a dict, eg: {'neg': 0.0, 'neu': 0.295, 'pos': 0.705, 'compound': 0.8012} 
        # usually sentence's sentiment is evaluated by 'compound' returned (cp): if cp>0 ==>pos, if cp<0 ==> neg

        if self.entry_sentiment['neu']>=0.6:
            if self.entry_sentiment['pos']<0.05:
                return '0' #== Mood/Day: bad
            else:
                return '50' #== Mood/Day: average
        else:
            if self.entry_sentiment['compound']<-0.5:
                if self.entry_sentiment['pos']>0.00:
                    return '50' #== Mood/Day: average
                else:
                    return '0' #== Mood/Day: bad
            if self.entry_sentiment['compound']>0.5:
                return '100' #== Mood/Day: good    
            else:
                if self.entry_sentiment['neg']>0.4:
                    return '0' #== Mood/Day: bad
                else:
                    return '50' #== Mood/Day: averag  
       
    def __str__(self):
        return f"> {self.entry_date_time.day:02g}.{self.entry_date_time.month:02g}.{self.entry_date_time.year} [{self.entry_date_time.hour:02g}:{self.entry_date_time.minute:02g}:{self.entry_date_time.second:02g}] {self.entry_content} (auto-grade: {self.emo_meter}, user-grade: {self.emo_grade})"
        #return f"> {self.entry_date_time.day:02g}.{self.entry_date_time.month:02g}.{self.entry_date_time.year} [{self.entry_date_time.hour:02g}:{self.entry_date_time.minute:02g}:{self.entry_date_time.second:02g}] {self.entry_content})"
    
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

    def entry_reaction (self, entry: Entry): # choosing words of reaction/support to the entry content based on automatic evaluation
        self.entry=entry

        # reactions to an entry:
        emo={
            '0':["Not the best day ever?", 
                 "Sh*t happens. You'll try again tomorrow.", 
                 "As a wise man said...Some days are genuinely f*cked and cannot be unf*cked, so go home and sleep.", 
                 "Big HUG!", 
                 "Remember, no storm lasts forever.", 
                 "Good news: not the worst either ;)", 
                 "Not every day is a good day. And you know what? That's Ok too.", 
                 "Be optimistic, it can always be worse ;)", 
                 "Prescribing you more self-care and more self-love today!"],

            '50':[f"Perhaps, you think it's been just an average {self.entry.entry_date_time.strftime("%A")}, but" , 
                  "objectively speaking, all is good, right? ;)", 
                  "think of all the bad things that did not happen today. See how lucky you are?", 
                  "you are really trying and it shows!", 
                  "in fact, you are nailing it, love!"],
            '100':["It seems you've had a pretty good day.", 
                   "Congrats! Keep going!", 
                   "Be proud of yourself!", 
                   "Tomorrow might be even better!", 
                   "Have many more of them!", 
                   "Well done!", 
                   "I'm so happy for you!", 
                   "So good to see you smiling, dear!"],
            }

        # Printing the relevant reaction to the entry:
        x=self.entry.emo_meter
        #print(self.entry.entry_sentiment) ### DELETE AFTER!!!
        #print(x)  ### DELETE AFTER!!!
        print (f"{emo[x][0]} {choice(emo[x][1:])}")

        # Asking the user to evaluate their day themselves >> to use the grade in training this evaluation model in the future:
        while entry.emo_grade==None:
            grade=input("How do you rate this day yourself? Give it a score from 0 to 100: ")
            if grade.isdigit() and 0<=int(grade)<=100:
                entry.emo_grade=grade
                break
            else:
                print("Please, enter a number from 0 to 100")
        
        # Brief assessment of the accuracy:
        by_user=int(entry.emo_grade)
        by_app=int(self.entry.emo_meter)
        if (by_user<33 and by_app==0) or (33<=by_user<=66 and by_app==50) or (by_user>66 and by_app==100):
            print('So, I guessed correctly.\nThank you!')
        else:
            print('I see that I guessed it wrong.\nYour rate will help me guess better in the future!\nThank you! ')

    # When you EXIT the app (==0):
    def quit(self):
        print("See you soon, bye!")
        quit()
          
    # To ADD an entry (==1):
    def new_entry(self):
        notes=input("Diary entry: ")        
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
            print("You have entered valid date and time, but there is no diary entry searching them")
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
            print("You have entered valid date and time, but there is no diary entry searching them")
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

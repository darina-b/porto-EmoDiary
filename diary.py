# Let's make a simple diary app. 
# In this diary, you can read, add, delete, and modify your entries.  

# Import the necessary tools:
from datetime import datetime, timedelta
from pathlib import Path
from textblob import TextBlob
from random import choice
import re

###################
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
###################

class Entry: # == the basic unit of the diary list
    def __init__ (self, entry_date_time: datetime, entry_content: str, feel_me_day=None: tuple):
        self.entry_date_time=entry_date_time
        self.entry_content=entry_content
        self.entry_sentiment=TextBlob(entry_content).sentiment()
        self.feel_me_day=self.mood_checker()

    def mood_checker (self):
        if self.entry_sentiment.subjectivity >= 0.5: # looks into the more subjective sentiments ('me' over 'day')
            if -1<=self.entry_sentiment.polarity<=-0.5:
                return ('1', 'me') #== 'Mood: pretty bad', 'Feeling down today? Big hug!', 'Looks like you might be upset about something. Remember, no storm lasts forever.'
            elif -0.5<self.entry_sentiment.polarity<=0:
                return ('2', 'me') #== 'Mood: Ok', 'Be optimistic, it can always be worse ;)', 'Prescribing you more self-care and more self-love today!'
            elif 0<self.entry_sentiment.polarity<=0.5:
                return ('3', 'me') #== 'Mood: not bad' 'You are really trying and it shows!', 'You are nailing it, love!'
            elif 0.5<self.entry_sentiment.polarity<=1:
                return ('4', 'me') #== 'Mood: feeling great' 'Oh! Someone is in a good mood today?! Happy for you!', 'So good to see you smiling, dear!'
        else: # looks into the more objective sentiments ('day' over 'me')
            if -1<=self.entry_sentiment.polarity<=-0.5:
                return ('1', 'day') #== 'Day: pretty bad' 'Sh*t happens. Tomorrow you'll try again.', 'Some days are genuinely f*cked and cannot be unf*cked, so go home and sleep.'
            elif -0.5<self.entry_sentiment.polarity<=0:
                return ('2', 'day') #== 'Day: Ok', 'Not the best day? Good news: not the worst either ;)', 'Not every day is a good day. And you know what? That's Ok too.'
            elif 0<self.entry_sentiment.polarity<=0.5:
                return ('3', 'day') #== 'Day: average' 'So, it's not such a bad day, after all?', 'Perhaps, tomorrow will be even better, who knows...'
            elif 0.5<self.entry_sentiment.polarity<=1:
                return ('4', 'day') #== 'Day: great' 'It's been a fantastic day today. Have many more of those!', 'Looks like you've had a great day. Well done!'

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
        # reactions to a subjective 'me'-entry:
        me={
            '1':["Mood: pretty bad.", "Feeling down today? Big hug!", "Looks like you might be upset about something. Remember, no storm lasts forever."],
            '2':["Mood: Ok.", "Be optimistic, it can always be worse ;)", "Prescribing you more self-care and more self-love today!"],
            '3':["Mood: not bad.", "You are really trying and it shows!", "You are nailing it, love!"],
            '4':["Mood: feeling great.", "Oh! Someone is in a good mood today?! Happy for you!", "So good to see you smiling, dear!"]
            }
        # reactions to an objective 'day'-entry:
        day={
            '1':["Day: pretty bad." "Sh*t happens. You'll try again tomorrow.", "Some days are genuinely f*cked and cannot be unf*cked, so go home and sleep."],
            '2':["Day: Ok.", "Not the best day? Good news: not the worst either ;)", "Not every day is a good day. And you know what? That's Ok too."],
            '3':["Day: average.", "So, it's not such a bad day, after all?", "Perhaps, tomorrow will be even better, who knows..."],
            '4':["Day: great." "It's been a fantastic day today. Have many more of those!", "Looks like you've had a great day. Well done!"]
            }
        support_words=choice([1,2]) # random choice of reaction phrase from 2 extra options

        #printing the right reaction based on the entry's sentiment value:
        if self.entry.feel_me_day[1]=='me':            
            x==self.entry.feel_me_day[0]
            print (me[x][0])
            print (me[x][support_words])

        elif self.entry.feel_me_day[1]=='day':
            x==self.entry.feel_me_day[0]
            print (day[x][0])
            print (day[x][support_words])
        else:
            raise Error('Something is wrong with the "feel_me_day" tuple!') ### DELETE???

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
        self.entry_reaction()

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

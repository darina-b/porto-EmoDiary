from datetime import datetime, timedelta
from pathlib import Path
#### from textblob import TextBlob
from random import choice, shuffle
import re
import nltk
# nltk.download(["stopwords","twitter_samples","movie_reviews","vader_lexicon","punkt", "punkt_tab"])
from nltk.sentiment import SentimentIntensityAnalyzer

a="> 11.09.2024 [19:33:40] Whatever goes today, let's see if anything works here. Ha-ha (auto-grade: 0, user-grade: 50) > 11.09.2024 [19:35:30] fantastic day! Everything works, everything is smooth and nice (auto-grade: 100, user-grade: 200)"
contents=a.split('> ')[1:]
for c in contents:
    print(c)

    c_entry_date_time=datetime.strptime(c.split(']')[0].replace(' [', ' '),"%d.%m.%Y %H:%M:%S") # separate entry's date and convert it into a datetime object
    print(f'c_entry_date_time:{c_entry_date_time}')
    
    c_entry=c.split(']')[1]
    print(f'c_entry: {c_entry}')
    find_01=re.search('\(auto\-grade\: ',c_entry)
    find_02=re.search(', user\-grade\: ',c_entry)
    find_03=re.search('user\-grade\: .*\)',c_entry)

    #print(f'find_01:{find_01}')
    #print(f'find_02:{find_02}')
    #print(f'find_03:{find_03}')

    c_entry_content=c_entry[:find_01.start()].strip() # separate entry's content
    print(f'c_entry_content: {c_entry_content}')
    
    c_entry_emo_meter=c_entry[find_01.end():find_02.start()].strip()
    print(f'c_entry_emo_meter: {c_entry_emo_meter}')

    c_emo_grade=c_entry[find_02.end():find_03.end()-1].strip() # WORKS ### NAMING!!!
    print(f'c_emo_grade: {c_emo_grade}')
    #re.search('(auto-grade:',c).start()

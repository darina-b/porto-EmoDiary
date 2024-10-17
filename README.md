PROJECT: **EmoDiary**  

AUTHOR: **Darina Bunak**  

TECHNOLOGIES: **Python (Pandas, NumPy, NLTK)**  

##  
![Pic_012](https://github.com/user-attachments/assets/b30ef837-2176-471f-9fd1-9721208e35c6)

##  
**IDEA**  

This is **a responsive diary app** meant to **evaluate user's emotional dynamics and provide daily support**.  
Potentially, keeping such a diary could **help a lot of people**, ranging **from the elderly** users living alone **to** the patients with **severe depression/ addiction/ anger control problems** etc. where a diary is **a part of prescribed therapy**.  

In the latter case, therapist's work is eased by **statistical features of the app**:  
* **Mood statistics** over certain period of time or on a certain date can reveal such trends as seasonal mental detetioration 
or show reaction of the patient to certain events. Looking into it and analysing trends together with the patient could boost theraputical effect.  
* **Language analysis** can deepen therapist's knowledge of dominating ideas and hint on underlying connotations in patient's mind

##  

**SOLUTION**  

**I.** The user is asked to enter the Diary's name or to create a new one. After that, the following options are available:  

*1. Add an entry*  
*2. Read entries added over a requested period  of time*  
*3. Check language statistics*  
*4. Check mood statistics*  

**II.** Once a new entry is added, the user is given a supportive reaction, based on the built-in sentiment evaluation.  
**Evaluation grades** are given in the range **0-100** and divide all sentiments into **3 categories**, i.e **bad** (0-29), **average** (30-70) and **good** (71-100).  

Examplary responses:  

- [x] **Bad mood >>** "Looks like it's not the best day ever? Sh*t happens. You'll try again tomorrow."  
- [x] **Average mood >>** "Perhaps, you think it's been just an average {day-of-week}, but objectively speaking, all is good, right? ;)"
- [x] **Good mood >>** "It seems you've had a pretty good day. Congrats! Keep going!"

**III.** After that, the user is asked to give their own evaluation of their mood:  
"**How do you rate this day yourself? Give it a score from 0 to 100:**"  

If the automatic evaluation did not match user's grade, the app will admit it and apologise: 
*"I see that I was wrong. Your rate will help me guess better in the future.Thank you!"*

**Collecting personal evaluation is important for two reasons;**  
* It collects data for future tuning of the evaluation model
* When the model is well-trained on a large set of diary-like data, it could potentially reveal subjectivity of user's evaluation. 


##  

**FUNCTIONALITY + TESTING**  

Start = RUN. Exit = '0', Ctrl+C. User can: add an entry, read entries for several days, check stats on language, check stats on moods.
When prompted, use file name 'TEST' (file TEST.txt attached)


##  

**COMMENTS**  

Although NLTK is widely recommended for language and sentiment analysis, in this case, it shows very poor reliability.
    Its basic built-in functions, e.g. tagging, raise a lot of questions. Part-of-speech evaluation is too often incorrect. 
    So is sentiment evaluation (I tried to adjust 'manually' but still pretty poor results). Despite the flaws, I decided to keep it for now 
    (too much time spent already) and replace it with a better module (e.g.BERT) later. So, expect strange results when choosing '3'.
##  

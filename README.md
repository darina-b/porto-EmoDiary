PROJECT: **EmoDiary**  

AUTHOR: **Darina Bunak**  

TECHNOLOGIES: **Python (Pandas, NumPy, ML: NLTK)**  

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

**I.** The user is asked to **enter the Diary's name** or to create a new one. After that, the **following options** are available:  

*1. Add an entry*  
*2. Read entries added over a requested period  of time*  
*3. Check language statistics*  
*4. Check mood statistics*  

**II.** If a new entry is added, the user is given a supportive reaction, based on the built-in sentiment evaluation.  

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
* It collects *data for future tuning* of the evaluation model
* When the model is well-trained on a large set of diary-like data, it could potentially *reveal subjectivity of user's evaluation*. 
##  
![Pic_021](https://github.com/user-attachments/assets/c08ac2e9-f2ee-4594-afa5-4d81b9b9b19a)

##  

**FUNCTIONALITY + TESTING**  

**Start** = RUN.  
**Exit** = '0', Ctrl+C.  
**Functionality:** add an entry/ read entries for several days/ check statistics on language/ check statistics on moods.  
**Testing:** when prompted, you can use diary name 'TEST' (in this repo).  
##  

**COMMENTS**  

Although **NLTK** is widely recommended **for language and sentiment analysis**, in this case, it **showed poor reliability**.
It was trained on Tweets, which were the 'closest-to-diary-style' corpora available at the time. However, I believe that **this training corpora is not close enough by style**. 
After numerous adjustments and attempts to fine-tune manually, results are still mediocre.

Luckily, **lack of training material shall be eliminated in the future**, as the data is being **collected from users** in the process. The model can be trained on diary entries (mixed users) 
and if necessary, fine-tuned for a particular user afterwards.

Most surprisingly, the performance of NLTK's **basic built-in functions**, e.g. tagging, also **raises questions**. For example, the part-of-speech evaluation is too often incorrect. 
Despite the flaws, I decided to keep it for now (lack of time) and **replace it with a better module (e.g.BERT) later**. So, expect strange results when choosing '3'.
As they say, 'negative result is still a result'...and **'you live, you learn' :)**

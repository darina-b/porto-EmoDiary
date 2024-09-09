# SENTIMENT EVALUATION MODEL:
from textblob import TextBlob 
wiki = TextBlob("Python is a high-level, general-purpose programming language.") # creates a blob out of text
# sentiment analysis: 
#The sentiment property returns a namedtuple of the form Sentiment(polarity, subjectivity). 
#The polarity score is a float within the range [-1.0, 1.0]. 
#The subjectivity is a float within the range [0.0, 1.0] 
# where 0.0 is very objective and 1.0 is very subjective.

testimonial = TextBlob("Textblob is amazingly simple to use. What great fun!")
testimonial.sentiment
# >> Sentiment(polarity=0.39166666666666666, subjectivity=0.4357142857142857)
testimonial.sentiment.polarity
# >> 0.39166666666666666

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
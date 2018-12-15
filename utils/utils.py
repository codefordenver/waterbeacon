import re
from nltk.corpus import stopwords

def remove_stopwords(input):
    word_list = input.split(" ")
    return ' '.join([word.lower() for word in word_list if word.lower() not in stopwords.words('english')]) # remove stop words

def int_or_none(value):
    try:
        try:
            val = int(value)
        except ValueError:
            val = int(round(float(value))) # just in case we get a float
    except (ValueError, TypeError):
        val = None
    return val

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext.replace("&nbsp;", "")

def removeNonAscii(s):
    return "".join(i for i in s if ord(i)<128)

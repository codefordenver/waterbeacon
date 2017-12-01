from nltk.corpus import stopwords

def remove_stopwords(input):
    word_list = input.split(" ")
    return ' '.join([word.lower() for word in word_list if word.lower() not in stopwords.words('english')]) # remove stop words

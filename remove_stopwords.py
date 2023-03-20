import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

stop_words = set(stopwords.words("english"))

def remove_stpwrds(statement : str) -> list:
    '''
    A function that removes stopwords like {'too', 'than', "isn't", 'doesn', 'an', 'before', 
    'off', 'is', 'be', 'which', 'had', 'now'....}
    '''
    word_list = statement.split(" ")
    filtered_words = [word for word in word_list if word not in stop_words]

    return filtered_words


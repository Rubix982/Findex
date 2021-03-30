import nltk
from nltk.stem.porter import PorterStemmer

def stemmer_func(tokens: list,
            stemming_func: PorterStemmer):
    return [stemming_func.stem(token) for token in tokens]

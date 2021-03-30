import nltk
from nltk.stem import WordNetLemmatizer

def lemmatize_func(tokens: list,
                    lemmatizer: WordNetLemmatizer):
    return [lemmatizer.lemmatize(token) for token in tokens]
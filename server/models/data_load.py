import pathlib
import os

# NLTK
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

# Local packages
from tokenizer import tokenizer
from stemmer import stemmer_func
from lemmatization import lemmatize_func

'''
Couple of steps in the below two lines
Here, os.path.abspath('.') is
'/home/saif/Downloads/University/Semester VI/Information Retrieval/Sir Zeeshan/Assignment/Findex/server/models'
So, what I did was,

1. Reverse the above string,
2. Find the position of '/' that comes first
3. Extract substr starting from that position all the way to the end
4. Reverse back the string
5. Append the `data/` folder path
'''
reversed_abspath = os.path.abspath('.')[::-1]

# Data folder path
data_path = reversed_abspath[reversed_abspath.find(
    '/'):len(reversed_abspath)][::-1] + "data"

# Dist folder path
dist_path = reversed_abspath[reversed_abspath.find(
    '/'):len(reversed_abspath)][::-1] + "dist"

# To store the retrieved file paths
file_paths = []

# stop word list
stop_words_list = []

# Total words
total_words = []

# PORTER STEMMER
porter_stemmer = PorterStemmer()

# NLTK - Regex Tokenizer, for removing punctuation
nltk_tokenizer = nltk.RegexpTokenizer(r"\w+")

# LEMMATIZATION
nltk.download('wordnet')
wordnet_lemmatizer = WordNetLemmatizer()

# Get file paths


def store_file_paths():
    for path in pathlib.Path(data_path).rglob('*.txt'):
        file_paths.append(str(path.parent) + "/" + str(path.name))

# load the stop words/


def load_stop_words():

    # Open the stop words file
    with open(f"{data_path}/Stopword-List.txt", mode='r') as file:

        # ... Going through the file until EOF - end of file
        for line in file:

            # Removing possible misc UTf-8 characters
            line = line.strip('\n')
            line = line.strip(' ')

            # Appending to the `stop_words` list
            stop_words_list.append(line)

# preprocess data files


def process_pipeline():
    for file_path in file_paths:
        with open(file_path, mode='r') as file:

            for line in file:

                '''
                TOKENIZER

                This does the following steps described below. 

                Taking an example,
                "“Yes,” said Ivan Abramitch, looking pensively out of window, “it is
                never too late to marry."

                The following steps demonstrate what they do

                1. First removes punctuation, then tokenizes them, using nltk

                Yes said Ivan Abramitch looking pensively out of window it is 
                never too late to marry

                ['Yes', 'said', 'Ivan', 'Abramitch', 'looking', 'pensively', 'out', 
                'of', 'window', 'it', 'is', 'never', 'too', 'late', 'to', 'marry']

                2. Uses case folding - that is, just makes the tokens lower cased

                ['yes', 'said', 'ivan', 'abramitch', 'looking', 'pensively', 'out', 
                'of', 'window', 'it', 'is', 'never', 'too', 'late', 'to', 'marry']

                3. Finally, removing tokens

                ['yes', 'said', 'ivan', 'abramitch', 'looking', 'pensively', 'out', 
                'of', 'window', 'it', 'is', 'never', 'too', 'late', 'marry']
                '''
                tokens = tokenizer(line, nltk_tokenizer, stop_words_list)

                '''
                PORTER STEMMER

                This turns our previous input into the following
                >>> ['ye', 'said', 'ivan', 'abramitch', 'look', 'pensiv', 'out', 'of', 
                'window', 'it', 'is', 'never', 'too', 'late', 'to', 'marri']
                '''
                tokens = stemmer_func(tokens, porter_stemmer)

                '''
                # LEMMATIZATION

                This turns our previous input into the following
                >>> ['ye', 'said', 'ivan', 'abramitch', 'look', 'pensiv', 'out', 'of', 
                'window', 'it', 'is', 'never', 'too', 'late', 'to', 'marri']
                '''
                tokens = lemmatize_func(tokens, wordnet_lemmatizer)

                '''
                CHECK AGAIN FOR STOP WORDS

                Parse tokens list again if any punctuation result through
                stemmer and lemma
                '''
                for idx, token in enumerate(tokens):
                    if token.strip(' ') in stop_words_list:
                        tokens.remove(token)

                # Append the tokens in a final list
                for token in tokens:
                    if token not in total_words and not token.isnumeric():
                        total_words.append(token)


def save_total_words():
    '''
    If the path `../dist` does not exist, create it
    '''
    if not os.path.exists(dist_path):
        os.makedirs(dist_path)

    '''
    Store the list `total_words` at the location
    `../dist/Total-Words.txt`
    '''
    with open(f"{dist_path}/Total-Words.csv", mode='w') as file:
        for idx, word in enumerate(total_words):
            file.write(f"{idx}, {word},\n")


def data_load_and_save():
    '''
    Loads the file paths for all the files
    '''
    store_file_paths()

    '''
    Loads the stop words
    '''
    load_stop_words()

    '''
    Goes through each each from `store_file_path()` and processes it through,
    
    1. Document collection - all the data in one place
    2. Tokenization
        2.1. Removes punctuation
        2.2. Tokenizes each line
        2.3. Case folding, lower casing
        2.4. Stop word removal
    3. Stemmer
    4. Lemmatization 
    '''
    process_pipeline()

    '''
    Saves the total_words list as a TEXT file at the
    location `../dist/Total-Words.txt`
    '''
    save_total_words()

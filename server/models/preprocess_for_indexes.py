import pathlib
import string
import nltk
import json
import re
import os
import multiprocessing as mp
from nltk.stem import WordNetLemmatizer
from multiprocessing import Pool

# import local, custom stemmer implementation for Porter
from custom_porter_algorithm import custom_porter_algorithm

# import positional index
from positional_index import PositionalIndex

# import positional node
from position_node import PositionNode

reversed_abspath = os.path.abspath('.')[::-1]

# Data folder path
data_path = reversed_abspath[reversed_abspath.find(
    '/'):len(reversed_abspath)][::-1] + "data"

# Dist folder path
dist_path = reversed_abspath[reversed_abspath.find(
    '/'):len(reversed_abspath)][::-1] + "dist"

# Positional Indexing folder path
positional_indexing_path = dist_path + "/positional"

# Inverted Indexing folder path
inverted_indexing_path = dist_path + "/inverted"

# To store the retrieved file paths
file_paths = []

# stop word list
stop_words_list = []

# stop word list
unique_word_counter = -500

# NLTK - Regex Tokenizer, for removing punctuation
nltk_tokenizer = nltk.RegexpTokenizer(r"\w+")

# LEMMATIZATION
nltk.download('wordnet')
wordnet_lemmatizer = WordNetLemmatizer()

# Very annoying UTF 8 characters
very_annoying_utf_8_characters = [
    '\n', '\r', '\"', '\'', '.', '’', ',', '“' '”', ';', '“', '!', '”', '”', '“', '-']

# If folders donot exist
if not os.path.exists(positional_indexing_path):
    os.makedirs(positional_indexing_path)

if not os.path.exists(inverted_indexing_path):
    os.makedirs(inverted_indexing_path)

# path_name_list
path_name_list = []

# patlib.Path results
pathlib_walked_path = pathlib.Path(data_path).rglob('*.txt')

# waste generation
next(pathlib_walked_path)

# path_name_parent
path_name_parent, path_name_seen = '', False

path_name_file_extension = next(pathlib_walked_path).name.split('.')[1]

# Get the file paths for each of the short stories
for path in pathlib_walked_path:

    if not path_name_seen:
        path_name_seen = True
        path_name_parent = path.parent

    path_name_list.append(int(str(path.name).split('.')[0]))

path_name_list = [
    f"{str(entry)}.{path_name_file_extension}" for entry in sorted(path_name_list)]

file_paths = [
    f"{str(path_name_parent)}/{str(path_name_entry)}" for path_name_entry in path_name_list]


def process_data_through_pipelines():

    short_stories_path = f"{dist_path}/ShortStories"

    global file_paths

    if not os.path.exists(short_stories_path):
        os.makedirs(short_stories_path)

    for path in file_paths:

        tokens = []

        with open(path) as file:

            # for line in file:
            data = file.readlines()

            for idx, _ in enumerate(data):
                for remove_character in very_annoying_utf_8_characters:
                    data[idx] = data[idx].replace(remove_character, ' ')
                    data[idx] = re.sub(' +', ' ', data[idx].strip())

            data = ' '.join([entry for entry in data if entry != '' and not entry.isnumeric()])
            tokens = [token.lower() for token in data.split(' ')]

            # STEMMING ->> LEMMATIZATION
            tokens = [wordnet_lemmatizer.lemmatize(
                custom_porter_algorithm(token)) for token in tokens]

            with open(f"{short_stories_path}/{path.split('/')[-1].split('.')[0]}.txt", mode='w') as file:
                file.write(' '.join(tokens))


def generate_positional_index(str_to_build_positional: str, positional_index: PositionalIndex):

    global file_paths
    short_stories_path = []
    total_positions = ''

    for path in file_paths:
        new_path = path.split('/')
        new_path[-3] = 'dist'
        short_stories_path.append('/'.join(new_path))

    for file_path_idx, path in enumerate(short_stories_path):

        positions = ''
    
        with open(path) as file:
            tokens = file.readlines()[0].split(' ')
            
            # TODO - I haven't tested how accurately this works
            for idx, token in enumerate(tokens):
                if str_to_build_positional == token:
                    positions += f"{idx},"

        if positions != '':
            positions = f"{file_path_idx},{positions[0:-1]};"
            total_positions = total_positions + positions

    positional_index.document_listing_positions = total_positions

def for_line_store_file(line: str):

    global unique_word_counter

    # Preprocessing / cleaning
    entry = line.strip('\n').split(',')[0:2]

    if os.path.exists(f"{positional_indexing_path}/{entry[1]}.txt"):
        return

    # Determining the csv path
    # csv_file_path = f"{inverted_indexing_path}/{unique_word_counter+500}-{unique_word_counter+1000}.csv"

    # Creating a new csv file for the words if none was found
    if int(entry[0]) < unique_word_counter + 500:
        unique_word_counter += 500

    # generate positional index
    positional_index = PositionalIndex(
        unique_hash=f"{entry[0]}")

    # Get the postiings from the parse
    generate_positional_index(entry[1], positional_index)

    content_dump = positional_index.__dict__

    if content_dump['document_listing_positions'] == '':
        return

    # opening file to save
    with open(f"{positional_indexing_path}/{entry[1]}.txt", mode='w') as file:
        # serializing to json
        file.write(
            f"{content_dump['unique_hash']}-{content_dump['document_listing_positions']}")

    # # opening file to save
    # with open(csv_file_path, 'a') as file:
    #     file.write(f"{content_dump['unique_keyword']},")
    #     for i in range(len(file_paths)):
    #         file.write(
    #             f"{len(content_dump['document_listing_positions'][i]['position_list'])},")
    #     file.write('\n')


def get_saved_normalized_words():

    global unique_word_counter

    total_words_list = []
    with open(f"{dist_path}/Total-Words.csv") as file:
        for line in file:
            # for_line_store_file(line)
            total_words_list.append(line)

    with mp.Pool(10) as p:
        p.map(for_line_store_file, total_words_list)


get_saved_normalized_words()

# process_data_through_pipelines()

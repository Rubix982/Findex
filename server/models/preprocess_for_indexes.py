import pathlib
import string
import nltk
import json
import re
import os
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


def generate_positional_index(str_to_build_positional: str, positional_index: PositionalIndex):

    total_positions = ''

    for path_index, path in enumerate(file_paths):

        tokens = []
        positions = ''

        with open(path) as file:

            # for line in file:
            data = file.readlines()

            for idx, _ in enumerate(data):
                for remove_character in very_annoying_utf_8_characters:
                    data[idx] = data[idx].replace(remove_character, ' ')
                    data[idx] = re.sub(' +', ' ', data[idx].strip())

            data = ' '.join([entry for entry in data if entry != ''])
            tokens = [token.lower() for token in data.split(' ')]

        for idx, token in enumerate(tokens):

            # STEMMING ->> LEMMATIZATION
            token = wordnet_lemmatizer.lemmatize(
                custom_porter_algorithm(token))

            # TODO - I haven't tested how accurately this works
            if token == str_to_build_positional:
                positions += f"{idx},"

        if positions == '':
            continue

        # positional_node = PositionNode(
        #     doc_id=path.split('/')[-1].split('.')[0], position_list=positions)

        positions = f"{path_index},{positions[0:-1]};"
        total_positions = total_positions + positions

    positional_index.document_listing_positions = total_positions


def get_saved_normalized_words():

    global unique_word_counter

    with open(f"{dist_path}/Total-Words.csv") as file:
        for line in file:

            # Preprocessing / cleaning
            entry = line.strip('\n').split(',')[0:2]

            # Determining the csv path
            csv_file_path = f"{inverted_indexing_path}/{unique_word_counter+500}-{unique_word_counter+1000}.csv"

            # Creating a new csv file for the words if none was found
            if int(entry[0]) < unique_word_counter + 500:
                unique_word_counter += 500
            #     if not os.path.isfile(csv_file_path):
            #         with open(csv_file_path, 'w') as file:
            #             file.write(',')
            #             for i in range(1, 50 + 1):
            #                 file.write(f"{i},")
            #             file.write('\n')
            # else:

            # generate positional index
            positional_index = PositionalIndex(
                unique_hash=f"{entry[0]}")

            # Get the postiings from the parse
            generate_positional_index(entry[1], positional_index)

            content_dump = positional_index.__dict__

            if content_dump['document_listing_positions'] == '':
                content_dump.pop('document_listing_positions')

            # opening file to save
            with open(f"{positional_indexing_path}/{entry[1]}.json", mode='w') as file:
                # serializing to json
                file.write(json.dumps(content_dump))

            # # opening file to save
            # with open(csv_file_path, 'a') as file:
            #     file.write(f"{content_dump['unique_keyword']},")
            #     for i in range(len(file_paths)):
            #         file.write(
            #             f"{len(content_dump['document_listing_positions'][i]['position_list'])},")
            #     file.write('\n')


get_saved_normalized_words()
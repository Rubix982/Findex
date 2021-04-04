from nltk.stem import WordNetLemmatizer

from Preprocessing import Porter

import re

from main import word_dict


class BooleanRetrievalModel():

    def __init__(self):
        self.wordnet_lemmatizer = WordNetLemmatizer()

    def boolean_query(self, query: str):
        tokens = str.split(' ')

        # Very annoying UTF 8 characters
        very_annoying_utf_8_characters = [
            '\n', '\r', '\"', '\'', '.', '’', ',', '“' '”', ';', '“', '!', '”', '”', '“', '-']

        for idx, _ in enumerate(tokens):
            for remove_character in very_annoying_utf_8_characters:
                tokens[idx] = tokens[idx].replace(remove_character, ' ')
                tokens[idx] = re.sub(' +', ' ', tokens[idx].strip())

        tokens = ' '.join([entry for entry in tokens if entry !=
                           '' and not entry.isnumeric()])

        tokens = [token.lower() for token in tokens.split(' ')]

        # STEMMING ->> LEMMATIZATION
        tokens = [self.wordnet_lemmatizer.lemmatize(
            Porter.CustomPorterAlgorithm(token)) for token in tokens]

        token_id = {}
        for token in tokens:
            token_id[word_dict[token]] = token

        positional_index = {}
        with open('../dist/positional.txt', mode='r') as file:
            for line in file:
                line_tokens = line.split('-')
                if line_tokens[0] in token_id:
                    positional_index[line_tokens[0]] = line_tokens[1]

        document_id = []
        for _, value in positional_index.items():
            tokens = value.split(';')

            for docs in tokens:
                document_id.append(docs.split(',')[0])

        if len(tokens) == 1:
            return tokens

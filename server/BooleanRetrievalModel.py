from nltk.stem import WordNetLemmatizer
from collections import OrderedDict
from Preprocessing import Porter
import re
import sys


class BooleanRetrievalModel():

    def __init__(self):
        self.id_token_dict_path = './dist/Total-Words.csv'
        self.positional_index_path = './dist/positional/positional.txt'
        self.wordnet_lemmatizer = WordNetLemmatizer()

    def GetTokenDictionary(self, filename: str):

        __token_to_id_dict = {}

        try:
            with open(filename, mode='r') as file:
                for line in file:
                    __tokens = line.split(',')
                    __token_to_id_dict[__tokens[1]] = __tokens[0]
        except FileNotFoundError:
            print('File not found!')
            sys.exit(1)

        return __token_to_id_dict

    def TokensToId(self, tokens: list, tokens_to_id_dict: dict):
        __token_to_id = []
        for token in tokens:
            __token_to_id.append(tokens_to_id_dict[token])
        return __token_to_id

    def PreprocessQuery(self, query: str):
        __tokens = query.split(' ')

        # Very annoying UTF 8 characters
        very_annoying_utf_8_characters = [
            '\n', '\r', '\"', '\'', '.', '’', ',', '“' '”', ';', '“', '!', '”', '”', '“', '-']

        for idx, _ in enumerate(__tokens):
            for remove_character in very_annoying_utf_8_characters:
                __tokens[idx] = __tokens[idx].replace(remove_character, ' ')
                __tokens[idx] = re.sub(' +', ' ', __tokens[idx].strip())

        __tokens = ' '.join([entry for entry in __tokens if entry !=
                             '' and not entry.isnumeric()])

        __tokens = [token.lower() for token in __tokens.split(' ')]

        # STEMMING ->> LEMMATIZATION
        __tokens = [self.wordnet_lemmatizer.lemmatize(
            Porter.CustomPorterAlgorithm(token)) for token in __tokens]

        return __tokens

    def GetPositionalIndex(self, tokens_to_id: list):
        __id_with_positions = OrderedDict()
        with open(self.positional_index_path, mode='r') as file:
            for line in file:
                line_split_token = line.split('-')
                if line_split_token[0] in tokens_to_id:
                    __id_with_positions[line_split_token[0]
                                        ] = line_split_token[1]

        return __id_with_positions

    def ExtractOnlyDocuments(self, id_with_positions: dict):
        __document_ids: dict = {}
        for key, value in id_with_positions.items():
            split_docs = value.split(';')
            for docs in split_docs:
                doc_id = docs.split(',')[0]
                if doc_id not in __document_ids:
                    __document_ids[key].append(docs.split(',')[0])
        return __document_ids

    def IntersectDocuments(self, documents_per_word: dict):

        doc_key_1 = next(iter(documents_per_word))
        doc_key_2 = next(iter(documents_per_word))

        doc_list_1 = documents_per_word[doc_key_1]
        doc_list_2 = documents_per_word[doc_key_2]

        __intersect_documents = [
            value for value in doc_list_1 if value in doc_list_2]

        for (_, value) in (documents_per_word.items()):
            __intersect_documents = [
                doc_id for doc_id in __intersect_documents if doc_id in value]

        return __intersect_documents

    def QueryDocPositions(self, query: str,
                          documents_per_word: list,
                          id_with_positions: dict) -> list:

        positions = []
        query_len = len(query)

        for _, value in id_with_positions.items():
            value_split_for_docs = value.split(';')
            for doc_space in value_split_for_docs:
                if doc_space.split(',')[0] in documents_per_word:
                    for entry in doc_space.split(',')[1]:
                        positions.append(int(entry))

        positions.sort()

        continue_count = 0
        for index in range(0, len(positions)):
            if positions[index] + 1 == positions[index + 1]:
                continue_count += 1
            else:
                continue_count = 0

            if continue_count == query_len:
                return positions

        return []

    def SimpleBooleanQuery(self, query: str):

        # Preprocess and convert the tokens to their respective IDs
        __tokens_to_id = self.TokensToId(
            self.PreprocessQuery(query), self.GetTokenDictionary(self.id_token_dict_path))

        __positional_indexes = self.GetPositionalIndex(__tokens_to_id)

        __document_ids = self.ExtractOnlyDocuments(__positional_indexes)

        if len(__document_ids):
            return __document_ids
        else:
            __intersected_docs = self.IntersectDocuments(__document_ids)

            return self.QueryDocPositions(
                query, __intersected_docs, __positional_indexes)

    def ORQuery(self, document_1, document_2):
        return [1, 2, 3]

    def ANDQuery(self, document_1, document_2):
        return [1, 2, 3]

    def NOTQuery(self, document_1, document_2):
        return [1, 2, 3]

    def ComplexBooleanQuery(self, query: str):

        __tokens = query.split(' ')

        phrases = []
        operators = []

        init_pos = 0
        for index, token in enumerate(__tokens):
            if token == 'AND' or token == 'OR' or token == 'NOT':
                phrases.append(__tokens[init_pos:index])
                init_pos = index + 1
                if token == 'AND':
                    operators.append('AND')
                elif token == 'OR':
                    operators.append('OR')
                elif token == 'NOT':
                    operators.append('NOT')

        if len(phrases) == 3:
            final_docs_1 = self.SimpleBooleanQuery(' '.join(phrases[0]))
            final_docs_2 = self.SimpleBooleanQuery(' '.join(phrases[1]))

            if operators[0] == 'AND':
                results = self.ANDQuery(final_docs_1, final_docs_2)
            elif operators[0] == 'OR':
                results = self.ORQuery(final_docs_1, final_docs_2)
            elif operators[0] == 'NOT':
                results = self.NOTQuery(final_docs_1, final_docs_2)

            final_docs_3 = self.SimpleBooleanQuery(' '.join(phrases[2]))

            if operators[1] == 'AND':
                results = self.ANDQuery(final_docs_3, results)
            elif operators[1] == 'OR':
                results = self.ORQuery(final_docs_3, results)
            elif operators[1] == 'NOT':
                results = self.NOTQuery(final_docs_3, results)

            return results

        elif len(phrases) == 2:
            final_docs_1 = self.SimpleBooleanQuery(' '.join(phrases[0]))
            final_docs_2 = self.SimpleBooleanQuery(' '.join(phrases[1]))

            if operators[0] == 'AND':
                results = self.ANDQuery(final_docs_1, final_docs_2)
            elif operators[0] == 'OR':
                results = self.ORQuery(final_docs_1, final_docs_2)
            elif operators[0] == 'NOT':
                results = self.NOTQuery(final_docs_1, final_docs_2)

            return results

        elif len(phrases) == 1:
            return self.SimpleBooleanQuery(' '.join(phrases[0]))
        else:
            print('Empty query received!')
            return

    def ProximityQuery(self, query: str):
        return [1, 2, 3]

    def ResolveQuery(self, query: str, option: int):

        collection_of_documents = []

        if option == 0:
            return self.SimpleBooleanQuery(query)
        elif option == 1:
            return self.ComplexBooleanQuery(query)
        elif option == 2:
            return self.ProximityQuery(query)

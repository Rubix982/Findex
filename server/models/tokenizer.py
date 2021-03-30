import nltk


def tokenizer(line: str,
              nltk_tokenizer: nltk.RegexpTokenizer,
              stop_words_list: list):

    # TOKENIZATION - removes punctuation!
    tokens = nltk_tokenizer.tokenize(line)

    # CASE FOLDING
    tokens = [token.lower() for token in tokens]

    # STOP WORDS REMOVAL
    for token in tokens:
        if token in stop_words_list:
            tokens.remove(token)
    
    return tokens

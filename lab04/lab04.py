import re
from collections import Counter

filepath_dictionary = "dictionary.txt"
filepath_text = "text.txt"
filepath_words_to_check = "words_to_check2.txt"

DIACRITIC_ERR_COST = {
	("ą","a") : 0.5,
	("ć","c") : 0.5,
	("ę","e") : 0.5,
	("ł","l") : 0.5,
	("ń","n") : 0.5,
	("ó","o") : 0.5,
    ("ś","s") : 0.5,
    ("ź","z") : 0.5,
    ("ż","z") : 0.5
}

PRONUNCIATION_ERR_COST = {
	("ł","u") : 0.5,
	("w","f") : 0.5,
	("z","s") : 0.5,
	("b","p") : 0.5,
	("d","t") : 0.5,
	("g","k") : 0.5,
	("ź","ś") : 0.5,
	("i","j") : 0.5,
}

def preprocess_text(filepath):
    with open(filepath, encoding="utf8") as f:
        text = f.read()
        text = text.lower()
        text = re.sub("[()[\]{\}0-9.,<>\":;+%*$#^?!*@=&_]", "", text)
        text = re.sub("[\-]", " ", text)
        text = re.sub("\s+", " ", text)
    return text

def split_text_into_words(filepath):
    text = preprocess_text(filepath)
    words = text.split()
    return words

def modify_cost(f, s):
    for key in PRONUNCIATION_ERR_COST:
        (f_key, s_key) = key
        if (f == f_key and s == s_key) or (f == s_key and s == f_key):
            return PRONUNCIATION_ERR_COST[key]
    return 1

def levenshtein(first_string, second_string):
    str_length_1 = len(first_string)
    str_length_2 = len(second_string)
    cost = 0

    if str_length_1 and str_length_2 and first_string[0] != second_string[0]:
        cost = modify_cost(first_string[0], second_string[0])

    if str_length_1 == 0:
        return str_length_2
    elif str_length_2 == 0:
        return str_length_1
    else:
        return min(
            levenshtein(first_string[1:], second_string) + 1,
            levenshtein(first_string, second_string[1:]) + 1,
            levenshtein(first_string[1:], second_string[1:]) + cost,
)

def normalized_levenshtein(first_string, second_string):
    lev = levenshtein(first_string, second_string)
    return 1 - lev / max(len(first_string), len(second_string))

def calc_Pc(c, corpus, M):
    occurences_in_corpus = corpus.count(c)
    return (occurences_in_corpus + 5) / (len(corpus) + 5*M)

def calc_Pcw(w, c, corpus, dictionary):
    Pc = calc_Pc(c, corpus, len(dictionary))
    Pwc = normalized_levenshtein(w,c)
    return Pwc * Pc

def check_correctness(word, corpus, dictionary):
    counter = Counter()
    if word in dictionary:
        return "Word %s is correct\n" % word
    
    for c in dictionary:
        counter[c] = calc_Pcw(word, c, corpus, dictionary)
    return "Incorrect word: %s. \nDid you mean: %s?\n" % (word, str(counter.most_common(3)))

def check_words(words, corpus, dictionary):
	for word in words:
		print(check_correctness(word, corpus, dictionary))


text = split_text_into_words(filepath_text)
dictionary = split_text_into_words(filepath_dictionary)
words = split_text_into_words(filepath_words_to_check)

print()
check_words(words, text, dictionary)
import re
import math
from collections import Counter 
from scipy import spatial

file = "data/pap.txt"
dict_file = "data/odm.txt"


def separate_notes(filepath):
    with open(filepath, encoding="utf8") as f:
        notes = f.read()
        notes = notes.lower()
        notes = re.split("\#[0-9]{6}\n", notes)[1:]
    return notes

def split_notes_into_words(notes):
    result = []
    for note in notes:
        note = re.sub("[()[\]{\}0-9.,<>\":;+*?!*@=&_]", "", note)
        note = re.sub("\-", " ", note)
        note = re.sub("\s+", " ", note)
        result.append(note.split())
    return result

def prepare_dictionary(filepath):
    words_with_base = {}
    with open(filepath, encoding="utf8") as f:
        text = f.read()
        text = text.lower()
        lines = text.split('\n')
        for line in lines:
            words_group = line.split(', ')
            for word in words_group:
                words_with_base[word] = words_group[0]
    return words_with_base

# word -> base form, calculate tf
def bring_text_to_base(words, dictionary):
    base_words = Counter()
    for word in words:
        if word in dictionary:
            base_form = dictionary[word]
            if base_form in base_words:
                base_words[base_form] += 1
            else:
                base_words[base_form] = 1
        else:
            if word in base_words:
                base_words[word] += 1
            else:
                base_words[word] = 1
    return base_words

# notes - list of dictionaries
def calc_df(word, notes):
    count_docs_with_word = 0
    for note in notes:
        if word in note.keys():
            count_docs_with_word += 1
    return count_docs_with_word

def calc_tf_idf(word, note, all_notes):
    df = calc_df(word, all_notes)
    return note[word] * math.log10(len(all_notes) / df)

 # dla base[0] policz dla każdego słowa tf_idf. Wsadź to w słownik ["słowo":tf_idf]
def calc_tf_idf_for_note(note, all_notes):
    result = []
    for key, value in note.items():
        key_tf_idf = calc_tf_idf(key, note, all_notes)
        result.append((key, key_tf_idf))
    return result


#  dla każdej kolejnej notatki policz tf_idf tylko dla słów z pierwszej(wybranej) notatki 
#  Biorę z notatki 1 słowo np "historyk", sprawdzam czy występuje w kolejnej notatce, 
#  jak tak - tf = liczba wystąpień, liczę tf_idf, jak nie = tf_idf = 0
#  zwracam: [(id_notatki, [(słowo":tf_idf)]]
def calc_tf_idf_for_all_notes(note, all_notes):
    all_result = []
    for i in range(0,len(all_notes)):
        result = []
        for key, value in note.items():
            key_tf_idf = calc_tf_idf(key, all_notes[i], all_notes)
            result.append((key, key_tf_idf))
        all_result.append((i, result))
    return all_result

def calc_similarity_cosine(tf_idf_for_note, tf_idf_for_all_notes):
    count = Counter()
    chosen_note_vector = list(map(lambda x: x[1], tf_idf_for_note))
    for (key, tf_idf_values) in tf_idf_for_all_notes:
        current_note_vector = list(map(lambda x: x[1], tf_idf_values))
        count[key] = (1 - spatial.distance.cosine(chosen_note_vector, current_note_vector))
    return count

###############################################################

text = separate_notes(file)
print()
print(text[323])
text = split_notes_into_words(text)
#print(text[0])

dictionary = prepare_dictionary(dict_file)
print()
base = list(map(lambda x: bring_text_to_base(x, dictionary), text))
chosen_note = base[323]
print(chosen_note)  # notatka, dla której sprawdzam

print()
#print(calc_df("historyk", base))
#print(calc_tf_idf("historyk", chosen_note, base))

chosen_note_tf_idf = calc_tf_idf_for_note(chosen_note, base)
#print(chosen_note_tf_idf)

all_notes_tf_idf = calc_tf_idf_for_all_notes(chosen_note, base)
#print(all_notes_tf_idf[1:2])

print()
similar = calc_similarity_cosine(chosen_note_tf_idf, all_notes_tf_idf)
print(similar.most_common(20))
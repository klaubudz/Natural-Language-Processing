import re
from collections import defaultdict
from gensim import corpora, models, similarities

############################ Preparing text, dictionary and stoplist ############################

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

def prepare_stoplist(filepath):
	with open(filepath, encoding="utf8") as f:
		stoplist = f.read()
		stoplist = set(stoplist.split())
	return stoplist

def apply_stoplist(notes, stoplist):
	notes_words = []
	for note in split_notes_into_words(notes):
		words = []
		for word in note:
			if word not in stoplist:
				words.append(word)
		notes_words.append(words)
	return notes_words


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

def bring_text_to_base(words, dictionary):
    base_words = []
    for word in words:
        if word in dictionary:
            base_form = dictionary[word]
            base_words.append(base_form)
        else:
            base_words.append(word)
    return base_words

############################ Counting words occurences ############################

def calc_word_occurences(base_notes):
	words_occurences = defaultdict(int)
	for note in base_notes:
		for word in note:
			words_occurences[word] += 1
	return words_occurences

def calc_word_occurences_in_notes(base_notes):
	occ_all = calc_word_occurences(base)
	notes_words_occurences = []
	for note in base_notes:
		note_word_occ = []
		for word in note:
			if occ_all[word] > 1:
				note_word_occ.append(word)
		notes_words_occurences.append(note_word_occ)
	return notes_words_occurences


############################ Build LSI Model ############################

def getLsiModel(notes_words_occ):
	dictionary = corpora.Dictionary(notes_words_occ)	# word<->id
	dictionary.filter_extremes(no_below=2, no_above=0.7, keep_n=200000)

	corpus = [dictionary.doc2bow(note) for note in notes_words_occ]
	tfidf_model = models.TfidfModel(corpus)
	corpus_tfidf = tfidf_model[corpus]

	lsi_model = models.lsimodel.LsiModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=400)
	corpus_lsi = lsi_model[corpus]
	return corpus, lsi_model, corpus_lsi
	
############################ Program execution ############################

file_text = "data/pap.txt"
file_dict = "data/odm.txt"
file_stop = "data/stoplist.txt"
selected_note_id = 10507

# Prepare notes
notes = separate_notes(file_text)
selected_note = notes[selected_note_id]
print("--------------------------------------")
print("Number of notes: " + str(len(notes)))
print("--------------------------------------")
print("Selected note id: " + str(selected_note_id))
print("Selected note: ")
print(selected_note)

# Prepare & apply stoplist
stoplist = prepare_stoplist(file_stop)
notes = apply_stoplist(notes, stoplist)
print("--------------------------------------")
print("Selected note split into words: ")
print(notes[selected_note_id])

# Prepare dictionary & bring words to base
base_dictionary = prepare_dictionary(file_dict)
base = list(map(lambda x: bring_text_to_base(x, base_dictionary), notes))

# Count words occurences in notes
words_occurences_in_notes = calc_word_occurences_in_notes(base)
print("--------------------------------------")
print("Selected note words brought to base form:")
print(words_occurences_in_notes[selected_note_id])

# Identify topics of notes
corpus, lsi_model, corpus_lsi = getLsiModel(words_occurences_in_notes)
print("--------------------------------------")
print("Identified topics: ")
for topic in lsi_model.print_topics(10):
	print(topic)

# Find similar notes
index = similarities.MatrixSimilarity(corpus_lsi)
sims = index[lsi_model[corpus[selected_note_id]]]
sims = sorted(enumerate(sims), key=lambda item: -item[1])
print("--------------------------------------")
print("The closest notes :")
print(sims[:15])

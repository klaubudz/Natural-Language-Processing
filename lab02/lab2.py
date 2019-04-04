import re
from collections import Counter

filepath_dictionary = "data/odm.txt"
filepath_test = "data/potop.txt"

def preprocess_text(filepath):
    with open(filepath, encoding="utf8") as f:
        text = f.read()
        text = text.lower()
        text = re.sub("[()[\]{\}0-9.,<>\":;+*?!*@=&_]", "", text)
        text = re.sub("[\-]", " ", text)
        text = re.sub("\s+", " ", text)
    return text

def split_text(filepath):
    text = preprocess_text(filepath)
    words = text.split()
    return words

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

def write_data_to_file(filepath, base_words):
	count = 0
	all_words_number = sum(base_words.values())
	percentage = 0
	with open(filepath, "w+", encoding='utf8') as f:
		for word in base_words.most_common():
			count += 1
			percentage += (word[1] / all_words_number) * 100
			# Słowo, ilość wystąpień, rank(indeks), % skumulowany
			f.write(word[0] + " " + str(word[1]) + " " + str(count) + " " + str(percentage) + "\n")
		
def count_hapex_legomena(words):
	return len({k: v for k,v in words.items() if v ==1})

def find_half_of_words(base_words):
	count = 0
	all_words_number = sum(base_words.values())
	percentage = 0
	for word in base_words.most_common():
		count += 1
		percentage += (word[1] / all_words_number) * 100
		if percentage >= 50:
			return (count, len(base_words)-count)

def ngrams_of_words(splitted_text, n):
	ngrams = Counter()
	for i in range(len(splitted_text) - n):
		singleNgram = " ".join(splitted_text[i:n+i])
		if singleNgram in ngrams:
			ngrams[singleNgram] += 1
		else:
			ngrams[singleNgram] = 1
	return ngrams



splitted_text = split_text(filepath_test)
dictionary = prepare_dictionary(filepath_dictionary)
text2base = bring_text_to_base(splitted_text, dictionary)
#print(text2base.most_common(40))
write_data_to_file("stats.txt", text2base)
print("Hapex:")
print(count_hapex_legomena(text2base))
print(find_half_of_words(text2base))
print(ngrams_of_words(splitted_text, 3).most_common(20))













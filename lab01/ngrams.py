import re
from collections import Counter

filepath = "C:/Users/Klaudia/Desktop/PJN/PJN/lab01/test/pl1.txt"

def preprocess_text(filepath):
    with open(filepath, encoding="utf8") as f:
        text = f.read()
        text = text.lower()
        text = re.sub("[()[\]{\}0-9.,\":;?!*@=&_]", "", text)
        text = re.sub("\s+", " ", text)
    return text

def create_ngrams(filepath, n):
    text = preprocess_text(filepath)
    ngrams = Counter()
    singleNgram = ""
    for c in text:
        if len(singleNgram) != n:
            singleNgram += c
        else:
            ngrams[singleNgram] += 1
            singleNgram = singleNgram[1:]
            singleNgram += c
    #print(ngrams)
    return ngrams






# def create_word_ngrams(filepath, n):
#     text = preprocess_text(filepath)
#     wordngrams = Counter()
#     singleWordNgram = ""
#     for word in text.split():
#         if len(singleWordNgram.split()) != n:
#             singleWordNgram += word
#             singleWordNgram += " "
#         else:
#             wordngrams[singleWordNgram] += 1
#             singleWordNgram = ' '.join((singleWordNgram.split())[1:])
#     print(wordngrams)

#create_ngrams(filepath, 3)
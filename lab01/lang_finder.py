import re
from collections import Counter
from math import fsum, sqrt
from scipy import spatial

from ngrams import create_ngrams

def normalize_vector(vec):
    valSum = fsum(vec.values())
    normalizedVector = {}
    for k, v in vec.items():
        normalizedValue = v / valSum
        normalizedVector[k] = normalizedValue
    return normalizedVector

def euclidean(langVector, testVector):
    sqSum = 0
    langVector = normalize_vector(langVector)
    testVector = normalize_vector(testVector)
    keySet = set(langVector.keys()) | set(testVector.keys())
    for key in keySet:
        sqSum += (langVector.get(key, 0) - testVector.get(key, 0) ) ** 2
    return sqrt(sqSum)

def taxi(langVector, testVector):
    sumAbs = 0
    langVector = normalize_vector(langVector)
    testVector = normalize_vector(testVector)
    keySet = set(langVector.keys()) | set(testVector.keys())
    for key in keySet:
        sumAbs += abs(langVector.get(key, 0) - testVector.get(key, 0))
    return sumAbs

def maximum(langVector, testVector):
    maxAbsValue = 0
    langVector = normalize_vector(langVector)
    testVector = normalize_vector(testVector)
    keySet = set(langVector.keys()) | set(testVector.keys())
    for key in keySet:
        diffAbsValue = abs(langVector.get(key, 0) - testVector.get(key, 0))
        maxAbsValue = max(maxAbsValue, diffAbsValue)
    return maxAbsValue

# def cosine(langVector, testVector):
#     sumMult = 0
#     langVector = normalize_vector(langVector)  #?
#     testVector = normalize_vector(testVector)  #?
#     keySet = set(langVector.keys()) | set(testVector.keys())
#     for key in keySet:
#         sumMult += langVector.get(key, 0) * testVector.get(key, 0)
#     return 1 - sumMult

def cosine(langVector, testVector):
    keySet = set(langVector.keys()) | set(testVector.keys())
    dict1 = {}
    dict2 = {}
    for key in keySet:
        dict1[key] = langVector.get(key, 0)
        dict2[key] = testVector.get(key, 0)
    return spatial.distance.cosine(list(dict1.values()), list(dict2.values()))
     

#------------------------------------------------------------------------------

n = 3
languages = [
    ("en", "lang/english1.txt", create_ngrams("lang/english1.txt", n)),
    ("fi", "lang/finnish1.txt", create_ngrams("lang/finnish1.txt", n)),
    ("de", "lang/german1.txt", create_ngrams("lang/german1.txt", n)),
    ("it", "lang/italian1.txt", create_ngrams("lang/italian1.txt", n)),
    ("pl", "lang/polish1.txt", create_ngrams("lang/polish1.txt", n)),
    ("es", "lang/spanish1.txt", create_ngrams("lang/spanish1.txt", n))
]

testfiles = [
	("en", "test/en1.txt"),
	("en", "test/en2.txt"),
    ("fi", "test/fn1.txt"),
    ("fi", "test/fn2.txt"),
    ("de", "test/de1.txt"),
    ("de", "test/de2.txt"),
    ("it", "test/it1.txt"),
    ("it", "test/it2.txt"),
    ("pl", "test/pl1.txt"),
    ("pl", "test/pl2.txt"),
    ("es", "test/es1.txt"),
    ("es", "test/es2.txt")
]

euclidean_ok = 0
taxi_ok = 0
max_ok = 0
cosine_ok = 0
effectiveness = []

for testfile in testfiles:
	print()
	print("Look for language: " + testfile[0])
	print("n = {}".format(n))
	testfile_ngrams = create_ngrams(testfile[1], n)

	# Euclidean space
	found_lang = ("", 10)
	print("Euclidean: ")
	for lang in languages:
	    langNgrams = lang[2]
	    e = euclidean(langNgrams, testfile_ngrams)
	    print(lang[0] + " : " + str(e))
	    if found_lang[1] > e:
	    	found_lang = (lang[0], e)
	print("Found language: " + found_lang[0])
	if found_lang[0] == testfile[0]:
		euclidean_ok += 1
	    	
	# Taxi space
	found_lang = ("", 10)
	print("Taxi: ")
	for lang in languages:
	    langNgrams = lang[2]
	    t = taxi(langNgrams, testfile_ngrams)
	    print(lang[0] + " : " + str(t))
	    if found_lang[1] > t:
	    	found_lang = (lang[0], t)
	print("Found language: " + found_lang[0])
	if found_lang[0] == testfile[0]:
		taxi_ok += 1

	# Maximum space
	found_lang = ("", 10)
	print("Max: ")
	for lang in languages:
	    langNgrams = lang[2]
	    m = maximum(langNgrams, testfile_ngrams)
	    print(lang[0] + " : " + str(m))
	    if found_lang[1] > m:
	    	found_lang = (lang[0], m)
	print("Found language: " + found_lang[0])
	if found_lang[0] == testfile[0]:
		max_ok += 1

	# Cosine space
	found_lang = ("", 10)
	print("Cosine: ")
	for lang in languages:
	    langNgrams = lang[2]
	    c = cosine(langNgrams, testfile_ngrams)
	    print(lang[0] + " : " + str(c))
	    if found_lang[1] > c:
	    	found_lang = (lang[0], c)
	print("Found language: " + found_lang[0])
	if found_lang[0] == testfile[0]:
		cosine_ok += 1

effectiveness = [
	("euclidean" , (euclidean_ok / len(testfiles))*100 ),
	("taxi" , (taxi_ok / len(testfiles))*100 ),
	("max" , (max_ok / len(testfiles))*100 ),
	("cosine" , (cosine_ok / len(testfiles))*100 ),
]
print(effectiveness)

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
#     langVector = normalize_vector(langVector)
#     testVector = normalize_vector(testVector)
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
    return 1 - spatial.distance.cosine(list(dict1.values()), list(dict2.values()))
     

languages = [
    ("en", "lang/english1.txt"),
    ("fi", "lang/finnish1.txt"),
    ("de", "lang/german1.txt"),
    ("it", "lang/italian1.txt"),
    ("pl", "lang/polish1.txt"),
    ("es", "lang/spanish1.txt")
]

n = 3
testfile = "test/polski.txt"
testfile_ngrams = create_ngrams(testfile, n)



# Euclidean space
print("Euclidean: ")
for lang in languages:
    langNgrams = create_ngrams(lang[1], n)
    e = euclidean(langNgrams, testfile_ngrams)
    print(lang[0] + " : " + str(e))

# Taxi space
print("Taxi: ")
for lang in languages:
    langNgrams = create_ngrams(lang[1], n)
    t = taxi(langNgrams, testfile_ngrams)
    print(lang[0] + " : " + str(t))

# Maximum space
print("Max: ")
for lang in languages:
    langNgrams = create_ngrams(lang[1], n)
    m = maximum(langNgrams, testfile_ngrams)
    print(lang[0] + " : " + str(m))

# Cosine space
print("Cosine: ")
for lang in languages:
    langNgrams = create_ngrams(lang[1], n)
    c = cosine(langNgrams, testfile_ngrams)
    print(lang[0] + " : " + str(c))

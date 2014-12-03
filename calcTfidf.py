#!/bin/env python
# encoding:utf-8
#
#
#
__Author__ =  "CORDEA"
__date__   =  "2014-11-29"


import os, sys, unicodedata
from sklearn.feature_extraction.text import TfidfVectorizer

with open(sys.argv[1]) as f:
    lines = f.readlines()

header = True
token_dict = {}
for line in lines:
    title = line.split("\t")[0]
    items = line.rstrip().split("\t")[1:]
    if header:
        tagList = [r.lower().replace("_", "") for r in items]
        header = False
    else:
        tmp = []
        for i in range(len(items)):
            if not float(items[i]) == 0.0:
                tmp.append(tagList[i])
        token_dict[title] = tmp

tfidf = TfidfVectorizer(tokenizer=lambda x: x.split("\t"))
tfs   = tfidf.fit_transform(["\t".join(r) for r in token_dict.values()])

for k, v in dict(zip(tfidf.get_feature_names(), tfidf._tfidf.idf_)).items():
    # for mecab
    k = unicodedata.normalize('NFKC', k)
    print(str(k.encode('utf-8')) + "\t" + str(v))

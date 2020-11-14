#!/usr/bin/env python

import csv
import metapy
import re
import emoji

# (1): Utility function to clean emojis/invalid chars
def clean_unicode(text):
    cleaned = re.sub(emoji.get_emoji_regexp(), r"", text)
    cleaned = re.sub(r"[^a-zA-Z0-9]+", ' ', cleaned)
    return cleaned

# MetaPy Data Cleaning
# MetaPy Examples: https://github.com/CS410Fall2020/MP1
# List Filter: wget -nc https://raw.githubusercontent.com/meta-toolkit/meta/master/data/lemur-stopwords.txt

# (2): Populating tweets from the scraped data.csv 
with open('data.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    tweets = []
    for row in readCSV:
        tweet = clean_unicode(row[2])
        tweets.append(tweet)

# (3): Cleaning
def clean(doc):
    tok = metapy.analyzers.ICUTokenizer(suppress_tags=True)
    tok = metapy.analyzers.LowercaseFilter(tok)
    tok = metapy.analyzers.LengthFilter(tok, min=2, max=5)
    tok = metapy.analyzers.Porter2Filter(tok)
    tok = metapy.analyzers.ListFilter(tok, "lemur-stopwords.txt", metapy.analyzers.ListFilter.Type.Reject)

    ana = metapy.analyzers.NGramWordAnalyzer(3, tok)
    trigrams = ana.analyze(doc)
    
    tok.set_content(doc.content())
    tokens, counts = [], []
    for token, count in trigrams.items():
        counts.append(count)
        tokens.append(token)
    return tokens

data = []
result_file = open("clean_data.csv",'wb')

for tweet in tweets:
    doc = metapy.index.Document()
    doc.content(tweet)
    result = clean(doc)
    data.append(result)

    wr = csv.writer(result_file, delimiter=',')
    for item in result:
        wr.writerow(item)

# if __name__ == '__main__':
# with open("clean_data.csv", "wt") as fp:
#     writer = csv.writer(fp, delimiter=",")
#     # writer.writerow(["your", "header", "foo"])  # write header
#     writer.writerows(data)
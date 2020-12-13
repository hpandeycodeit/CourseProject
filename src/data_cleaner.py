#!/usr/bin/env python
#%%

import csv
import metapy
import re
import emoji
import pandas

# (1): Utility function to clean emojis/invalid chars
def clean_unicode(text):
    cleaned = re.sub(emoji.get_emoji_regexp(), r"", text)
    cleaned = re.sub(r"[^a-zA-Z0-9@$# ]+", ' ', cleaned)
    return cleaned

# MetaPy Data Cleaning
# MetaPy Examples: https://github.com/CS410Fall2020/MP1
# List Filter: wget -nc https://raw.githubusercontent.com/meta-toolkit/meta/master/data/lemur-stopwords.txt

# (2): Populating tweets from the scraped data.csv 
def read_raw_tweets_from_file(input_fname):
    with open(input_fname) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        tweets, tstamps, authors = [], [], []
        for row in readCSV:
            tweet = clean_unicode(row[2])
            tweets.append(tweet)
            tstamps.append(row[1])
            authors.append(row[0])
    df = pandas.DataFrame({'author':authors[1:], 'tstamp':tstamps[1:], 'rawtweet':tweets[1:]})
    df.sort_values('tstamp').reset_index(drop=True)
    return(df)

# (3): Cleaning
def filter_tweets(df):
    df['tweet'] = ''
    for i, row in df.iterrows():
        # remove numbers and other special characters
        rawtweet = row['rawtweet']
        rawtweet = re.sub(r'[^A-Za-z@$# ]+', '', rawtweet)
        # metapy
        doc = metapy.index.Document()
        doc.content(rawtweet)
        tok = metapy.analyzers.ICUTokenizer(suppress_tags=True)
        tok = metapy.analyzers.LowercaseFilter(tok)
        tok = metapy.analyzers.LengthFilter(tok, min=2, max=30)
        tok = metapy.analyzers.Porter2Filter(tok)
        tok = metapy.analyzers.ListFilter(tok, "../lemur-stopwords.txt", metapy.analyzers.ListFilter.Type.Reject)
        tok.set_content(doc.content())
        df.loc[i, 'tweet'] = ' '.join(tok)
    return(df)
    

################
# MAIN
################
   
if __name__ == '__main__':

    #### parameters
    params = pandas.read_pickle('../data/params.pkl')
    input_data_file = params['input_data_file']
    #input_file = './data/RealTime2.csv'
    output_file = input_data_file.split('.csv')[0] + '.pkl'
    
    #### read tweets from file, remove emojis; store in rawtweet column
    df = read_raw_tweets_from_file(input_data_file)
    
    #### tokenize, lowercase, lengthfilter, Porter filter, remove stopwords in rawtweet; store in tweet column
    df = filter_tweets(df)

    #### convert dtypes
    df['tstamp'] = pandas.to_datetime(df.tstamp)
    
    #### write output file
    df.to_pickle(output_file, compression='zip')
    
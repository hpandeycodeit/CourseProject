#%%
import pandas

'''
tweet count analyzer
'''

def ngrammize_tweets(df, ngram_len):
    tokens, counts = [], []
    for i, row in df.iterrows():
        doc = metapy.index.Document()
        doc.content(row['tweet'])
        tok = metapy.analyzers.ICUTokenizer(suppress_tags=True)
        tok.set_content(doc.content())
        ana = metapy.analyzers.NGramWordAnalyzer(ngram_len, tok)
        trigrams = ana.analyze(doc)
        for token, count in trigrams.items():
            counts.append(count)
            tokens.append(token)
    return(tokens, counts)

def ngrammize_string(s, ngram_len):
    tokens, counts = [], []
    doc = metapy.index.Document()
    doc.content(s)
    tok = metapy.analyzers.ICUTokenizer(suppress_tags=True)
    tok.set_content(doc.content())
    ana = metapy.analyzers.NGramWordAnalyzer(ngram_len, tok)
    trigrams = ana.analyze(doc)
    for token, count in trigrams.items():
        counts.append(count)
        tokens.append(token)
    return(tokens, counts)

################
# MAIN
################
   
if __name__ == '__main__':

    #### parameters
    input_file = './data/RealTime2.pkl'

    #### read cleaned file
    df = pandas.read_pickle(input_file, compression='zip')
    
    #### calculate intervals for analysis
    interval_length_secs = 300
    st_time = df.tstamp.min()
    en_time = df.tstamp.max()
    intervals = pandas.interval_range(st_time, en_time, freq=f'{interval_length_secs}S')    
    
    # ngrammize tweets and count ngrams every 5 minutes
    out = []
    for interval in intervals:
        x = df[(df.tstamp > interval.left) & (df.tstamp <= interval.right)]
        tokens, counts = ngrammize_string(' '.join(list(x.tweet.values)), 3)
        t = pandas.DataFrame({'tokens':tokens, 'counts':counts})
        t = t.sort_values('counts')
        t['st_time'] = interval.left
        t['en_time'] = interval.right
        out.append(t)
        
        



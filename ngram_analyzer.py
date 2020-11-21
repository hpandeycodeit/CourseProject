#%%
'''
computes 2, 3, 4, and 5-grams of all tweets and plots trends of the top-20 tweets
in intervals of 5 minutes

the plots are saved as html/plotly files that can be seen from a browser
'''

import pandas
import metapy
import plotly.graph_objects as go

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

def compute_interval_ngrams(df, intervals, ngram_length):
    out = []
    for interval in intervals:
        x = df[(df.tstamp > interval.left) & (df.tstamp <= interval.right)]
        all_tweets_str = ' '.join(list(x.tweet.values))
        # remove http, https
        all_tweets_str = all_tweets_str.replace('https', '')
        all_tweets_str = all_tweets_str.replace('http', '')
        
        tokens, counts = ngrammize_string(all_tweets_str, ngram_length)
        t = pandas.DataFrame({'tokens':tokens, 'counts':counts})
        t = t.sort_values('counts')
        t['st_time'] = interval.left
        t['en_time'] = interval.right
        out.append(t)
    out = pandas.concat(out)
    return(out)

def plot_ngram_time_series_variation(out, save_figs_dir, ngram_length, number_to_plot=20):
    #### plot the top 20 currently most popular tokens through time
    top_tokens = out[out.st_time == out.st_time.max()].tail(number_to_plot).tokens.values
    fig = go.Figure()
    for token in top_tokens:
        x = out[out.tokens == token]
        fig.add_trace(go.Scatter(x = x.en_time, y = x.counts, name=', '.join(token)))
    
    fig.write_html(f'{save_figs_dir}/current-top20-{ngram_length}gram.html')
    
    #### plot the top 20 most popular tokens at the start
    top_tokens = out[out.st_time == out.st_time.min()].tail(number_to_plot).tokens.values
    fig = go.Figure()
    for token in top_tokens:
        x = out[out.tokens == token]
        fig.add_trace(go.Scatter(x = x.en_time, y = x.counts, name=', '.join(token)))
    
    fig.write_html(f'{save_figs_dir}/beginning-top20-{ngram_length}gram.html')
    return()


################
# MAIN
################
if __name__ == '__main__':

    #### read parameters
    params = pandas.read_pickle('./data/params.pkl')
    input_data_file = params['input_data_file']
    save_figs_dir = params['save_figs_dir']
    
    #### read cleaned file
    input_processed_file = input_data_file.split('.csv')[0] + '.pkl' # this is the file name used here
    df = pandas.read_pickle(input_processed_file, compression='zip')
    
    #### calculate intervals for analysis
    interval_length_secs = 300
    st_time = df.tstamp.min()
    en_time = df.tstamp.max()
    intervals = pandas.interval_range(st_time, en_time, freq=f'{interval_length_secs}S')    
    
    #### ngrammize tweets and count ngrams every 5 minutes
    #### here we plot 2-gram, 3-gram, 4-gram and 5-grams
    out = compute_interval_ngrams(df, intervals, 2)
    plot_ngram_time_series_variation(out, save_figs_dir, 2, 20)

    out = compute_interval_ngrams(df, intervals, 3)
    plot_ngram_time_series_variation(out, save_figs_dir, 3, 20)

    out = compute_interval_ngrams(df, intervals, 4)
    plot_ngram_time_series_variation(out, save_figs_dir, 4, 20)

    out = compute_interval_ngrams(df, intervals, 5)
    plot_ngram_time_series_variation(out, save_figs_dir, 5, 20)

    
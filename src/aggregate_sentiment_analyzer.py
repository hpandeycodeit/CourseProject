#%%
'''
aggregate sentiment
the plots are saved as html/plotly files that can be seen from a browser
'''

import pandas
import plotly.graph_objects as go
import textblob
import numpy

def compute_sentiment(df):
    df['polarity'] = 0
    df['subjectivity'] = 0
    for i, row in df.iterrows():
        polarity = textblob.TextBlob(row.tweet).sentiment.polarity
        subjectivity= textblob.TextBlob(row.tweet).polarity
        df.loc[i, 'polarity'] = polarity
        df.loc[i, 'subjectivity'] = subjectivity
    return(df)
    

def compute_interval_sentiment(df, intervals):
    out = []    
    for interval in intervals:
        x = df[(df.tstamp > interval.left) & (df.tstamp <= interval.right)]
        xx = x[x.tweet.str.contains('biden')]
        biden_polarity = xx.polarity.sum()
        biden_weighted_polarity = numpy.nansum(xx.polarity * (1 - xx.subjectivity))
        
        xx = x[x.tweet.str.contains('trump')]
        trump_polarity = xx.polarity.sum()
        trump_weighted_polarity = numpy.nansum(xx.polarity * (1 - xx.subjectivity))
        
        t = pandas.DataFrame({'biden_polarity':biden_polarity, \
                              'biden_weighted_polarity':biden_weighted_polarity, \
                              'trump_polarity':trump_polarity, \
                              'trump_weighted_polarity':trump_weighted_polarity, \
                              }, index=[0])
        t['st_time'] = interval.left
        t['en_time'] = interval.right
        out.append(t)
    out = pandas.concat(out)
    return(out)

def plot_aggregate_sentiment_time_series_variation(out, save_figs_dir):
    fig = go.Figure()
    x = out
    fig.add_trace(go.Scatter(x = x.en_time, y = x.biden_polarity, name='biden_polarity'))
    fig.add_trace(go.Scatter(x = x.en_time, y = x.trump_polarity, name='trump_polarity'))
    fig.write_html(f'{save_figs_dir}/biden_trump_polarity.html')
    
    fig = go.Figure()
    x = out
    fig.add_trace(go.Scatter(x = x.en_time, y = x.biden_weighted_polarity, name='biden_weighted_polarity'))
    fig.add_trace(go.Scatter(x = x.en_time, y = x.trump_weighted_polarity, name='trump_weighted_polarity'))
    fig.write_html(f'{save_figs_dir}/biden_trump_weighted_polarity.html')
    return()


################
# MAIN
################
if __name__ == '__main__':

    #### read parameters
    params = pandas.read_pickle('../data/params.pkl')
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
    
    #### net polarity every 5 minutes
    df = compute_sentiment(df)
    sentiment_outfile = input_data_file.split('.csv')[0] + '_sentiment.pkl'
    df.to_pickle(sentiment_outfile, compression='zip')
    out = compute_interval_sentiment(df, intervals)
    plot_aggregate_sentiment_time_series_variation(out, save_figs_dir)

    
    
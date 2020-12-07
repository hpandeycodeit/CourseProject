#%%
'''
aggregate sentiment
the plots are saved as html/plotly files that can be seen from a browser
'''

import pandas
from plsa import Corpus, Pipeline, Visualize
from plsa.pipeline import DEFAULT_PIPELINE
from plsa.algorithms import PLSA
import matplotlib.pylab as plt


################
# MAIN
################
if __name__ == '__main__':

    #### read parameters
    params = pandas.read_pickle('./data/params.pkl')
    input_data_file = params['input_data_file']
    save_figs_dir = params['save_figs_dir']
    n_topics = 10
  
    #### read cleaned file
    input_processed_file = input_data_file.split('.csv')[0] + '.pkl' # this is the file name used here
    df = pandas.read_pickle(input_processed_file, compression='zip')
    
    #### write csv file (so that plsa library can read it)
    csv_file = './data/biden_trump_tweets.csv'
    df['tweet'] = df.tweet.transform(lambda x : x.replace('https','').replace('http',''))
    df[['author', 'tstamp', 'tweet']].to_csv(csv_file, index=False)
    
    #### do PLSA analysis
    pipeline = Pipeline(*DEFAULT_PIPELINE)
    corpus = Corpus.from_csv(csv_file, pipeline, col=2)
    plsa = PLSA(corpus, n_topics, True)
    result = plsa.fit()
    visualize = Visualize(result)

    #### plot figures    
    fig = plt.figure(figsize=(9.4, 10))
    _ = visualize.wordclouds(fig)
    fig.savefig('./figures/html/plsa_wordcloud.jpeg')
    
    fig, ax = plt.subplots()
    _ = visualize.topics(ax)
    fig.tight_layout()
    plt.grid()
    fig.savefig('./figures/html/plsa_topicdistribution.jpeg')
    
    fig, ax = plt.subplots()
    _ = visualize.convergence(ax)
    fig.tight_layout()
    plt.grid()
    fig.savefig('./figures/html/plsa_KL_divergence.jpeg')
    
    
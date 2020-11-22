#%%
"""
main twitter project driver
"""
import pandas

if __name__ == '__main__':

    #### parameters
    print('saving parameter file')
    params = {}
    params['input_data_file'] = './data/RealTime2.csv'
    params['save_figs_dir'] = './figures/html/'
    pandas.to_pickle(params, './data/params.pkl') # we always read from here; don't change!!

    # call data_cleaner    
    print('cleaning data')
    exec(open('./data_cleaner.py').read())
    
    # call ngram_analyzer
    print('analyzing ngram frequencies')
    exec(open('./ngram_analyzer.py').read())
    
    # done
    print('done')
    
    
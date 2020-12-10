
## About the project

This project is about capturing sentiments on the data. The data that was used in this project was streamed through Twitter and mainly focued on the tweets during the Presidential Election 2020. 
Streaming the social media data like Twitter, gave us a dataset on the topic “Presidential Campaign” and then we processed the data to find and evaluate
the sentiments of the users on the Presidential Campaign.

## DATA Collection

Data was collected using the Twitter API and python code. The code "twitter_data.py" was run during the Presedential Election Night 2020 to collect the most relevant tweets and which covered the hashtags such as 'Elections2020', 'ElectionNight', 'Elections', 'Trump', 'Biden'. It roughly collected around 650K tweets

## Data Cleaning 

We used metapy to cleanup the data. We used the MeTA analysis toolkit to clean the raw data that was scraped from
Twitter. This involved using ‘stemming’ to treat base words as the same, in order
to reduce the amount of noise in the analysis.

## DATA Processing 

Current data is analyzed to create time-series of n-gram counts charts are plotted
and embedded into html files. These Plots contain the top-20 most popular ngrams.
We have computed for 2,3,4 and 5-grams. As per the proposal we have
created the initial Sentiment Analysis for Presidential Elections 2020.


## Run the project

Clone the project and follow the steps below: 


- Run python driver_twitter.py only. This python file does the following tasks: 

  1. It takes the input "RealTime2.csv" file 
  2. Cleans the Data by running "data_cleaner.py" 
  3. After, cleaning runs "ngram_analyzer.py" to analyze ngram frequencies
  4. Calculates the sentiments by running "aggregate_sentiment_analyzer.py" 
  5. Stores the charts/graphs in "./figures/html/" directory
 
## TOOLs/Languages

- Python
- Twitter API

  
 ## Team
 
 [Amrutha](https://github.com/amrutha97)\
 [Bala](https://github.com/balaksuiuc)\
 [Himanshu](https://github.com/hpandeycodeit)

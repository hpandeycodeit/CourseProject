
## About the project

This project provides a general framework for capturing sentiment trends from streamed twitter data. We demonstrate our software by capturing the US 2020 election related tweets, in the morning after the election, and applying n-gram frequency trends, and PLSA. The framework is written to be such that it is easy to add new modules, and perform new analytics. 

Using this dataset, we show that n-gram analysis captures many of the prominent characteristics of the election -- including "biden win", "claim victory", and "trump premature claim". We then apply a sentiment analysis, and show that the positive sentiment towards trump decreases between 840-1000 AM, while biden's positive sentiment marginally increases. Finally, we do a PLSA analysis on the data to identify the top-10 topics that are of the greatest importance. We show that the PLSA analysis captures biden's win in georgia, importance of swing states pennsylvania, and wisconsin, and vote count stop related messages. Interestingly, the top topic turned out to be "claims of a premature result".

This package can be used as a template for processing any other twitter data stream. 

## DATA Collection

Data was collected using the Twitter API and python code. The code "twitter_data.py" was run during the Presidential Election Night 2020 to collect the most relevant tweets that covered hashtags such as 'Elections2020', 'ElectionNight', 'Elections', 'Trump', 'Biden'. In all, we collected approximately 650K tweets.

## Data Cleaning 

We used metapy for initial clean up of the data. We used the MeTA analysis toolkit to clean the raw data that was scraped from Twitter. This involved using ‘stemming’ to treat base words as the same, in order to reduce the amount of noise in the analysis. One important aspect of this work is the necessity to remove "emojis". These contaminate the data, and create biases in the results. So, we removed any emojis with the text. 

## DATA Analysis

Current data is analyzed to create time-series of n-gram counts at 5 minute intervals. Clickable/zoomable charts are automatically generated, and embedded into html files. These Plots contain the top-20 most popular n-grams (for n=2,3,4,5). As per the proposal we have created the sentiment trend analysis results for the US presidential elections in 2020. Finally, PLSA analysis picks up the most salient topics. 


## Requirements

Check our requirements file for the required libraries and run pip install requirements.txt. Following are the required libraries for this project. 

- metapy
- emoji
- pandas
- plotly
- textblob

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
 
 
 ## Video Link
 [Presentation](https://mediaspace.illinois.edu/media/1_lh174zet)

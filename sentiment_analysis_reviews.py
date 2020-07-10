"""
Sentiment Analysis Google Play/Apple Reviews 

Author: Bob van de Mortel 
        Yilu Dai
Create date: April 1, 2020
Last edit: April 2, 2020, 11:51 PM

Purpose: Ingest reviews from a Google Play/Apple Store app and output sentiment on selected themes. Requires importing the raw data and a ngram-theme dictionary csv file that has been generated manually based on ngrams found in app reviews of the client bank.

Inputs: 1) raw reviews csv files, 2) ngram_theme_dictionary.csv
Output: 1) theme_sentiment.csv, 2) app_sentiment.csv
"""

############################### Choose parameters ###############################

### Choose parameters
#ngram_theme_dictionary_file = 'ngram_theme_dictionary.csv'
normalization_method = 'lemmatization' # method is 'stemming' or 'lemmatization'
use_spacy = True # True removes all words but adjectives and nouns by using spaCy langague model


### Import packages

# General

import os
import pandas as pd
import numpy as np

from collections import Counter
from tqdm import tqdm

# Text processing
import spacy
import nltk

from nltk.corpus import stopwords
from nltk.util import ngrams
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

##check directory and change it to where your output files are
import os
os.getcwd()
os.chdir('C:/Users/Yilu Dai/Desktop/scraper')

#### Load resources (run one time)
os.system('python -m spacy download en')
nltk.download('stopwords')
nltk.download('wordnet')



### Setup list
# Import list of banks to imput their .csv files
bank_list = [
            'ms',
            'etrade',
            'fidelity',
            'schwab',
            'pc',
            'marcus',
            'mymerrill',
            'merrilledge',
            'boa',
            'UBS',
            'power_etrade',
             'robinhood',
             'td'
            ]
#bank_counter = 0


#bank_name='ms'

#process the reviews 
##################################################################################
############################### Sentiment Analysis ###############################
##################################################################################
#'../GooglePlayScraper/out/' +
with pd.ExcelWriter('sentimen_out/apple/ouput.xlsx', engine='xlsxwriter') as writer:
    for bank_name in bank_list:
    
        ############################### Load data ###############################
        input_data_file = 'out/apple app/'+ bank_name + '.csv'
        df_raw = pd.read_csv(input_data_file)
        df = df_raw.copy()
    
    
        ############################### Clean data structure ###############################
    
        # Drop unneccesary columns
        df = df[['score','text']]#        
#        # Drop unneccesary rows (especaill apple scraps)
        df = df[df['score'] !='score']
        df['score']=df['score'].astype('float') 
        
        
        # Translate score into sentiment column. A review is positive (1) if it has a 5 star score and negative (-1) if it has a 1 or 2 star score.
        df['sentiment'] = df.score.apply(lambda x: 1 if x == 5 else (-1 if x <= 2 else 0))
    
        # Transform str objects in time column to datetime
#        df['date'] = pd.to_datetime(df.date)
    
    
        ############################### Clean text ###############################
    
        df['clean_text'] = df['text'].copy()
    
        # Remove unwanted symbols
        df['clean_text'] = df['clean_text'].str.replace("[^a-zA-Z#]", " ")
    
    
        # Make text lowercase
        df['clean_text'] = df.clean_text.apply(lambda x: str(x).lower())
    
    
        # Remove short words
        #parameter setting 
#        accepted_short_words = ['td', 'cc']
        df['clean_text'] = df['clean_text'].apply(lambda x: ' '.join([w for w in x.split() if ((len(w)>2) or (w in accepted_short_words))]))
    
    
        # Import stopwords dictionary
        stop_words = stopwords.words('english')
    
        # Fucntion to remove stopwords from a review
        def remove_stopwords(review):
            review_out = " ".join([word for word in review if word not in stop_words])
            return review_out
    
        # Apply function to remove stopwords to clean review text
        df['clean_text'] = df.clean_text.apply(lambda review: remove_stopwords(review.split()))
    
    
        # We can use spaCy for removing all words that are not nouns or adjectives. 
        if use_spacy:
            # Load spacy language model to disect the language in reviews
            nlp = spacy.load("en_core_web_sm", disable=['parser', 'ner'])
    
            # Define which wordtypes spacy should return (set to nouns, adjectives, proper nouns, and unknowns)
            tags=['NOUN', 'ADJ']
    
            # Using spacy we return the lemma's of the selected word types
            df['clean_text'] = df['clean_text'].apply(lambda review: " ".join([token.text for token in nlp(review) if token.pos_ in tags]))
        else:
            print('Did not use spacy. Check value use_spacy.')
    
    
        # Stemming or lemmatization
        if normalization_method == 'stemming':
            stemmer = PorterStemmer()
            df['clean_text'] = df['clean_text'].apply(lambda review: ' '.join([stemmer.stem(word) for word in review.split()]))
        elif normalization_method == 'lemmatization':
            # Use nltk WordNetLemmatizer to lemmatize words
            lemmatizer = WordNetLemmatizer()
            df['clean_text'] = df['clean_text'].apply(lambda review: ' '.join([lemmatizer.lemmatize(word) for word in review.split()]))
        else:
            print('No stemming or lemmatization applied. Check value normalization_method.')
    
    
        ############################### Create n-grams ###############################
    
        # Create ngrams of reviews to create meaninful word groupings
    
        # Defines functions to extract tokens/words, bigrams, and trigrams
        def tokenize(review):
            return review.split()
    
        def create_bigrams(tokens):
            return list(zip(tokens, tokens[1:]))
    
        def create_trigrams(tokens):
            return list(zip(tokens, tokens[1:], tokens[2:]))
    
        # Apply ngram functions and create new columns holding ngrams
        df['tokens'] = df.clean_text.apply(lambda review: tokenize(review))
        df['bigrams'] = df.tokens.apply(lambda tokens: [' '.join(tup) for tup in create_bigrams(tokens)])
        df['trigrams'] = df.tokens.apply(lambda tokens: [' '.join(tup) for tup in create_trigrams(tokens)])
        df['ngrams'] = df.tokens + df.bigrams + df.trigrams
    
    
        # Create complete corpa of all reviews for tokens, bigrams, trigrams and ngrams respectively
    
        # Defines function to create one corpus list from pandas series with a list at each entry
        def create_corpus(series):
            return [item for sublist in list(series) for item in sublist]
    
        # Create corpa for tokens, bigrams and trigrams
        token_corpus = create_corpus(df.tokens)
        bigram_corpus = create_corpus(df.bigrams)
        trigram_corpus = create_corpus(df.trigrams)
    
    
        ############################### Create frequency tables ###############################
    
        # Defines function to create dataframes of each corpus including frequency counts
        def corpus_to_counter_df(corpus, set_name):
            count = pd.DataFrame.from_dict(Counter(corpus), orient='index').reset_index().rename(columns={'index':'ngram', 0:'count'})
            count['set_name'] = set_name
            return count
    
        # Generate frequency dataframe for ngrams
        unigram_df = corpus_to_counter_df(token_corpus, 'uni-gram')
        bigram_df = corpus_to_counter_df(bigram_corpus, 'bi-gram')
        trigram_df = corpus_to_counter_df(trigram_corpus, 'tri-gram')
        ngram_df = pd.concat([unigram_df,bigram_df,trigram_df]).reset_index(drop=True)
    
    
        ############################### Create sentiment table ###############################
    
        # Defines function to retrieve tuples of negative, neutral and positive review sentiment counts for each ngram
        def get_sentiment_counts(ngram):
            return tuple(df.sentiment.loc[df.ngrams.apply(lambda x: ngram in x)].value_counts().reindex([-1,0,1], fill_value=0).sort_index().values)
    
        # Use tqdm to monitor progress in apply functions
        tqdm.pandas()
    
        # Create tuples containing sentiment counts for each of the ngrams
        sentiment_count_tuples = ngram_df.ngram.progress_apply(lambda ngram: get_sentiment_counts(ngram))
    
        # Convert the tuples into a sentiment dataframe
        temp_sentiment_df = pd.DataFrame(list(sentiment_count_tuples), columns = ['negative_count', 'neutral_count', 'positive_count'])
    
        # Join bank_sentiment_df to ngram_df and sort by count
        bank_sentiment_df = ngram_df.join(temp_sentiment_df).sort_values(by='count', ascending=False)
        
        ############################### Calculate overall app sentiment ###############################
        bank_app_sentiment_df = pd.DataFrame(df.sentiment.value_counts()).rename(columns = {'sentiment':bank_name}, index = {-1:'negative_count', 0:'neutral_count', 1:'positive_count'}).T
        bank_app_sentiment_df['count'] = bank_app_sentiment_df['negative_count'] + bank_app_sentiment_df['neutral_count'] + bank_app_sentiment_df['positive_count']
        bank_app_sentiment_df['negative_percentage'] = round(bank_app_sentiment_df['negative_count']/bank_app_sentiment_df['count'], 2)
        bank_app_sentiment_df['neutral_percentage'] = round(bank_app_sentiment_df['neutral_count']/bank_app_sentiment_df['count'], 2)
        bank_app_sentiment_df['positive_percentage'] = round(bank_app_sentiment_df['positive_count']/bank_app_sentiment_df['count'], 2)
        
        print(bank_name)
        bank_sentiment_df.to_excel(writer, sheet_name=bank_name+'bank_sentiment')
        bank_app_sentiment_df.to_excel(writer, sheet_name=bank_name+'bank_app_sentiment')
        
        
#check the output and run generate dictionarycode to create the theme dictionary
#set parameter
metrics='theme'   


journey_order = pd.DataFrame({'journey':['open a new account','access account','plan for investment',
                 'transfer','manage portfolio','check_performance','manage_account',
                 'receive service','resolve an issue','refer to a friend']})
    
theme_order = pd.DataFrame({'theme':['ui/ux','error-proof','charge-free',
                 'informed','trackable','watch out','personalization',
                 'speed']})

if (metrics=='journey'):
    order=journey_order
else:
    order=theme_order

importance=pd.DataFrame(columns =['bank',metrics,'count'])     
xls = pd.ExcelFile('sentimen_out/apple/ouput.xlsx')
with pd.ExcelWriter('result_out/apple/theme.xlsx', engine='xlsxwriter') as writer:
    for bank_name in bank_list:
        ### Group ngrams by theme
        # Read dictionary csv to translate ngrams to themes
        bank_sentiment_df=pd.read_excel(xls, bank_name+'bank_sentiment')
        #use the same dictionay 
        ngram_theme_dict_df = pd.read_csv('sentimen_out/google/ngram_theme_dictionary_file.csv')
    
        # Inner join of ngram_theme_dictionary_df to bank_sentiment_df
        bank_sentiment_df = pd.merge(left = ngram_theme_dict_df, right = bank_sentiment_df, left_on = 'ngram', right_on = 'ngram')
        #change parameters here 
        bank_theme_sentiment_df = bank_sentiment_df.groupby(metrics,as_index=False).sum()
        # sort journey by order
        bank_theme_sentiment_df=order.merge(bank_theme_sentiment_df, on=metrics,how='left')
        ### Calculate additional columns
    
        # Calculate the square root of the count column. To be used as width of bars in visualization.
        bank_theme_sentiment_df['count_squareroot'] = bank_theme_sentiment_df['count']**0.5
    
        # Calculate percentage negative and positive
        bank_theme_sentiment_df['negative_percentage'] = round(bank_theme_sentiment_df['negative_count']/bank_theme_sentiment_df['count'], 2)
        bank_theme_sentiment_df['positive_percentage'] = round(bank_theme_sentiment_df['positive_count']/bank_theme_sentiment_df['count'], 2)
        
        print(bank_name)

        bank_theme_sentiment_df.to_excel(writer, sheet_name=bank_name)
        bank_theme_sentiment_df['bank']=bank_name
        importance=pd.concat([importance,bank_theme_sentiment_df[['bank',metrics,'count']]])
        
importance.to_csv('result_out/apple/theme_importance.csv')       
##    # Add bank name column
##    bank_theme_sentiment_df['bank'] = bank_name
#
#    ############################### Concatenate to output ###############################
#
#    if bank_counter == 0:
#        theme_sentiment_df = bank_theme_sentiment_df
#        app_sentiment_df = bank_app_sentiment_df
#    else:
#       theme_sentiment_df = pd.concat([theme_sentiment_df, bank_theme_sentiment_df])
#       app_sentiment_df = pd.concat([app_sentiment_df, bank_app_sentiment_df])
#    bank_counter += 1
#
#    print(bank_name)
#    ### End for loop
#
#
################################ Write output ###############################
#
#theme_sentiment_df.to_csv('out/theme_sentiment.csv')
#app_sentiment_df.to_csv('out/app_sentiment.csv')
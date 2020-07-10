# -*- coding: utf-8 -*-
"""
Created on Tue May 19 20:53:32 2020

@author: Yilu Dai
"""
import os
import pandas as pd
import numpy as np
from PIL import Image
from wordcloud import WordCloud
os.chdir('C:/Users/Yilu Dai/Desktop/scraper')

bank_list = [
            'ms',
            'etrade',
#            'capitalone',
#            'discover',
#            'amex',
#            'pnc'
            ]


for bank_name in bank_list:
    input_data_file = 'out/'+ bank_name + '.csv'
    df_raw = pd.read_csv(input_data_file)
    df = df_raw.copy()      

    ############################### Clean data structure ###############################
    # Drop unneccesary columns
    df = df[['date','score','text']]
    
    # Translate score into sentiment column. A review is positive (1) if it has a 5 star score and negative (-1) if it has a 1 or 2 star score.
    df['sentiment'] = df.score.apply(lambda x: 1 if x == 5 else (-1 if x <= 2 else 0))
    
    # Transform str objects in time column to datetime
    df['date'] = pd.to_datetime(df.date)
    
    
    ############################### Clean text ###############################
    
    df['clean_text'] = df['text'].copy()
    
    # Remove unwanted symbols
    df['clean_text'] = df['clean_text'].str.replace("[^a-zA-Z#]", " ")
    
    
    # Make text lowercase
    df['clean_text'] = df.clean_text.apply(lambda x: str(x).lower())
    
    
    # Remove short words
    #parameter setting 
    accepted_short_words = ['td', 'cc']
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
    
    df_positive=df[df['sentiment']==1] 
    df_negative=df[df['sentiment']==-1] 
        
    text_positive = " ".join(text for text in df_positive.clean_text )
    text_negative = " ".join(text for text in df_negative.clean_text)
    print ("There are {} words in the combination of all review.".format(len(text_positive)))
    print ("There are {} words in the combination of all review.".format(len(text_negative)))

    wordcloud_positive = WordCloud(stopwords=['app'],width=800, height=800,background_color="white").generate(text_positive)
    wordcloud_negative = WordCloud(stopwords=['app'],width=800, height=800,background_color="white").generate(text_negative)
    plt.figure(figsize=(20,10)) 
    plt.imshow(wordcloud_positive)
    plt.axis("off")
    plt.savefig('out/'+ bank_name+'_positive')
    plt.close()
    
    plt.figure(figsize=(20,10)) 
    plt.imshow(wordcloud_negative)
    plt.axis("off")
    plt.savefig('out/'+ bank_name+'_negative')
    plt.close()
        



    
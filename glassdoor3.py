import pandas as pd
import string
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer 
from nltk import word_tokenize
import math
import os
import sys

lemmatizer = WordNetLemmatizer()


def main():

    if len(sys.argv)!=2:
        sys.exit("Filename Not Entered")

    #all files with there words
    files = file_words_def()

    #all idfs values of there words
    idfs = idfs_def(files)

    #every review with there words
    review_data = load_data_indeed_world()   

    df = pd.read_csv(f'Training Files/{sys.argv[1]}.csv')
    categories = []
    N = len(df)
    for i in range(N):
        # print(review_data[i][1])
        filenames = categorize(review_data[i][1], files, idfs, n=1)
        # print(filenames)
        filename = str(filenames[0]).replace('.txt','')

        categories.append(filename)

    df['Categories'] = categories
    # print(df)
    df.to_csv(os.path.join('Final Csvs','Categories_Indeed_Worldwide.csv'),index=False)


def get_stopwords():
    stopword = set(stopwords.words('english'))
    return stopword

def get_functional_words():
    functional_words=[]
    with open('function_words.txt') as f:
        readline=f.read().split("\n")
        functional_words.append(readline)
    return functional_words

def tokenize(sentence):
    words = word_tokenize(sentence)
    return words

def lemmatize_words(words):
   lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
   return lemmatized_words

def file_words_def():
    file_words={}
    topics = load_topics('Topics')
    for file in topics:
         file_words[file] = lemmatize_words(cleaned(tokenize(topics[file])))
         
    return file_words

def cleaned(words):
    stopword = get_stopwords()
    functional_words = get_functional_words()
    cleaned_words = [x.lower() for x in words if x.lower() not in stopword and functional_words and x.isalpha() ]
    
    return cleaned_words

def idfs_def(file_word_dict):
    list_of_words={}
    idfs={}
    for file in file_word_dict:
        for word in file_word_dict[file]:
            if word in list_of_words:
                list_of_words[word] +=1
            else:
                list_of_words[word] = 1
    
    N = len(file_word_dict)
    for word in list_of_words:
        doc_cont_word = 0
        for doc_words in file_word_dict.values():
            if word in doc_words:
                doc_cont_word +=1
        idf = math.log(N/doc_cont_word)
        idfs[word] = idf

    # N = len(file_word_dict)
    # for word in list_of_words:
    #     doc_cont_word =0
    #     for doc_words in file_word_dict.values():
    #         if word in doc_words:
    #             doc_cont_word +=1

    #     idfs[word] = math.log(N/doc_cont_word)

    # idfs = dict(sorted(idfs.items(),key=lambda item: item[1],reverse=True))
   
    return idfs

def load_data_glassdoor():
    df = pd.read_csv('Glassdoor.csv')
    cleaned_data = []
    
    for i in range(len(df)):
        title = df['title'][i]
        pros = df['pros'][i]
        cons = df['cons'][i]
        cleaned_info = str(title) + ',' +  str(pros) + ','+ str(cons)
        cleaned_info = cleaned(tokenize(cleaned_info))
        cleaned_info = lemmatize_words(cleaned_info)
        cleaned_data.append([i,cleaned_info])

    return cleaned_data

def load_data_indeed_world():
    df = pd.read_csv('Indeed_Worldwide.csv')
    cleaned_data=[]
    
    for i in range(len(df)):
        title = df['Title'][i]
        description = df['Description'][i]
        pros = df['Pros'][i]
        cons = df['Cons'][i]
        cleaned_info = str(title) + ',' + str(description) + ',' + str(pros) + ',' + str(cons)
        cleaned_info = cleaned(tokenize(cleaned_info))
        cleaned_info = lemmatize_words(cleaned_info)
        cleaned_data.append([i,cleaned_info])
        
    return cleaned_data

def categorize(review,files,idfs,n):
    categories=[]
    for file in files:
        score=0
        for word in review:
            if word in files[file]:
                score += idfs[word] * files[file].count(word)
        categories.append((file,score))
    categories.sort(key=lambda x : x[1],reverse=True)
    return [top[0] for top in categories[:n]]

def load_topics(directory):
    topics={}
    for file in os.listdir(directory):
        with open(os.path.join(directory,file),encoding='utf-8') as data:
            topics[file] = data.read()
    return topics




if __name__ =="__main__":
    main()
    
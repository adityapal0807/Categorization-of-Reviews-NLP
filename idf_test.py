import pandas as pd
import string
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer 
lemmatizer = WordNetLemmatizer()
from nltk import word_tokenize
import math
import os

def main():
    files = file_words_def()
    
    idfs = idf_test(files)
    

def file_words_def():
    file_words={}
    topics = load_topics('Topics')
    for file in topics:
        file_words[file] = lemmatize_words(cleaned(tokenize(topics[file])))
    return file_words
    
def idf_test(file_word_dict):
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
    

def load_topics(directory):
    topics={}
    for file in os.listdir(directory):
        with open(os.path.join(directory,file),encoding='utf-8') as data:
            topics[file] = data.read()
    return topics

def cleaned(words):
    stopword = get_stopwords()
    functional_words = get_functional_words()
    cleaned_words = [x.lower() for x in words if x.lower() not in stopword and functional_words and x.isalpha() ]
    
    return cleaned_words

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

if __name__ == '__main__':
    main()
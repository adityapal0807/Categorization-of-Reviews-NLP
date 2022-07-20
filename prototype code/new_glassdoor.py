import pandas as pd
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer 
lemmatizer = WordNetLemmatizer()
from nltk import word_tokenize
import math
import gensim
from gensim.models import Word2Vec



CATEGORIES = {
    'hr':'Human Resources',
    'technology': 'Technology',
    'culture': 'Culture',
    'management':'Management'

}

def main():

    for i in range(10):
        print(tfs_idfs(i))

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


def lemmetize_words(words):
   lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
   return lemmatized_words


def cleaned(words):
    stopword = get_stopwords()
    functional_words = get_functional_words()
    cleaned_words = [x.lower() for x in words if x.lower() not in stopword and functional_words and x.isalpha()]
    # cleaned_without_duplicates = []
    # for x in cleaned_words:
    #     if x not in cleaned_without_duplicates:
    #         cleaned_without_duplicates.append(x)
    return cleaned_words

def load_data():
    df = pd.read_csv('Glassdoor.csv')
    cleaned_data = []
    
    for i in range(len(df)):
        title = df['title'][i]
        pros = df['pros'][i]
        cons = df['cons'][i]
        cleaned_info = str(title) + ',' +  str(pros) + ','+ str(cons)
        cleaned_info = cleaned(tokenize(cleaned_info))
        cleaned_info = lemmetize_words(cleaned_info)
        cleaned_data.append([i,cleaned_info])

    return cleaned_data

def words_to_count():
    word_count = {}
    datas = load_data()
    for data in datas:
        for word in data[1]:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1

    word_count = dict(sorted(word_count.items(),key=lambda item: item[1],reverse=True))
    return word_count

def tf_def(id):
    tf={}
    datas = load_data()
    for data in datas:
        if data[0] == id:
            words = data[1]
    for word in words:
        if word in tf:
            tf[word] +=1
        else:
            tf[word] = 1
    tf = dict(sorted(tf.items(),key=lambda item: item[1],reverse=True))
    return tf

def bagofwords():
    bagofwords = []
    datas = load_data()
    for data in datas:
        for words in data[1]:
            bagofwords.append(words)
    return bagofwords

def idf_def():
    idfs={}
    bagofword = bagofwords()
    datas = load_data()
    N = len(load_data())
    for word in bagofword:
        no_of_docs_cont = 0
        for data in datas:
            for item in data[1]:
                if word in item:
                    no_of_docs_cont +=1
                    break
        idfs[word] = math.log(N/no_of_docs_cont)
    idfs = dict(sorted(idfs.items(),key=lambda item: item[1],reverse=True))
    return idfs

def tfs_idfs(id):
    tf_idf={}
    tf = tf_def(id)
    idfs = idf_def()
    datas = load_data()
    for data in datas:
        if data[0] == id:
            words = data[1]
            for word in words:
                tf_idf[word] = tf[word] * idfs[word]
    
    tf_idf = dict(sorted(tf_idf.items(),key=lambda item: item[1],reverse=True))
    return tf_idf


def wordnet_def(word):
    synonyms=[]
    for syn in wordnet.synsets("Culture"):
        for l in syn.lemmas():
            synonyms.append(l.name())
            

    print(synonyms)



def score():
    pass
    

    

if __name__ =="__main__":
    main()
    
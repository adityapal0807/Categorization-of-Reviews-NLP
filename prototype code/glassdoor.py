import pandas as pd
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk import word_tokenize
import math



CATEGORIES = {
    ''

}

def main():
    dataset = []
    #calculate tf individually for all the words of a particular review
    for i in range(10):
        data={}
        data['review_id'] = i
        data['TF-IDFS'] = tf_idf(i)
        dataset.append(data)
    final = pd.DataFrame(dataset)
    final.to_csv('Final.csv')



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

def cleaned(words):
    stopword = get_stopwords()
    functional_words = get_functional_words()
    cleaned_words = [x.lower() for x in words if x.lower() not in stopword and functional_words and x.isalpha()]
    # cleaned_without_duplicates = []
    # for x in cleaned_words:
    #     if x not in cleaned_without_duplicates:
    #         cleaned_without_duplicates.append(x)
    return cleaned_words

def load_data(filename):
    df = pd.read_csv(filename)
    return df

def termfrequency_for_words():
    tf={}
    df = update_csv()
    pros = df['pros']
    cons=df['cons']
    for pro in pros:
        for word in pro:
            if word in tf:
                tf[word] +=1
            else:
                tf[word] = 1

    return tf

def show_tf():
    tf = termfrequency_for_words()
    sorted_tf = dict(sorted(tf.items(),key=lambda item: item[1],reverse=True))
    print(sorted_tf)

    
def tf(id):
    df = all_reviews_mapping()
    tf_list={}
    pros = df[id]
    N = len(pros)
    for word in pros:
        count = pros.count(word)
        tf_list[word] = count/N
        
    return tf_list

def idf():
    idf={}
    mapping = all_reviews_mapping()
    all_words = bagofwords()
    df = update_csv()
    N = len(df)
    for word in all_words:
        no_of_doc_cont = 0
        for map in mapping:
            for all_word in mapping[map]:
                if word in all_word:
                    no_of_doc_cont +=1

        idf[word] = math.log(N/no_of_doc_cont)
    return idf
    
def tf_idf(id):
    tf_idf = {}
    idfs = idf()
    tf_value = tf(id)
    mapping = all_reviews_mapping()
    mapped = mapping[id]
    for words in mapped:
        tf_idf[words] = tf_value[words] * idfs[words]
    sorted_tf_idf = dict(sorted(tf_idf.items(),key=lambda item: item[1],reverse=True))
    return sorted_tf_idf

    


def bagofwords():
    bagofword=[]
    all_words = termfrequency_for_words()
    for word in all_words:
        bagofword.append(word)
    return bagofword

    

def all_reviews_mapping():
    mapping = {}
    df = update_csv()
    ids = df['id']
    for i in range(len(df)):
        mapping[ids[i]] = df['pros'][i]
    return mapping

def update_csv():
    df = load_data('Glassdoor.csv')
    columns = ['pros','cons']
    for i in range(len(df)):
        for col in columns:
            df[col][i] = cleaned(tokenize(df[col][i]))
            #print(df[col][i])

    #df.to_csv('Updated.csv')
    return df
    



    

if __name__ =="__main__":
    main()
    
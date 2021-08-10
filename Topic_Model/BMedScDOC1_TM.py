import os
import csv
#topic model using NMF
import pandas as pd
#import gensim
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import sys

csv.field_size_limit(sys.maxsize)

#main function
def main():
    path = input("Path to txt files folder: ")
    #txt_lst is a list of all the txt files in our path folder
    # make a csv file headers: PMID, Text, len of text
    # NMF
    make_csv(path)
    
    docs=pd.read_csv('corpus.csv', encoding = 'unicode_escape', encoding_errors = 'ignore', engine ='c')
    # use tfidf by removing tokens that don't appear in at least 50 documents
    vect = TfidfVectorizer(min_df=2, stop_words='english')
    # Fit and transform
    X = vect.fit_transform(docs.Text)
    
    # Create an NMF instance: model
    # the empircal 10 components will be the topics
    model = NMF(n_components=20, random_state=5)
    # Fit the model to TF-IDF
    model.fit(X)
    # Transform the TF-IDF: nmf_features
    nmf_features = model.transform(X)
    X.shape
    nmf_features.shape
    model.components_.shape
    components_df = pd.DataFrame(model.components_, columns=vect.get_feature_names())
    components_df
    
    for topic in range(components_df.shape[0]):
        tmp = components_df.iloc[topic]
        print(f'For topic {topic+1} the words with the highest value are:')
        print(tmp.nlargest(20))
        print('\n')
    
    
        

#get a corpus of texts from folder and separate its .txt files
def get_corpus(basepath):
    lst = os.listdir(basepath)
    lst.sort()
    newlst = []
    for file in lst:
        check = file
        path = os.path.abspath(check)
        ext = os.path.splitext(path)[-1].lower()
        if ext == ".txt":
            newlst.append(check)
    return newlst


#make a csv file from a folder of txts
def make_csv(folder_path):
    txt_lst = get_corpus(folder_path) #list
    
    headers = ["PMID", "Text"]
    PMID = txt_lst
    Text = []
    Length = []
    
    with open('corpus.csv', 'w', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        
        for i in range(len(txt_lst)):
            filepath = folder_path + "/" + txt_lst[i]
            with open(filepath, 'r') as contents:
                string = contents.read()
                string.replace("\n", " ")
                string.encode('unicode_escape')
                data = [txt_lst[i], string]
                writer.writerow(data)
                
        

main()
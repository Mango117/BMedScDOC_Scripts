#BMedSc DOC v7.2 script
#The aim of this script is to transpose a corpus of pdf studies into a txt
#Then run a search for specific terms from a dictionary within the txt file
#Inputs: Python program + Dictionary + subdir for corpus of texts, all of which must be within the same dir
#Outputs: bar graph of all dictionary terms + BoW of corpus
#Outputs: term document matrix as a csv in downloads

#Usage: python BMedScDOC1_v7.2.py [dictionary.txt] [corpus path] [csv.path]


import os
import sys
import re
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud
from gensim.parsing.preprocessing import remove_stopwords
from nltk.tokenize import word_tokenize
import spacy
from tika import parser

os.environ['KMP_DUPLICATE_LIB_OK']='True'
nlp = spacy.load("en_core_web_sm", disable=['parser', 'ner'])



dictionary = []
combined = [] #For pathway 2 - total dictionary list
docs = []

#main function
def main():
    if __name__ == '__main__':
        if len(sys.argv) != 4: #This needs to be changed to 3 soon
            print('Usage: python BMedScDOC1_v7.2.py [dictionary.txt] [corpus_path] [csv.path]')
            sys.exit(1)
        doc_list = get_corpus(sys.argv[2]) #list of the texts in corpus
        print("\n Corpus List: ", doc_list)
        dictionary = makedict(sys.argv[1]) #Make the dictionary
        print("\n Dictionary terms: ", dictionary)

    
        for i in range(len(doc_list)):
            action(i, doc_list, dictionary)
        
        
        #print BoW
        print(">>>>Combined BoW:", "(", len(combined), "):\n", combined, "\n")
    
        #print list of strings for tdm
        print(doc_list)
        print(docs)
    
        #make a term-document matrix
        df = tdm_make(docs) 
        print("tdm: \n", df)
    
        #convert pandas dataframe to csv
        location = input("Please enter the Path to directory where outputs should be saved. \n ie: /Users/manojarachige/Downloads/ \n Path: ")
        df.to_csv(r'{}TDM.csv'.format(location))
        
        #replace with Display words
        #for_display is the combined list, substituted for display words from csv
        for_display = display(combined, sys.argv[3])
        print("Words For Display >>>", for_display)
    
        #Make bar chart with totals and convert to png
        barchart(for_display, location)
    
        #create wordcloud and convert to png
        wc(for_display, location)
        

#shows a barchart and also saves it
def barchart(combined, location):
    total = Counter(combined).most_common()
    print("Total>>>", total)
    chart = plotwords(total)
    chart.savefig('{}Bar.png'.format(location))
    plt.show()


#creates a wordcloud with a list of words
def wc(combined, location):
    total = Counter(combined).most_common()
    
    brain_mask = np.array(Image.open("head.png"))
    
    dict_for_wc = dict(total)
    wordcloud = WordCloud(background_color="white", colormap="plasma", mask=brain_mask, contour_width=3, contour_color='firebrick').generate_from_frequencies(dict_for_wc)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    wordcloud.to_file('{}freq_WordCloud.png'.format(location))
      


#get folder path and print alphanum sorted list of files
def get_corpus(folder):
    basepath = folder
    lst = os.listdir(basepath)
    lst.sort()
    print("full list", lst)
    for file in lst:
        check = file
        path = os.path.abspath(check)
        ext = os.path.splitext(path)[-1].lower()
        if ext != ".pdf":
            lst.remove(file)
    return lst
        

#Make dictionary list from txt file

def makedict(textfile):
    with open(textfile, 'r') as file:
        dictionary = file.read().replace('\n', ' ')
        dictionary = dictionary.lower().split()
        return dictionary

#Remove references from the end of the file

def remove_ref(text):
    f = open(text,"r")
    openfile = f.read()
    newfile = openfile.lower()
    if "references" in newfile:
        finder = newfile.rfind("references")
        newfile = newfile[:finder]
    f.close()
    n = open(text,"w")
    n.write(newfile)
    n.close()

    
#Convert a pdf to a txt file and remove references. Arg (text) is a file path to pdf

def pdftotxt(text):
    with open("{}.txt".format((text)[:-4]), "w") as output:
              raw = parser.from_file(text)
              string = raw["content"]
              if string == None:
                string = "None"
              output.write(string)
    remove_ref("{}.txt".format((text)[:-4])) 
    return "{}.txt".format((text)[:-4]) 



#Preprocess text from string

def preprocess(string, csv_path):
    
    #remove line breaks
    #lemmatise
    lemmatised = nlp(string.replace("\n", " ").replace("\r", " "))
    lemmatised = " ".join([token.lemma_ for token in lemmatised])
    
    #remove stopwords
    stopwords_removed = remove_stopwords(lemmatised)
    
    #replace
    df = pd.read_csv(csv_path)
    replaced = stopwords_removed
    for i in range(len(df)):
        replaced = replaced.replace(df["Location"][i], df["Replacement"][i])
        #print("executed {}".format(i))
        
    #tokenise
    tokenised = word_tokenize(replaced)

    return tokenised

#substitutes words in combined[] with replacement csv words
def display(combined, csv_path):
    df = pd.read_csv(csv_path)
    for i in range(len(df)): #python replace items in a loop
        for j in range(len(combined)):
            if df["Replacement"][i] == combined[j]:
                combined[j] = df["Display"][i]
    return combined
        
    

#Create list of words appearing in txt file 
def maketxt(text, csv_path):
    string = ''
    with open(text) as file:
        string = file.read()
        return preprocess(string, csv_path)



    
#Remove words not in the dictionary NOTE: Will find words within words ie. bar within bars
def rem_dict(dictionary, doc):
    new_doc = []
    for i in range(len(doc)):
        for j in range(len(dictionary)):
            if dictionary[j] in doc[i]:
                new_doc.append(dictionary[j])
    return new_doc




#plot words in a bar graph

def plotwords(list_of_tuples):
    plotdata = ([ a for a,b in list_of_tuples ], [ b for a,b in list_of_tuples ])

    #split x and y axis values into separate lists
    words = plotdata[0]
    occurrences = plotdata[1]

    #use pyplot the graph
    plt.figure(figsize=(20, 5))
    plt.plot()
    plt.bar(words, occurrences, width = 0.8, align = 'center', )
    plt.xticks(rotation=90)

    #title and labels for graph
    plt.title("BMedScDOC words in corpus")
    plt.ylabel("Number of occurrences")
    plt.xlabel("Words from dictionary")
    #all done!
    return plt


#make tdm

def tdm_make(docs):
    vec = CountVectorizer()
    X = vec.fit_transform(docs)
    df = pd.DataFrame(X.toarray(), columns=vec.get_feature_names())
    return df


#i is counter, doc_list is a list of all docs in corpus, and dictionary is a list of words from dict
def action(i, doc_list, dictionary):
    print("Doc {}".format(i + 1), "out of {}".format(len(doc_list)))
    print("{}".format(doc_list[i]))
    
    text = maketxt(pdftotxt("{}".format(sys.argv[2]) + "/{}".format(doc_list[i])), sys.argv[3]) 
        
    #remove non-dictionary words
    text = rem_dict(dictionary,text)  
        
    #add to Total List for Combined BoW later
    combined.extend(text) 
        
    #check corpus doc again
        
    #add to list of text strings for tdm
    doc_for_tdm = " ".join(text)
    docs.append(doc_for_tdm)
    #print individual document texts
    print("Length", "(", len(text), "):\n", text, "\n")



main()
#List of reusable functions that may be called in BMedScDOC_Scripts

#imports
import os
import sys
import progressbar
import shutil 
from collections import Counter
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
from pathlib import Path

downloads_path = str(Path.home() / "Downloads") + "/" #Find Downloads folder path
os.environ['KMP_DUPLICATE_LIB_OK']='True'
nlp = spacy.load("en_core_web_sm", disable=['parser', 'ner'])




#functions
class outputs:
    #Action: Creates a Barchart from a list of words and saves it to computer
    #Input: A list of strings ie.[word1, word2]
    #Input: Path to save location ie. "usr/Documents/Folder" default is downloads folder
    #Output: prints the list of tuples [total], displays barchart and saves a Bar.png to save_location
    def barchart(list, save_location = downloads_path):
        total = Counter(list).most_common()
        print("Total>>>", total)
        chart = outputs.plotwords(total)
        chart.savefig('{}Bar.png'.format(save_location))
        plt.show()
        
    
    #Action: Creates a Barchart from a list of words and displays it
    #Input: A list of tuples ie.[(word1, 2),  (word2, 3)]
    #Output: Displays barchart 
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
    

    #Action: Creates a wordcloud from a list of words
    #Input: A list of strings ie.[word1, word2]
    #Input: Path to image mask ie. "usr/Documents/Folder" default is head.png
    #Input: Path to save location ie. "usr/Documents/Folder" default is downloads folder
    #Output: Saves a freq_WordCloud.png to save_location
    def wc(list, shape_path = "/Users/manojarachige/Documents/Coding/BMedScDOC1/Assets/head.png", save_location = downloads_path):
        total = Counter(list).most_common()
    
        brain_mask = np.array(Image.open(shape_path))
    
        dict_for_wc = dict(total)
        wordcloud = WordCloud(background_color="white", colormap="plasma", mask=brain_mask, contour_width=3, contour_color='firebrick').generate_from_frequencies(dict_for_wc)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        wordcloud.to_file('{}freq_WordCloud.png'.format(save_location))
        
    
    #Action: Converts a list of text strings into a df tdm
    #Input: list of strings, with each string being a "document" for the term-document matrix
    #Output: pandas df of a tdm
    def tdm_make(docs):
        vec = CountVectorizer()
        X = vec.fit_transform(docs)
        df = pd.DataFrame(X.toarray(), columns=vec.get_feature_names())
        return df
    
    
    #Action: Make a csv file from a folder of txts, with 2 columns: [Name] and [Text]
    #Input: path to folder of txt files
    #Output: csv with 2 columns saved to the current directory. csv has 2 columns: [Name] and [Text]
    def make_csv(folder_path):
        txt_lst = os_level.get_corpus(folder_path) #list
    
        headers = ["Name", "Text"]
        Name = txt_lst
        Text = []
    
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
      

class processing:
    #Action: Splits stirng following an instance of "References" in a txt file
    #Input: path to txt file with a references section ie. "usr/Documents/File" 
    #Output: modifies txt file by lowering it and removing references
    def remove_ref(text):
        f = open(text,"r")
        openfile = f.read()
        newfile = openfile.lower()  #lowers the file just in case
        if "references" in newfile:
            finder = newfile.rfind("references")
            newfile = newfile[:finder]
        f.close()
        n = open(text,"w")
        n.write(newfile)
        n.close()



    def preprocess(string, csv_path):
        #Action: Performs preprocessing of the string
        #Input: string to be modified
        #Output: list of preprocessed string ie.[preprocessed, words]
        
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
    
    
    
    #Action: Converts a pdf file to a txt file and removes references
    #Input: a single PDF file
    #Output: a single txt file of the same filename 
    def pdftotxt(text):
        with open("{}.txt".format((text)[:-4]), "w") as output:
            raw = parser.from_file(text)
            string = raw["content"]
            if string == None:
                string = "None"
                output.write(string)
        processing.remove_ref("{}.txt".format((text)[:-4])) #removes references in this step
        return "{}.txt".format((text)[:-4]) 


class os_level:
    #Action: Returns a list of files in a folder of a specified file type
    #Input: path to folder of files
    #The extension of the file type you want
    #Output: list of the names of 
    def get_corpus(folder, extension):
        lst = os.listdir(basepath, extension)
        lst.sort()
        newlst = []
        for file in lst:
            check = file
            path = os.path.abspath(check)
            ext = os.path.splitext(path)[-1].lower()
            if ext == "." + extension:
                newlst.append(check)
        return newlst
    
    #Action: Creates a list of words that are in a txt file, removing line breaks
    #Input: path to txt file
    #Output: list of words in txt file
    def makedict(textfile):
        with open(textfile, 'r') as file:
            dictionary = file.read().replace('\n', ' ')
            dictionary = dictionary.lower().split()
            return dictionary
        
    #Action: Checks if a file is a valid and working pdf
    #Input: path to pdf
    #Output: Boolean True if valid PDF
    def isFullPdf(f):
        end_content = ''
        start_content = ''
        size = os.path.getsize(f)
        if size < 1024: return False 
        with open(f, 'rb') as fin: 
            #start content 
            fin.seek(0, 0)
            start_content = fin.read(1024)
            start_content = start_content.decode("ascii", 'ignore' )
            fin.seek(-1024, 2)
            end_content = fin.read()
            end_content = end_content.decode("ascii", 'ignore' )
        start_flag = False
        #%PDF
        if start_content.count('%PDF') > 0:
            start_flag = True
    
        
        if end_content.count('%%EOF') and start_flag > 0:
            return True
        eof = bytes([0])
        eof = eof.decode("ascii")
        if end_content.endswith(eof) and start_flag:
            return True
        return False
    
    
    
    #Action: Iterates over a source folder of pdfs and separates the valid ones to output_location
    #Input: source is a string path to folder of pdfs
    #Input: output_location is a string path to output location of successfully separated pdfs
    #Output: Copies valid pdfs to a specified output_location
    def pdf_separate(source, output_location):
        separated_counter = 0
        time_counter = 0
        pdf_list = os_level.get_corpus(source)
        length = len(pdf_list)
        with progressbar.ProgressBar(max_value=length, redirect_stdout=True) as p:
            for i in pdf_list:
                if os_level.isFullPdf(source + "/" + i) == True:
                    shutil.copy2(source + "/" + i, output_location)
                    separated_counter += 1
                p.update(time_counter)
                time_counter += 1
            
            
        print(separated_counter, "files separated out of ", len(pdf_list), "source files" )
            
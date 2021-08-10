#Loop over a folder of txt abstracts and do a count of all the words 
#count words and output bar chart + tdm + wordcloud
#Replacement Path: /Users/manojarachige/Documents/Coding/BMedScDOC1/BMedScDOC2021/Abstracts/Python_Scripts/replacement.csv
#Abstracts Folder Path: /Users/manojarachige/Documents/Coding/BMedScDOC1/BMedScDOC2021/Abstracts/Empty
#Dictionary Path: /Users/manojarachige/Documents/Coding/BMedScDOC1/BMedScDOC2021/Abstracts/Python_Scripts/full_dictionary.txt

import BMedScWC as wrc
import os



#initialise empty lists:
dictionary = []
combined = [] #For pathway 2 - total dictionary list
docs = []



def main(): 
    #input replacement + abstracts
    replacement = input("Replacement Path: ")
    abstracts = input("Abstracts Folder Path: ")
    dictpath = input("Dictionary Path: ")
    
    failed = 0
    #create a list of abstract files found in folder (get_corpus) 
    doc_list = os.listdir(abstracts)
    print("\n Corpus List: ", doc_list)
    
    #create the dictionary list from the dictionary txt
    dictionary = wrc.makedict(dictpath)
    print("\n Dictionary terms: ", dictionary)

    #loop over files in contents list
    counter = 0
    for file in doc_list:
        try:
            print(counter) #To keep track
        
            text = wrc.maketxt(abstracts + "/" + file, replacement)
            text = wrc.rem_dict(dictionary, text)
            combined.extend(text) 
        
            doc_for_tdm = " ".join(text)
            docs.append(doc_for_tdm)
        except:
            failed += 1
            
        
        counter += 1
    
    print(">>>>Combined BoW:", "(", len(combined), "):\n", combined, "\n")
    #create tdm
    df = wrc.tdm_make(docs) 
    print("tdm: \n", df)
    
    #where to download
    location = input("Please enter the Path to directory where outputs should be saved. \n ie: /Users/manojarachige/Downloads/ \n Path: ")
    df.to_csv(r'{}TDM.csv'.format(location))
    
    #replace with Display words
    #for_display is the combined list, substituted for display words from csv
    for_display = wrc.display(combined, replacement)
    print("Words For Display >>>", for_display)
    
    wrc.barchart(for_display, location)
    wrc.wc(for_display, location)
    print("Failed: ", failed)
    
    
main()
    
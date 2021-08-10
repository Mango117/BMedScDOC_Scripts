#Separate a list of pdfs to remove broken copies.
#Create a new folder of only good pdfs

import os
import shutil 
from pdf_check import isFullPdf
import progressbar

#source = input("Path to folder of initial pdfs: ")
#output_location = input("Path to output folder: ")

source = "/Users/manojarachige/Documents/Coding/BMedScDOC1/BMedScDOC2021/Pubmed-Batch-Download-Multiprocessing/fetched_pdfs"
output_location = "/Users/manojarachige/Documents/Coding/BMedScDOC1/BMedScDOC2021/Pubmed-Batch-Download-Multiprocessing/separated_pdfs"

#previous version of main without progessbar
'''def main():
    separated_counter = 0
    time_counter = 1
    pdf_list = get_corpus(source)
    length = len(pdf_list)
    for i in pdf_list:
        print(time_counter, "out of ", length)
        if isFullPdf(source + "/" + i) == True:
            shutil.copy2(source + "/" + i, output_location)
            separated_counter += 1
        time_counter += 1
            
    print(separated_counter, "files separated out of ", len(pdf_list), "source files" )
    '''
    
def main():
    separated_counter = 0
    time_counter = 0
    pdf_list = get_corpus(source)
    length = len(pdf_list)
    with progressbar.ProgressBar(max_value=length, redirect_stdout=True) as p:
        for i in pdf_list:
            if isFullPdf(source + "/" + i) == True:
                shutil.copy2(source + "/" + i, output_location)
                separated_counter += 1
            p.update(time_counter)
            time_counter += 1
            
            
    print(separated_counter, "files separated out of ", len(pdf_list), "source files" )
            
        
    
def get_corpus(folder):
    basepath = folder
    lst = os.listdir(basepath)
    lst.sort()
    for file in lst:
        check = file
        path = os.path.abspath(check)
        ext = os.path.splitext(path)[-1].lower()
        if ext != ".pdf":
            lst.remove(file)
    return lst
    

    
main()
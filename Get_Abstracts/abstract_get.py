#take a list of PMIDs
#loop over all of them
#write their abstract contents into txt files
#Path to PMID list: /Users/manojarachige/Documents/Coding/BMedScDOC1/BMedScDOC2021/Abstracts/Txt_Files/PMID_numbers


#Firstly, navigate to empty folder
#run python abstract_get.py
import urllib.request

PMID_list = input("Path to PMID list: ")

counter = 1
with open(PMID_list, "r") as file:
    for line in file:
        #keep track
        print("PMID: ", line, "  ", counter)
        counter += 1
        
        try:
            url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={0}&retmode=text&rettype=abstract".format(line.strip("\n"))
            print(url)
            abst = urllib.request.urlopen(url)
        
            with open("{}.txt".format(line), "w") as output:
                for line in abst:
                    decoded_line = line.decode("utf-8")
                    output.write(decoded_line)
                output.close()
        except:
            pass

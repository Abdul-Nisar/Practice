# 3. process_json.py == Will use the output/int_data_file.csv as a reference and will go through the doc.json to and extract the description in the structured format.

 

import json
import re
import csv
# Read Table of content file

# toc_file = open("pdf-results.txt","r")
toc_file = open(r"int_data_file.csv", "ra", encoding="utf-8")
toc_records = toc_file.read().splitlines()
toc_file.close()
i = 0
j = 1

# Read Extracted pdf file as json
# with open("doc.json","r") as read_file:
with open(r"doc.json", "r", encoding="utf-8") as read_file:
    pdf_para = json.load(read_file)
k = 0

print_bool = False

while i < len(toc_records):
    current_header = toc_records[i].replace('|', ' ')
    current_header = '<h3>' + current_header

    if j > (len(toc_records) - 1):
        next_header = ""
    else:
        next_header = toc_records[j].replace('|', ' ')
        next_header = '<h3>' + next_header

    # print("Processing ----> :" + current_header)
    k = 0
    while k < (len(pdf_para) - 1):
        while print_bool == True:
            if k < len(pdf_para):
                if (pdf_para[k].strip() != '') and (pdf_para[k].strip() != '|'):
                    # print(pdf_para[k].strip())
                    pass
            k += 1
            if k < len(pdf_para):
                if (next_header == "") or (next_header.strip() in pdf_para[k].strip()):
                    print_bool = False
            else:
                print_bool = False
        #                k = k-1

        if k < len(pdf_para):
            if current_header.strip() in pdf_para[k].strip():
                print_bool = True
        k += 1
    i += 1
    j += 1




file_json = open(r"doc.json", 'r', encoding="utf-8")
data = json.loads(file_json.read())

header_maj = []
for file_data_major in data[0:50]:
    head_reg = re.compile(r'<h2>CIS')
    version_reg = re.compile(r'<p>v[0-9].')
    if file_data_major != "":
        if head_reg.search(file_data_major) or version_reg.search(file_data_major):
            header_maj.append(file_data_major.strip())

title_of_benchmark = header_maj[0].replace("<h2>", '')
version_benchmark = header_maj[1].replace("<p>", '')
split_version = version_benchmark.split(' - ')


# the list_of_headers is defined to get matching element in doc.json file
list_of_headers = ["<p>Profile Applicability: ", "<p>Description: ", "<p>Rationale: ", "<p>Audit: ", "<p>Remediation: ",
                   "<p>Impact: ", "<p>Default Value: ", "<p>References: ", "<p>CIS Controls: ",
                   "<p>Profile Applicability:", "<p>Description:", "<p>Rationale:", "<p>Audit:", "<p>Remediation:",
                   "<p>Impact:", "<p>Default Value:", "<p>References:", "<p>CIS Controls:"]

# list_header is define to get element from data matching with list headers element
list_header = ["header", "<p>Profile Applicability:", "<p>Description:", "<p>Rationale:", "<p>Impact:", "<p>Audit:",
               "<p>Remediation:",
               "<p>Default Value:", "<p>References:", "<p>CIS Controls:"]

# getting index positions of the elements of the doc.json which match with the headers in to our set
def get_list_index():
    pos = 0
    index_set = set()       # index set is defined to store the index value of list_of_headers
    while pos < len(data):
        if data[pos] in list_of_headers:
            index_set.add(pos)
        pos += 1
    return index_set

# sorting the index positions in sorted manner
sorted_index = sorted(get_list_index())
i = 0

op_f = open(r"final.csv", "w", encoding="utf-8")
op_f.write(title_of_benchmark+','+split_version[0]+','+split_version[1])     # write the output line in resulted file
op_f.write('\n')
op_f.write("Number,Category,Sub-Category,Sub-Sub-Category,Sub-Sub-Sub-Category,Type of Check,Profile Applicability,Description,Rationale,Impact,Audit,Remediation,Default Value,References,CIS Controls")
op_f.write("\n")

# this list is defined for storing data of headers list in list_header e.g. data of profile applicability will story in pot_list's 2nd position and data of header will store in 1st position
pot_list = ['', '', '', '', '', '', '', '', '', '']
num = 0


csv2 = open(r'final_data_file.csv', 'r',  encoding="utf-8")
f2 = csv.reader(csv2)

f2 = list(f2)

list_data = []

while i < len(sorted_index):
    m = i
    stri = data[sorted_index[m]]        # stri will store header like profile applicability, CIS Control, References etc 
    if stri.strip() == "<p>Profile Applicability:":     # this will check whether header is profile applicatiobility or not, if yes, them, data of previous index which is stored in pot_list will be append to list_data
        list_data.append(pot_list[0:10])
        
        pot_list = ['', '', '', '', '', '', '', '', '', '']     # redefining empty pot_list for next index
        header = data[sorted_index[m]-2]        # get index name as header and will store in 1st position of pot_list
        header = header.split(' ')
        header = ' '.join(string_this for string_this in header[1:])
        header = header.replace('(Automated)', '')
        header = header.replace('(Manual)', '')       
        header = header.strip()
        pot_list.insert(list_header.index('header'), header) 

    if stri.strip() in list_header:     # if header is present in list_header, then we will take data from current header to next header eg. from profile applicability to description
        if i+1 != len(sorted_index):    # if current iteration of i is less than length of sorted index
            string_list = data[sorted_index[m]:sorted_index[m+1]]   # e.g. from profile applicability to description
            for header in list_of_headers:
                if header in string_list:
                    string_list.remove(header)      # removing header e.g. removing profile applicability
        else:   # this is to get last index of data,
            next_num = sorted_index[m]+10
            string_list = data[sorted_index[m]:next_num]
            for header in list_of_headers:
                if header in string_list:
                    string_list.remove(header)
        # to remove next header (index information) from data we get
        regex = re.compile(r'<[a-z][0-9]>[0-9].')
        for string_li in string_list:
            if regex.search(string_li):
                string_list.remove(string_li)
        
        # joining all the string present in string_list [data from profile applicability to description]
        string = ' '.join(list_ele for list_ele in string_list)
        string = string.replace('<p>', '')
        string = string.replace('<h4>', '')
        string = string.replace('<h5>', '')
        string = string.replace('<s1>', '')
        string = string.replace('<s2>', '')
        string = string.replace('<s3>', '')
        string = string.replace('<s4>', '')
        string = string.replace('<s5>', '')
        string = string.replace('|', '')
        string = string.replace(',', ' ')
        # data we get between two headers will be stored on position of current header e.g.
        # data of profile applicability which is present in string after concatination 
        # which is from profile applicability to description at position 2 which is from list_header
        pot_list.insert(list_header.index(stri.strip()), string)
        num += 1
        i += 1
        

list_data.append(pot_list[0:10])    # to add last line of last index
pointer_this = 1


for index_nm in f2[1:]:     # reading every data of index file present in out.csv
    string_index = ' '.join(s for s in index_nm)    # joining all the content of list getting of line
    string_sample = string_index.replace('|', ',')   # replacing | with , as it is define as comma separated
    this_string = string_sample     # storing the current line of index file
    
    for every_list_index in range(pointer_this, len(list_data), 1):     # reading lines by lines from list_data for fetching index data
        list_string = list_data[every_list_index]       # storing list of every index in list string
        string_data = ','.join(every_data for every_data in list_string[1:])        # joining all list element of index data except header
        if list_string[0] in string_sample:     # cheking whether header(index detail) of pot_list is present in index detail of index file
            this_string = this_string + ',' + string_data   # if present , add to this_string with index file line
            pointer_this += 1    # increase the pointer to start from next list_data element
    op_f.write(this_string)     # write the output line in resulted file
    op_f.write('\n')

op_f.close()                    




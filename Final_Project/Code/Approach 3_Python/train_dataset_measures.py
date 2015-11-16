__author__ = 'Aniket Ghodke'

''' All the import statements '''
import time
import math
import pandas as pd

import statsmodels.api as sm
import numpy as np

start_time = time.time()

# ----------------------------Data Definitions Begin-------------------------------------#

'''
Input file is AP_train's processed file named Train_Data_Matrix.txt
This file is ; separated file. More to be added here.
'''
train_data_matrix_handler = open("Train_Data_Matrix.txt", "r")

'''
Input file handler for Test data file.
'''
test_data_matrix_handler = open("Test_Data_Matrix.txt", "r")

'''
Reading the hindex file
'''
hindex_file = open("H_index_Non_Zero.txt","r")
'''
'''
''' '''
test_papers_handler = open("Test_Ids.txt", "r")
data_entry_handler = open("training_data_set.csv", "w")


paper_to_bucketid_handler = open("paperid_bucketid.txt", "r")
#paper_bucket = open("paper_bucket.txt","r")
pap_level_3_handler = open("pap_compres_level3.txt","r")
bucketid_to_bucket_handler = open("filtered_term_buckets.txt", "r")
citation_map_handler = open("Citations.txt", "r")
paper_buckets = open("paper_bucket.txt","r")
''' Reading files to read and  writing the files '''


''' Creating the maps '''
bucketid_to_bucket = {}
paper_to_bucketid = {}
data_matrix_map = {}
unique_bucket = {}
missing_bucket = {}
paper_bucket_map = {}
citation_count = {}
author_paper_map = {}
paper_author_map = {}
hindex_map = {}
data_entry = {}
citation_map = {}
pap_all_auth_level1_map = {}
pap_all_auth_level3_map = {}
paper_buckets_map = {}

''' Global variables '''
theta_vector = []
total_cs = 0.0
total_count = 0
cs_threshold = 0.0

''' Creating the maps from the files read '''
print("Creating the paper bucket map")
for line in paper_buckets:
    content = line.split(";")
    paper_id = int(content[0])
    bucket_ids = content[1].split(",")
    bucket_ids= map(int,bucket_ids)
    paper_buckets_map[paper_id] = bucket_ids
print("Creating the paper_buckets map done. ")


print "creating the pap_level_3_map patience check !! It will slow the system down"
for line in pap_level_3_handler:
    line = line.strip()
    content = line.split("\t")
    if len(content) > 1:
        paper = int(content[0])
        authors = content[1]
        #print(paper)
        authors = authors.split(",")
        all_auth = list()
        for p in authors:
            all_auth.append(p)
        pap_all_auth_level3_map[paper] = all_auth
print("Paper level 3 map created" + str(len(pap_all_auth_level3_map)))

print("creating citations map")
for line in citation_map_handler:
    line = line.strip()
    line = line.split(';')
    paper_being_cited = int(line[0])
    papers_that_cites_list = line[1]
    if papers_that_cites_list != 'null':
        papers_that_cites_list = papers_that_cites_list.split(',')
        papers_that_cites_list = map(int, papers_that_cites_list)
        citation_map[paper_being_cited] = papers_that_cites_list
        citation_count[paper_being_cited] = len(papers_that_cites_list)

print "Length of citations_map is: " +str(len(citation_map))

print("creating hindex map")
for line in hindex_file:
    content = line.split(";")
    key = content[0]
    value = content[1]
    hindex_map[key] = int(value)
print("Length of hindex " + str(len(hindex_map)))
#Positive label count
pcount = 0

# ----------------------------Data Definitions End-------------------------------------#

''' Creating the data matrix '''
def create_data_matrix_map(file):
    global author_paper_map
    global paper_author_map

    for line in file:
        # Strip the newline character
        line = line.strip()
        # Split the attributes into two fields
        current_paper = line.split(';')

        #  Do the processing for indexes of paper
        # Sanity check if index is not null
        if current_paper[0] != '':
            # Define paper index number
            paper_index = int(current_paper[0])

        paper_authors = set()

        if current_paper[2] != '':
            authors = current_paper[2].strip()
            '''Aniket's changes start'''
            #paper_author_map[str(paper_index)] = authors
            paper_author_map[paper_index] = authors
            authors_array = authors.split(",")
            for a in authors_array:
                if a in author_paper_map:
                    #author_paper_map[a] = author_paper_map[a] + "," + str(paper_index)
                    author_paper_map[a].append(paper_index)
                else:
                    #author_paper_map[a] = str(paper_index)
                    author_paper_map[a] = [paper_index]
            '''Aniket's changes end'''
            authors = set(authors.split(','))
            paper_authors.union(authors)

        paper_ref = set()
        if current_paper[5] != '':
            references = current_paper[5]
            references = references.split(',')
            references = set(map(int, references))
            paper_ref.union(references)
        paper_abstract = ''
        if current_paper[6] != '':
            paper_abstract = current_paper[6]

        paper_data = (paper_authors, paper_ref, paper_abstract)
        data_matrix_map[paper_index] = paper_data

print("Creating data matrix AP_Train")
create_data_matrix_map(train_data_matrix_handler)
print 'Completed Reading AP_Train.txt'
create_data_matrix_map(test_data_matrix_handler)
print("reading test data")

# Generates the papers missing from the buckets.
for line in paper_to_bucketid_handler:
    line = line.strip()
    data = line.split()
    #print(data[0])
    paper = int(data[0])
    if len(data) > 1:
        bucket = int(data[1])
        paper_to_bucketid[paper] = bucket
        unique_bucket[bucket] = 1
    else:
        missing_bucket[paper] = 1

print 'Completed Reading paper_to_bucketid ' + str(len(paper_to_bucketid))
print 'Unique buckets : ' + str(len(unique_bucket))

count = 0
for line in bucketid_to_bucket_handler:
    count +=1
    counter =0
    print count
    line = line.strip()
    data = line.split('\t')
    bucketid = int(data[0])
    if bucketid in unique_bucket:
        papers = data[1].split()
        papers = map(int, papers)
        bucketid_to_bucket[bucketid] = papers
print 'Completed Reading bucketid_to_bucket ' + str(len(bucketid_to_bucket))

''' Functions defination starts here '''
#PAP Measures takes p1 and p2 and gives the count and path sim measures for the 2 papers.
#Number of common authors is count and path sim in HM of common authors.
def PAP_measures(p1, p2):

    auth1_list =  data_matrix_map[p1][0]
    auth2_list =  data_matrix_map[p2][0]

    ''' Count '''
    common_authors = auth1_list.intersection(auth2_list)
    common_auth = len(common_authors)

    ''' PathSim '''
    auth1_list_length = len(auth1_list)
    auth2_list_length = len(auth2_list)

    if auth1_list_length != 0 and auth2_list_length != 0:
        pathSim = (2 * common_auth) / (auth1_list_length + auth2_list_length)
    else:
        pathSim = 0.0

    measures = (common_auth, pathSim)
    return measures

#PCP Measures: takes 2 papers p1 and p2 and generates the PCP measures for the papers.
# in form of tuple of (count,path sim)
def PCP_measures(p1, p2):

    p1_ref = data_matrix_map[p1][1]
    p2_ref = data_matrix_map[p2][1]

    ''' Count '''
    common_ref = p1_ref.intersection(p2_ref)
    common_ref_len = len(common_ref)

    p1_ref_length = len(p1_ref)
    p2_ref_length = len(p2_ref)

    ''' PathSim '''
    if p1_ref_length != 0 and p2_ref_length != 0:
        pathSim = (2 * common_ref_len / (p1_ref_length + p2_ref_length))
    else:
        pathSim = 0

    measures = (common_ref_len, pathSim)
    return measures


#PTP Measures: takes 2 papers p1 and p2 and generates the PTP measures for the papers.
# in form of tuple of (count,path sim)
def PTP_measures(p1, p2):
    p1_terms_map = {}
    p2_terms_map = {}
    count =0
    pathSim =0.0
    if p1 in data_matrix_map and p2 in data_matrix_map:
        p1_terms = data_matrix_map[p1][2].split(' ')
        p2_terms = data_matrix_map[p2][2].split(' ')

        for t in p1_terms:
            if t not in p1_terms_map:
                p1_terms_map[t] = 1
            else:
                p1_terms_map[t] += 1

        for t in p2_terms:
            if t not in p2_terms_map:
                p2_terms_map[t] = 1
            else:
                p2_terms_map[t] += 1
        ''' Count '''
        p1_set = set(p1_terms_map.keys())
        p2_set = set(p2_terms_map.keys())
        common_terms = p2_set.intersection(p1_set)
        count = len(common_terms)

        ''' PathSim '''
        ''' Numerator '''
        if count != 0:
            num = 0.0
            for term in common_terms:
                num += p1_terms_map[term] * p2_terms_map[term]
            num *= 2

            ''' Denomenarator 1 '''
            denom1 = 0.0
            for term in p1_terms_map:
              denom1 += p1_terms_map[term] * p1_terms_map[term]

            ''' Denomenarator 1 '''
            denom2 = 0.0
            for term in p2_terms_map:
                denom2 += p2_terms_map[term] * p2_terms_map[term]

            pathSim = num / (denom1 + denom2)
        if count ==0:
            pathSim = 0.0

    measures = (count, pathSim)
    return measures




''' Aniket's changes start '''

#PAP2 Measures: takes 2 papers p1 and p2 and generates the PAP2 measures for the papers.
# in form of tuple of (count,path sim)
def pap2(authors_level1_p1,authors_level3_p1,papers_level4_p1,p2):
    #print("pap2 measure called")
    #p2 = str(p2)
    if p2 in pap_all_auth_level3_map and p2 in paper_author_map:
        count = papers_level4_p1.count(p2)
        authors_level1_p2 = paper_author_map[p2]
        authors_level1_p2 = authors_level1_p2.split(",")
        authors_level3_p2 = pap_all_auth_level3_map[p2]
        total = authors_level3_p2
        authors_level3_p2 = list()
        for t in total:
            complete = t.split(";")
            authors_level3_p2.append(complete[0])

        allauthors_p1 = authors_level1_p1 + authors_level3_p1
        allauthors_p2 = authors_level1_p2 + authors_level3_p2
        all_authors = {}
        for a1 in allauthors_p1:
            if a1 in all_authors:
                val = all_authors[a1][0]
                all_authors[a1] = (val+1,0)
            else:
                all_authors[a1] = (1,0)

        for a2 in allauthors_p2:
            if a2 in all_authors:
                val1 = all_authors[a2][0]
                val2 = all_authors[a2][1]
                all_authors[a2] = (val1,val2+1)
            else:
                all_authors[a2] = (0,1)
        numerator = 0
        denom1= 0
        denom2 =0
        for a in all_authors:
            val1 = all_authors[a][0]
            val2 = all_authors[a][1]
            numerator += (val1 * val2)
            denom1 += (val1 * val1)
            denom2 += (val2 * val2)
        if denom1 != 0 and denom2 !=0:
            numerator = numerator * 2
            pathsim = numerator / (float)(denom1 + denom2)
        else:
            pathsim = 0
    else:
        pathsim = 0
        count = 0
    measures = (count,pathsim)
    #if measures[0] != 0 and measures[1] !=0:
    #    print "pap2" + str(measures)
    return measures


#PCP2 Measures: takes 2 papers p1 and p2 and generates the PCP2 measures for the papers.
# in form of tuple of (count,path sim)
def pcp2(p1,p2):
    #print("pcp2 measure called")
    all_citations_level2_p1 = list()
    cit_p1 = {}
    cit_p2 = {}
    count =0
    ps = 0.0
    if p1 in citation_map:
        cits = citation_map[p1]
        for c in cits:
            if c in citation_map:
                cits_level2 = citation_map[c]
                for c2 in cits_level2:
                    all_citations_level2_p1.append(c2)
                    if c2 in cit_p1:
                        cit_p1[p1] += 1
                    else:
                        cit_p1[p1] = 1
        count = all_citations_level2_p1.count(p2)
        #if(count != 0):
        #    print "pcp2" + str(count)
        if count != 0:
            all_citations_level2_p2 = list()
            if p2 in citation_map:
                cits = citation_map[p2]
                for c in cits:
                    if c in citation_map:
                        cits_level2 = citation_map[c]
                        for c2 in cits_level2:
                            all_citations_level2_p2.append(c2)
                            if c2 in cit_p2:
                                cit_p2[p2] += 1
                            else:
                                cit_p2[p2] = 1

            p1_keys = cit_p1.keys()
            p2_keys = cit_p2.keys()
            p1_keys = set(p1_keys)
            p2_keys = set(p2_keys)
            intersect = p1_keys.intersection(p2_keys)
            numerator = 0
            denom1= 0
            denom2 =0
            for i in intersect:
                numerator += (cit_p1[i] * cit_p2[i])
                denom1 += (cit_p1[i] * cit_p1[i])
                denom2 += (cit_p2[i] * cit_p2[i])
            numerator = numerator * 2
            if denom1 != 0 and denom2 !=0:
                ps = numerator / (float)(denom1 + denom2)

        if count == 0:
            ps = 0.0
    measures = (count,ps)
    return measures

#Hindex Measures: takes paper p2 and generates the Hindex measures for the papers.
# If there are more authors then we get the maximum of all the authors Hindex.
def hindex(p2):
    #p2 = str(p2)
    #print("hindex measure called")
    if p2 in paper_author_map:
        authors = paper_author_map[p2]
        authors_array = authors.split(",")
        max = 0
        for a  in authors_array:
            if a != "" and a in hindex_map:
                if hindex_map[a] > max:
                    max = hindex_map[a]
    else:
        max = 0
    return(max)

#Citations: Takes a paper and generates citation count of paper,
# if there are no citations then it gives the score as 0
def citations(p2):
    #print("citations measure # ")
    if p2 in citation_count:
        counter = citation_count[p2]
    else:
        counter = 0
    return counter

''' Aniket's changes ends '''
# find_label : Takes a paper p2 and generates a label to be given to logistic regression

def find_label(p2):
    global pcount
    if p2 in citation_map:
        if len(citation_map[p2]) > 1:
            label = 1
            pcount += 1
        else:
            label = 0
    else:
        label = 0

    return label


def create_logit_model():
   # read the data in
   #print("Logit model called")
   df = pd.read_csv("training_data_set.csv")

   df.columns = ["f1", "f2", "f3","f4", "f5", "f6","f7","f8", "label"]

   # create a clean data frame for the regression
   cols_to_keep = ["f1", "f2", "f3","f4", "f5", "f6","f7","f8", "label"]
   data = df[cols_to_keep]

   # manually add the intercept
   data['intercept'] = 1.0
   #print(data)
   train_cols = data.columns[:2]
   #print("Printing data[label]")
   #print(data['label'])
   #print("Printing data[tran_cols]")
   #print(data[train_cols])
   if len(data['label']) > 2:
       if len(data[train_cols]) > 2:
        logit = sm.Logit(data['label'], data[train_cols])
        # fit the model
        result = logit.fit()
        # cool enough to deserve it's own gist
        params = (result.params)
        #print("Printing type of result.params")
        #print(type(result.params))
        return params
   else:
       return "Fail"

def assign_attributes(p1, bucket):
    global data_entry
    p2_papers = bucketid_to_bucket[bucket]

    p1 = int(p1)
    if p1 in paper_author_map and p1 in pap_all_auth_level3_map:
        authors_level1_p1 = paper_author_map[p1] # Need set here
        authors_level1_p1 = authors_level1_p1.split(",")

        authors_level3_p1 = pap_all_auth_level3_map[p1]# Need set here
        total = authors_level3_p1
        authors_level3_p1 = list()
        for t in total:
            complete = t.split(";")
            authors_level3_p1.append(complete[0])
        papers_level4_p1 = list()
        for a in authors_level3_p1:
            all_papers = author_paper_map[a]
            for al in all_papers:
                papers_level4_p1.append(al)# need set here

        for p2 in p2_papers:
            if p1 != p2:
                #pap = PAP_measures(p1, p2)
                #pcp = PCP_measures(p1, p2)
                #print("calling ptp")
                ptp = PTP_measures(p1, p2)
                #print("calling pap2")
                papsq = pap2(authors_level1_p1,authors_level3_p1,papers_level4_p1,p2)
                #print("calling pap3")
                #papcu = pap3(count,authors_level1_p1,authors_level3_p1,authors_level5_p1,paper_level6_p1,p2)
                pcpsq = pcp2(p1,p2)
                #print("calling hindex")
                hin = hindex(p2)
                #print("calling citations")
                cit = citations(p2)

                f_vector = (ptp[0], ptp[1], papsq[0],papsq[1],pcpsq[0],pcpsq[1],hin,cit)
                #label = find_label(p2, f_vector, count)
                label = find_label(p2)

                entry = (ptp[0], ptp[1] , papsq[0],papsq[1],pcpsq[0],pcpsq[1],hin,cit, label)

                data_entry[p2] = f_vector
                data = ','.join(map(str, entry)) + '\n'
                data_entry_handler.write(data)

def create_final_dataset():
    global data_entry_handler, data_entry, start_time, theta_vector, total_cs, total_count, cs_threshold
    count = 0
    top_10 = {}
    top10_citations_handler = open("top10_citations_Program_changed.txt", "w")
    top10_citations_handler.write("Id,References" + '\n')

    #for p1 in paper_to_bucketid:
    total_cs = 0.0
    total_count = 0
    cs_threshold = 0.0
    for p1 in test_papers_handler:
        p1 = int(p1)
        #end_time = time.time()
        #print("Elapsed time after each iteration is %g seconds" (end_time - start_time))
        #start_time = time.time()

        #if count > 100:
        #    break
        count += 1
        #dataset =
        data_entry.clear()
        top_10.clear()
        cur_min = 0.0
        min_ind = -1
        if data_entry_handler != 0:
            data_entry_handler = open("training_data_set.csv", "w")

        data_entry_handler.write("f1,f2,f3,f4,f5,f6,f7,f8,label\n")
        if p1 in paper_to_bucketid:
            bucket = paper_to_bucketid[p1]
            #print(bucket)
            print("calling assign attribute" + str(p1))
            assign_attributes(p1, bucket)
            data_entry_handler.close()
            theta = create_logit_model()
            if isinstance(theta, pd.core.series.Series):
                theta_vector = []
                for t in theta:
                    theta_vector.append(t)

                for p2 in data_entry:
                    f_vector = data_entry[p2]
                    f_theta = sum([a*b for a,b in zip(f_vector,theta_vector)])
                    ''' To avoid overflow'''
                    if f_theta > 600.0:
                        f_theta = 600.0
                    #print(f_theta)
                    e_z = math.exp(f_theta)
                    citation_prob = e_z / (e_z + 1)
                    # This is the CBN logic
                    # Takes 2 papers and get the number of common buckets the paper is in.
                    if p1 in paper_buckets_map and p2 in paper_buckets_map:
                        paper1_bucket_set = set()
                        paper2_bucket_set = set()
                        buckets_paper1 = paper_buckets_map[p1]
                        for b in buckets_paper1:
                            paper1_bucket_set.add(b)
                        buckets_paper2 = paper_buckets_map[p2]
                        for b in buckets_paper2:
                            paper2_bucket_set.add(b)
                        common_buckets = paper1_bucket_set.intersection(paper2_bucket_set)
                        cbn = len(common_buckets)
                    else:
                        cbn = 0
                    cs = math.log10(1 + cbn) * citation_prob
                    # Commenting the above code since for all CBN = 0 the citation score will be 0
                    #cs = citation_prob
                    #print 'Paper : ' + str(p2) + ' : ' + str(cs)

                    total_cs += cs
                    total_count += 1
                    top_10[p2] = cs
                    #print("Citations score p2: " +str(p2) + ";" + str(cs))
                top10_citations = sorted(top_10.iteritems(), key=lambda key_value: key_value[1], reverse=True)
                top10_citations = top10_citations[:10]

                cs_threshold = total_cs / total_count

                print 'Citations for Paper : ' + str(p1)
                citations = str(p1) + ','
                for i in top10_citations:
                    print i
                    cited_paper = i[0]
                    citations += str(cited_paper) + ' '
                citations = citations.strip()
                citations += '\n'
                top10_citations_handler.write(citations)
    for miss in missing_bucket:
        data = str(miss) + ",\n"
        top10_citations_handler.write(data)
    top10_citations_handler.close()

create_final_dataset()
end_time = time.time()
print("Elapsed time was %g seconds" % (end_time - start_time))

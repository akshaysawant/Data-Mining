__author__ = 'Aniket'
# PAP2 this program takes the train data set and the test data set and
# generates a map with the paper number and the author which are in level 3 with respect to given paper
# i.e. it takes a paper and from filtered term buckets map, then gets authors then from those authors
# get their written papers and then from those papers get the authors again. this is PAP^2 measure.

pap_all_auth_level1_map = {}
pap_all_auth_level3_map = {}
pap_all_auth_level5_map = {}
author_paper_map = {}
paper_author_map = {}

train_data_matrix_handler = open("Train_Data_Matrix.txt", "r")
test_data_matrix_handler = open("Test_Data_Matrix.txt", "r")
pap_all_auth_level1_file = open("pap_all_auth_level1_map.txt", "w")
pap_all_auth_level3_file = open("pap_all_auth_level3_map.txt", "w")
bucketid_paper = open("filtered_term_buckets.txt","r")


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


create_data_matrix_map(train_data_matrix_handler)
create_data_matrix_map(test_data_matrix_handler)

print("maps created")
count = 0

for line in bucketid_paper:
    count +=1
    counter =0
    print count
    line = line.strip()
    data = line.split('\t')
    papers = data[1].split(" ")
    papers = map(int, papers)
    for p2 in papers:
        string = ""
        if p2 not in pap_all_auth_level1_map:
            counter += 1
            print(str(count) + ";" + str(counter))
            if p2 in paper_author_map:
                authors_level1_p2 = paper_author_map[p2]
                authors_level1_p2 = authors_level1_p2.split(",")
                if counter == 1082:
                    print("Authors level 1")
                    print authors_level1_p2
                papers_level2_p2 = list()
                for a in authors_level1_p2:
                    papers = author_paper_map[a]
                    for p in papers:
                        if p != p2:
                            papers_level2_p2.append(p)
                authors_level3_p2 = list()
                for p in papers_level2_p2:
                    if p in paper_author_map:
                        authors = paper_author_map[p]
                        authors = authors.split(",")
                        for a in authors:
                            if a not in authors_level1_p2:
                                authors_level3_p2.append(a)
                if counter == 1082:
                    print("Authors level 3")
                for a in authors_level1_p2:
                    string += a +","
                string = string[:-1]
                pap_all_auth_level1_file.write(str(p2)+"\t"+str(string) +"\n")
                string = ""
                pap_all_auth_level1_map[p2] = 1

                for a in authors_level3_p2:
                    string += a +","
                string = string[:-1]
                pap_all_auth_level3_file.write(str(p2)+"\t"+str(string) +"\n")
                pap_all_auth_level3_map[p2] = 1

pap_all_auth_level1_file.close()
pap_all_auth_level3_file.close()

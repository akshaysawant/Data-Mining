__author__ = 'Aniket'

# This program takes the paper author level 3 map. i.e. given a paper get its
# authors then for those authors get papers and then again for all those papers
# get author. This will be PAP^2 measure.
# This program will compress the author names in the map.
# e.g. if the author is xyz and it comes 2 time in the level 3 map then the
# map will be compressed to XYZ-2 hence the size of the map is reduced from
# 6GB to 3GB which is nearly half the size.

# This program will write the compress map to pap_compres_level3.txt file in the same
# folder.

file = open("pap_all_auth_level3_map.txt","r")
outfile = open("pap_compres_level3.txt","w")
count = 0
for line in file:
    line = line.strip()
    content = line.split("\t")
    paper = int(content[0])
    if len(content) > 1:
        authors = content[1]
        authors = authors.split(",")
        comp_map = {}
        for a in authors:
            if a in comp_map:
                comp_map[a] += 1
            else:
                comp_map[a] = 1
        string = ""
        for k in comp_map:
            string += str(k) + ";" + str(comp_map[k]) + ","
        string = string[:-1]

        outfile.write(str(paper) + "\t" + str(string) +"\n")
        count += 1
        print(count)
outfile.close()
__author__ = 'Aniket'
# this program takes bucketid_bucketpapers.txt and then from that
# checks given paper is in which all buckets. i.e. it creates inverse bucket map.
# and stores the output in paper_bucket.txt file in the same folder.

paper_bucket = open("filtered_term_buckets.txt","r")
output = open("paper_bucket.txt","w")

paper_bucket_map = {}
for line in paper_bucket:
    line = line.strip()
    content = line.split("\t")
    bucket_id = int(content[0])
    papers = content[1]
    papers = papers.split(" ")
    for p in papers:
        if p in paper_bucket_map:
            paper_bucket_map[p].append(bucket_id)
        else:
            paper_bucket_map[p] = [bucket_id]
print("map created" + str(len(paper_bucket_map)))
for k in paper_bucket_map:
    paper = str(k)
    bucket_list = paper_bucket_map[k]
    string = ""
    for b in bucket_list:
        string += str(b) +","
    string = string[:-1]
    output.write(paper + ";" + string +"\n")

output.close()



__author__ = 'Aniket'
## This takes in the file "Test_Data_Matrix" and generates all the test id's in the file
## and generates the test id in a file
input = open("Test_Data_Matrix.txt","r")
output = open("Test_Ids.txt","w")

for line in input:
    content = line.split(";")
    index = content[0]
    output.write(index +"\n")

output.close()
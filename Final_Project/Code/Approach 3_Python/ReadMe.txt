All the code needs to run on python 2.7 with following libraries installed on the machine: 
math
time
pandas
statsmodels
numpy

To run the second approach please perform the following steps: 
1. Copy Citations.txt, H_index_Non_Zero.txt, paperid_bucketid.txt, Test_Data_Matrix.txt, Train_Data_Matrix.txt and filtered_term_buckets.txt from Misc folder to the folder containing programs. 
2. Run the code PAP2.py this will generate pap_all_auth_level3_map.txt
3. Now run MapCompress.py this will generate pap_compres_level3.txt
4. Now run CBN.py this will generate paper_bucket.txt
5. Now run Test_ID_Generation.py this will generate Test_Ids.txt
6. Now run train_dataset_measures.py this will generate top10_citations_Program_changed.txt which will contain all the citations

NOTE: Running program in step 6 might take a lot of time depending on machines configuration. 

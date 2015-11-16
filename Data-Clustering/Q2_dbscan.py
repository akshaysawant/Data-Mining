#!/usr/bin/python

import os
import sys
import collections
import pylab
import math

file_name = sys.argv[1]
eps = float(sys.argv[2])
minpts = int(sys.argv[3])

path = 'dataset'

matrix = collections.OrderedDict()
cluster = {}
distances = {}
N = {}


def find_dist(obj1, obj2):
   if obj2 in distances.keys() and obj1 in distances[obj2].keys():
      return distances[obj2][obj1]
   else:
      distance = 0
      for i in range(len(obj1)):
         distance += (obj1[i] - obj2[i])**2
      return math.sqrt(distance)


def build_distances():
   #global distances
   for obj1 in matrix:
      if obj1 not in distances.keys():
         distances[obj1] = {}
      for obj2 in matrix:
         distances[obj1][obj2] = find_dist(obj1, obj2)


def build_neighborhood():
   #global N
   for obj1 in matrix:
      N[obj1] = []
      for obj2 in matrix:
	 if distances[obj1][obj2] <= eps:
	    N[obj1].append(obj2)



'''def get_neighborhood(obj, N):
   obj1_cord = [obj[0], obj[1]]
   for j in range(len(matrix)):
      obj2_cord = [matrix[j][0], matrix[j][1]]'''




for file in os.listdir(path):
   filename = os.path.join(path, file)

   x = []
   x1 = []
   y1 = []
   i = 1
   cluster_no = 0
   f_name = filename.split('/')[1]

   if f_name == file_name:
      with open(filename) as lines:

         ### Read file data into matrix
         for line in lines:
            data = line.split('\t')
            key = (float(data[0]), float(data[1]))
            value = [0, False]

            matrix[key] = value

      #print len(matrix)
      build_distances()
      build_neighborhood()
      for key in matrix:
         if matrix[key][1] == False:
	    matrix[key][1] = True
	    #obj = [matrix[j][0], matrix[j][1]]
	    N_obj = N[key]
	    if len(N_obj) >= minpts:
	       list = [key]
	       cluster_no += 1
	       print cluster_no
	       cluster[cluster_no] = list
	       matrix[key][0] = cluster_no

	       for p in N_obj:
	          if matrix[p][1] == False:
		     matrix[p][1] = True
		     NP_obj = N[p]
		     if len(NP_obj) >= minpts:
		        N_obj.extend(NP_obj)
		     if matrix[p][0] == 0:
		        matrix[p][0] = cluster_no
			list.append(p)
	       cluster[cluster_no] = list


      f_output = open('db_algo_' + f_name, "w")

      cno = 1
      prev_cno = 1
      for key, value in matrix.items():
	 if value[0] != 0:
            cno = value[0]
            if cno != prev_cno:
	       f_output.write('\n')
            f_output.write(str(key[0]) + '\t' +  str(key[1]) + '\t' + str(value[0]) + '\n')
	    prev_cno = cno






#!/usr/bin/python

import os
import sys
import collections
import math
from matplotlib import *
import pylab

file_name = sys.argv[1]

k = 3
path = 'dataset'

matrix = collections.OrderedDict()
cluster = {}

def update_centers():
   global cluster
   c1x1 = 0.0
   c1x2 = 0.0
   c2x1 = 0.0
   c2x2 = 0.0
   c3x1 = 0.0
   c3x2 = 0.0
   no1 = 0
   no2 = 0
   no3 = 0
   status = False
   prev_centers = {}
   for i in range(1,3):
      prev_centers[i] = cluster[i]

   for key, obj in matrix.items():
      if obj[2] == 1:
         c1x1 += obj[0]
	 c1x2 += obj[1]
	 no1 += 1

      if obj[2] == 2:
         c2x1 += obj[0]
	 c2x2 += obj[1]
	 no2 += 1

      if obj[2] == 3:
         c3x1 += obj[0]
	 c3x2 += obj[1]
	 no3 += 1

   cluster[1] = [(c1x1/no1), (c1x2/no1)]
   cluster[2] = [(c2x1/no2), (c2x2/no2)]
   cluster[3] = [(c3x1/no3), (c3x2/no3)]

   for i in range(1,3):
      if cluster[i] == prev_centers[i]:
         status = status or False
      else:
         status = status or True

   return status


def distance(x1, y1, x2, y2):
   return math.sqrt((x1-x2)**2 + (y1-y2)**2)


def update_data(obj):
   distances = {}
   dist = []
   j = 1
   while (j <= k):
      d = distance(obj[0], obj[1], cluster[j][0], cluster[j][1])
      distances[d] = j
      dist.append(d)
      j += 1
   min_d = min(dist)
   if obj[2] != distances[min_d]:
      obj[2] = distances[min_d]


def update_clusters():
   status = False
   for key, obj in matrix.items():
      new_sts = update_data(obj)
   #   status = status or new_sts
   #return status




for file in os.listdir(path):
   filename = os.path.join(path, file)

   x = []
   x1 = []
   y1 = []
   i = 1
   j = 0
   f_name = filename.split('/')[1]

   if f_name == file_name:
   #if f_name != "readme.txt":
      with open(filename) as lines:

         ### Read file data into matrix
         for line in lines:
            data = line.split('\t')
	    x = []
	    x = [float(data[0]), float(data[1]), i]
   	    '''x.append(float(data[0])) 
	    x.append(float(data[1])) 
	    x.append(i)'''
	    i += 1
      	    if i > k:
	       i = 1
	    matrix[j] = x
	    j += 1

	 ### Initialize the Cluster matrix
	 j = 1
	 c = [0.0, 0.0]
	 while (j <= k):
	    cluster[j] = c
	    j += 1

	 not_converged = True

	 while (not_converged):
	    not_converged = update_centers()
	    update_clusters()

	 c1x = []
	 c1y = []
	 c2x = []
	 c2y = []
	 c3x = []
	 c3y = []

         cno = 1
         prev_cno = 1

	 f_output = open('knn_algo_' + f_name, "w")
	 for key, value in matrix.items():
	    f_output.write(str(value[0]) + '\t' + str(value[1]) + '\t' + str(value[2]) + '\n')
            if value[2] == 1:
               c1x.append(value[0])
               c1y.append(value[1])

            if value[2] == 2:
               c2x.append(value[0])
               c2y.append(value[1])

            if value[2] == 3:
               c3x.append(value[0])
               c3y.append(value[1])

	 '''img_name = f_name.split('.')[0] + '_knn.png'
	 pylab.plot(c1x, c1y, color='r')
	 pylab.plot(c2x, c2y, color='g')
	 pylab.plot(c3x, c3y, color='b')

	 pylab.xlabel('x1')
	 pylab.ylabel('x2')

         pylab.savefig(img_name, bbox_inches='tight')'''

	 f_output.close()
	 

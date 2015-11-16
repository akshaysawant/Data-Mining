#!/usr/bin/python

import os
import sys
import collections
import math
from matplotlib import *
import pylab
import operator


file_name = sys.argv[1]
k = int(sys.argv[2])

path = 'dataset'


matrix = collections.OrderedDict()
cluster = {}
stddev = {}
split_mtx = {}
mem_matrix = {}


def split_matrix():
   global split_mtx
   split_mtx = {}
   for key, value in matrix.items():
      if value not in split_mtx.keys():
         split_mtx[value] = []
      split_mtx[value].append(key)


def intialize_clusters():
   for i in range(1, k+1):
      cluster[i] = (0.0, 0.0)


def update_centers():
   global cluster
   status = False
   prev_centers = {}

   for i in range(1,k+1):
      prev_centers[i] = cluster[i]

   for i in range(1,k+1):
      sum_x1 = 0.0
      sum_x2 = 0.0
      n = 0
      for item in split_mtx[i]:
         sum_x1 += item[0]
	 sum_x2 += item[1]
	 n += 1
      mean = (sum_x1/n, sum_x2/n)
      cluster[i] = mean

   for i in range(1,k+1):
      if cluster[i] == prev_centers[i]:
         status = status or False
      else:
         status = status or True

   return status


def find_sdeviation():
   global stddev
   for i in range(1, k+1):
      sum_x1 = 0.0
      sum_x2 = 0.0
      n = 0
      for item in split_mtx[i]:
         sum_x1 += (item[0] - cluster[i][0])**2
         sum_x2 += (item[1] - cluster[i][1])**2
         n += 1
      dev1 = math.sqrt(sum_x1 / n)
      dev2 = math.sqrt(sum_x2 / n)
      stddev[i] = (dev1, dev2)


def get_probability(obj, mean, sdev):
   divident = 2 * math.pi * sdev[0] * sdev[1]
   expo1 = (obj[0] - mean[0])**2 / (2 * sdev[0]**2)
   expo2 = (obj[1] - mean[1])**2 / (2 * sdev[1]**2)
   expo = expo1 + expo2
   return ((1 / divident) * math.exp(expo * -1))


def update_cluster(obj):
   p = {}
   for i in range(1, k+1):
      p[i] = get_probability(obj, cluster[i], stddev[i])
   max_i = max(p.iteritems(), key=operator.itemgetter(1))[0]
   matrix[obj] = max_i


def distance(obj1, obj2):
      distance = 0
      for i in range(len(obj1)):
         distance += (obj1[i] - obj2[i])**2
      return math.sqrt(distance)


def get_membership_matrix(key):
   if k == 2:
      d1 = distance(key, cluster[1])
      d2 = distance(key, cluster[2])
      val1 = d2 / (d1 + d2)
      val2 = d1 / (d1 + d2)
      return [val1, val2]

   elif k == 3:
      d1 = distance(key, cluster[1])
      d2 = distance(key, cluster[2])
      d3 = distance(key, cluster[3])

      val1 = (d2 * d3) / ((d2 * d3) + (d1 * d3) + (d1 * d2))
      val2 = (d1 * d3) / ((d2 * d3) + (d1 * d3) + (d1 * d2))
      val3 = (d1 * d2) / ((d2 * d3) + (d1 * d3) + (d1 * d2))

      return [val1, val2, val3]


def update_membership():
   global mem_matrix
   mem_matrix = {}
   for key in matrix:
      mem_matrix[key] = get_membership_matrix(key)


def update_ctr(i):
   num_x1 = 0.0
   num_x2 = 0.0
   denom = 0.0
   for key in matrix:
      denom += mem_matrix[key][i-1]**2
      num_x1 += (key[0] * (mem_matrix[key][i-1]**2))
      num_x2 += (key[1] * (mem_matrix[key][i-1]**2))
   center = ((num_x1 / denom), (num_x1/ denom))
   return center


def maximize_centers():
   global cluster
   status = False
   prev_centers = {}

   for i in range(1,k+1):
      prev_centers[i] = cluster[i]

   for i in range(1, k+1):
      cluster[i] = update_ctr(i)

   for i in range(1,k+1):
      x1_diff = cluster[i][0] - prev_centers[i][0]
      x2_diff = cluster[i][1] - prev_centers[i][1]
      if x1_diff > 0.01 or x2_diff > 0.02:
         status = status or False
      else:
         status = status or True

   return status


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
            value = i
            matrix[key] = value

	    if i not in split_mtx.keys():
	       split_mtx[i] = []
	    split_mtx[i].append(key)
	    i += 1
	    if i > k:
	       i = 1

	 split_matrix()
	 intialize_clusters()
	 not_converged = update_centers()
	 print cluster
	 while (not_converged):
	    find_sdeviation()

	    for key in matrix:
	       update_cluster(key)
	    split_matrix()
	    update_membership()
	    not_converged = maximize_centers()
	    print cluster

	 #for i in range(1, k+1):
	 #   print len(split_mtx[i])

         c1x = []
         c1y = []
         c2x = []
         c2y = []
         c3x = []
         c3y = []

         f_output = open('em_algo_' + f_name, "w")
	 for key, value in matrix.items():
            f_output.write(str(key[0]) + '\t' + str(key[1]) + '\t' + str(value) + '\n')
            if value == 1:
               c1x.append(key[0])
               c1y.append(key[1])

            if value == 2:
               c2x.append(key[0])
               c2y.append(key[1])

            if value == 3:
               c3x.append(key[0])
               c3y.append(key[1])

         img_name = f_name.split('.')[0] + '_em.png'
         pylab.plot(c1x, c1y, color='r')
         pylab.plot(c2x, c2y, color='g')
         pylab.plot(c3x, c3y, color='b')

         pylab.xlabel('x1')
         pylab.ylabel('x2')

         pylab.savefig(img_name, bbox_inches='tight')







#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 11:36:23 2023

@author: ananya
"""

import numpy as np
import sys
import os

##########################################

# dashed line in output

def prl():
  print("-------------------------------------------------------")


##########################################

prl()
print("get_d_from_VolInt.py")
prl()

args = sys.argv[1:]
argc = len(args)

if argc == 0:

  print("Usage:")
  print("get_d_from_VolInt.py file_path")
  print()
  print("file_path: path to data file")
  print()
  print("Output in file with: column 1: time, column 2: distance.")

elif argc != 1:

  print("Incorrect commandline specs.")

else:

  path = args[0]
  print("file:\n"+path)

  if os.path.isfile(path):

    try:
      # get data from file
      data = np.loadtxt(path)

      # time
      i_t = 0
      t = data[:,i_t]

      # coordinates of first star
      i_x1 = 2
      x1 = data[:,i_x1]   / data[:,i_x1+3]
      y1 = data[:,i_x1+1] / data[:,i_x1+3]
      z1 = data[:,i_x1+2] / data[:,i_x1+3]

      # coordinates of second star
      i_x2 = 7
      x2 = data[:,i_x2]   / data[:,i_x2+3]
      y2 = data[:,i_x2+1] / data[:,i_x2+3]
      z2 = data[:,i_x2+2] / data[:,i_x2+3]

      # differences:
      x = x2-x1
      y = y2-y1
      z = z2-z1

      # calculating distance
      d = np.sqrt(x*x + y*y + z*z)

      name = path+'.td.txt'
      print("output in file:\n"+name)
      np.savetxt(name, np.transpose([t,d]),
                 header='Col. 1: Time\n'
                        'Col. 2: Coordinate separation between '
                                 'the centers of mass of the stars')

    except:
      print("Something went wrong with reading data.")

  else:
    print("Cannot find file.")

prl()
print("Exiting program.")
prl()

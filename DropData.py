#!/usr/bin/env python

# DropData - Drop data in a file if it is not close to average
#
# Copyright (C) 2015 Wolfgang Tichy
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import print_function

import argparse
#import sys
import numpy as np
from scipy import optimize

# use pythons arg parser
parser = argparse.ArgumentParser(description=
    '''Drop some data lines in a file and then reprint it''',
    epilog='''Example:
    DropData.py -c 7 bam0/moving_puncture_distance.lxyz6 > mpd.txt ;
    tgraph.py -c 9:7 mpd.txt''')
parser.add_argument('-c', metavar='COL', dest='distcolumn',
        default=2, help='column (counting from 1) in file we use ')
parser.add_argument('file', help='pathname of distance file')

args = parser.parse_args()
print("# Data from file:", args.file)

##################################################################
# set Columns we use
dcol = int(args.distcolumn) - 1

print("# Column (counting from 1) we inspect:", dcol+1)

##################################################################
# load data
data = np.loadtxt(args.file, comments=['#', '"', '$'])

# get data
ddata = data[:,dcol]
#print("# d0 =", ddata[0])
#print("# de =", ddata[-1])

##################################################################
# reprint data but drop some lines

print("# data from file where we dropped some lines")

ndata = len(ddata)
for i in range(0, ndata):
    if i>=2 and i<ndata-2:
        av4 = (ddata[i-2] + ddata[i-1] + ddata[i+1] + ddata[i+2])*0.25
        if ddata[i] < 0.9*av4:
            continue
    #print(np.array_str(data[i]))
    datline = data[i]
    for el in datline:
        print(el, end='  ')
    print()

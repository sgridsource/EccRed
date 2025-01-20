#!/usr/bin/env python

# EccRed - Fit proper distance to 
#          d(t)=S0+A0*t+0.5*A1*t^2-(B/omega)cos(omega*t+phi).
#          Then estimate the changes drdot and dOmega needed in SGRID pars
#          DNSdata_rdot and DNSdata_Omega to reduce the measured eccentricity ecc.
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
    '''Fit proper distance to 
    d(t)=S0+A0*t+0.5*A1*t^2-(B/omega)cos(omega*t+phi).
    Then estimate the changes drdot and dOmega needed in SGRID pars
    DNSdata_rdot and DNSdata_Omega to reduce the measured eccentricity ecc.''',
    epilog='''Example:
    EccRed_noForceBal.py bam0/moving_puncture_distance.lxyz4
    --Mass 3 --Omega 0.007030695  --tskip 200 --dmin 31 > d.txt ;
    tgraph.py d.txt -c 1:3 d.txt''')
parser.add_argument('--Mass', metavar='MASS', dest='Mass',
        help='total mass of binary')
parser.add_argument('--Omega', metavar='OMEGA', dest='Omega',
        help='orbital angular velocity')
parser.add_argument('--tskip', metavar='TIMESKIP', dest='tskip',
        default=200.0,
        help='initial time interval to skip')
parser.add_argument('--dmin', metavar='D_MIN', dest='dmin',
        default=31.0, help='minimum d we read in')
parser.add_argument('-ct', metavar='TCOL', dest='timecolumn',
        default=9, help='column (counting from 1) in file we use as time')
parser.add_argument('-cc', metavar='CDCOL', dest='coorddistcolumn',
        default=8, help='column (counting from 1) in file we use as coordinate distance')
parser.add_argument('-c', metavar='DCOL', dest='distcolumn',
        default=7, help='column (counting from 1) in file we use as distance')
parser.add_argument('file', help='pathname of distance file')

args = parser.parse_args()
#print(args.Omega)
#print(args.Mass)
print("# Opening:", args.file)
tskip = float(args.tskip)
dmin = float(args.dmin)
Mass = float(args.Mass)
print("# Skipping until time =", tskip)
print("# Dropping distances below", dmin)
#print(type(dmin))

##################################################################
# set Columns we use
tcol = int(args.timecolumn) - 1
dcol = int(args.distcolumn) - 1
dcoordcol = int(args.coorddistcolumn) - 1

print("# Columns (counting from 1) we use:")
print("# time:", tcol+1, "   distance:", dcol+1, "   r0:", dcoordcol+1)

##################################################################
# load data
data = np.loadtxt(args.file, comments=['#', '"', '$'])

# filter repeating time entries, e.g., after a restarts
_, mask = np.unique(data[:,tcol], return_index=True)
data = data[mask]

# get time data
tdata = data[:,tcol]

# drop all before tskip
idrop = 0
for i in range(0, len(tdata)):
    if tdata[i] >= tskip:
        idrop = i
        break
# delete col 0 to idrop in data
data = data[idrop:]

# get distance data
ddata = data[:,dcol]
# drop all after distance dmin
iout = len(ddata)
#print(iout)
for i in range(0, len(ddata)):
    if ddata[i] < dmin:
        iout = i
        break
#print(iout)

# keep only 0 to iout in data
data = data[0:iout]

# get tdata and ddata of reduced data array
tdata = data[:,tcol]
ddata = data[:,dcol]

print("# t0 , d0 =", tdata[0], ",", ddata[0])
print("# te , de =", tdata[-1], ",", ddata[-1])

##################################################################
# model for d(t), dpending on pars S0, A0,A1,B, omega,phi
def d_of_t_model(t,  S0, A0,A1,B, omega,phi):
    return S0 + A0*t + 0.5*A1*t*t - (B/omega) * np.cos(omega*t + phi)

##################################################################
# find initial guess for pars
d0 = ddata[0]
de = ddata[-1]
dT = tdata[-1] - tdata[0]
ddot = (de - d0)/dT
OmegaKepler = np.sqrt(Mass/d0**3)
pinit = [d0, ddot,0,0, OmegaKepler, 0]

# use curve_fit from scipy
popt, pcov = optimize.curve_fit(d_of_t_model, tdata, ddata, p0=pinit)
S0 = popt[0]
A0 = popt[1]
A1 = popt[2]
B  = popt[3]
omega = popt[4]
phi   = popt[5]

# print data and fitted curve:
print("# time  d  d_fit")
for i in range(len(tdata)):
    print(tdata[i], ddata[i], d_of_t_model(tdata[i],  S0, A0,A1,B, omega,phi))

print()
print("# S0 =", S0)
print("# A0 =", A0)
print("# A1 =", A1)
print("# B  =", B)
print("# omega =", omega)
print("# phi =", phi)

##################################################################
# calc ecc, drdot, dOmega from fit
def eval_pars(S0, A0,A1,B, omega,phi,  r0, Omega):
    ecc = -B/(omega*r0)
    drdot = -B*np.sin(phi)
    dOmega = -B*omega*np.cos(phi)/(2.0 * r0 * Omega)
    return ecc, drdot, dOmega

##################################################################
# print results
if args.Omega == None:
    Omega = omega
else:
    Omega = float(args.Omega)

print()
print("# Results for:  r0 = d0 =", d0, "  Omega =", Omega)
ecc, drdot, dOmega = eval_pars(S0, A0,A1,B, omega,phi,  d0, Omega)
print("# ecc =", ecc)
print("# drdot  =", drdot)
print("# dOmega =", dOmega)

print()
r0 = data[0,dcoordcol]
print("# Best Results for:  r0 =", r0, "  Omega =", Omega)
ecc, drdot, dOmega = eval_pars(S0, A0,A1,B, omega,phi,  r0, Omega)
print("# ecc =", ecc)
print("# drdot  =", drdot)
print("# dOmega =", dOmega)

#!/usr/bin/env python


### Script to define scan grid

### Authors:
### Manuel Franco Sevilla
### Ana Ovcharova

import os,sys,math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from grid_utils import *
    
model = "VBF_EWKino_DemocraticSlepton_mChargino-375to400"
process = "C1N2"

# Parameters that define the grid in the bulk and diagonal
class gridBlock:
  def __init__(self, xmin, xmax, xstep):
    self.xmin = xmin
    self.xmax = xmax
    self.xstep = xstep

scanBlocks = []
scanBlocks.append(gridBlock(375, 401, 25))

deltaM = [ 0.5, 1, 5, 10, 15, 20, 30, 40, 50, 60, 75 ] 

# Number of events for mass point, in thousands
nev = 250

# -------------------------------
#    Constructing grid

cols = []
Nevents = []
xmin, xmax = 9999, 0
ymin, ymax = 9999, 0
for block in scanBlocks:
  Nbulk, Ndiag = 0, 0
  xmin = min(xmin, block.xmin)
  xmax = max(xmax, block.xmax)
  for mx in range(block.xmin, block.xmax, block.xstep):
    col = []
    for dm in deltaM:
      my = mx-dm
      if my>=0.: 
        ymin = min(ymin, my)
        ymax = max(ymax, my)
        col.append([mx,my,nev])
        Nbulk += nev
    cols.append(col)
  Nevents.append([Nbulk, Ndiag])

mpoints = []
for col in cols: mpoints.extend(col)

## Test print out for repeated points
mset = set()
for mp in mpoints: mset.add(mp[0]*10000+mp[1])
Npts, Ndiff = len(mpoints), len(mset)
if Npts==Ndiff: print "\nGrid contains "+str(Npts)+" mass points. No duplicates\n"
else: print "\n\nGRID CONTAINS "+str(Npts-Ndiff)+" DUPLICATE POINTS!!\n\n"

# -------------------------------
#     Plotting and printing

Ntot = makePlot(cols, 'events', model, process, xmin, xmax, ymin, ymax)

print '\nScan contains '+"{0:,.0f}".format(Ntot*1000)+" events"

print


print 'Average efficiency of: ', getAveEff(mpoints, process)

print


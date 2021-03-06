#!/usr/bin/env python

### Script to define scan grid

### Authors:
### Manuel Franco Sevilla
### Ana Ovcharova

import os,sys,math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from grid_utils import *

model = "TChipmWW"
process = "C1C1"

# Number of events for mass point, in thousands
nevt = 100

diag_low, diag_high = 10, 3
xmin, xmax, xstep = 100, 600, 25
ymin, ymax, ystep_low, ystep_high = 50, 600, 10, 2


# -------------------------------
#    Constructing grid

mpoints = []
for mx in range(xmin, xmax+1, xstep):
  ylist = []
  if mx > (ymax + (diag_low - diag_high)): 
    ylist.extend(range(ymin, ymax+1, ystep_low))
  elif mx > ymax:
    ylist.extend(range(ymin, mx - diag_low, ystep_low))
    ylist.extend(range(mx - diag_low, ymax+1, ystep_high))
  else:
    ylist.extend(range(ymin, mx - diag_low, ystep_low))
    ylist.extend(range(mx - diag_low, mx-diag_high+1, ystep_high))
  for my in ylist:
    if mx-my > ymin:
      continue
    else:
      mpoints.append([mx,my,nevt])
    
# Need to remove points with dM less than ymin (50)

## Test print out for repeated points
mset = set()
for mp in mpoints: mset.add(mp[0]*10000+mp[1])
Npts, Ndiff = len(mpoints), len(mset)
if Npts==Ndiff: print "\nGrid contains "+str(Npts)+" mass points. No duplicates\n"
else: print "\n\nGRID CONTAINS "+str(Npts-Ndiff)+" DUPLICATE POINTS!!\n\n"

# -------------------------------
#     Plotting and printing

Ntot = makePlot([mpoints], 'events', model, process, xmin, xmax, ymin, ymax)

print '\nScan contains '+"{0:,.0f}".format(Ntot*1000)+" events"
print 'Average matching efficiency (for McM and GEN fragment) = '+"{0:.3f}".format(getAveEff(mpoints,process))

print

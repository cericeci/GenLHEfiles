import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP2Settings_cfi import *

import math

baseSLHATable="""
BLOCK MASS  # Mass Spectrum
# PDG code           mass       particle
   1000001     1.00000000E+05   # ~d_L
   2000001     1.00000000E+05   # ~d_R
   1000002     1.00000000E+05   # ~u_L
   2000002     1.00000000E+05   # ~u_R
   1000003     1.00000000E+05   # ~s_L
   2000003     1.00000000E+05   # ~s_R
   1000004     1.00000000E+05   # ~c_L
   2000004     1.00000000E+05   # ~c_R
   1000005     1.00000000E+05   # ~b_1
   2000005     1.00000000E+05   # ~b_2
   1000006     %MSTOP%          # ~t_1
   2000006     1.00000000E+05   # ~t_2
   1000011     1.00000000E+05   # ~e_L
   2000011     1.00000000E+05   # ~e_R
   1000012     1.00000000E+05   # ~nu_eL
   1000013     1.00000000E+05   # ~mu_L
   2000013     1.00000000E+05   # ~mu_R
   1000014     1.00000000E+05   # ~nu_muL
   1000015     1.00000000E+05   # ~tau_1
   2000015     1.00000000E+05   # ~tau_2
   1000016     1.00000000E+05   # ~nu_tauL
   1000021     1.00000000E+05    # ~g
   1000022     %MLSP%           # ~chi_10
   1000023     1.00000000E+05   # ~chi_20
   1000025     1.00000000E+05   # ~chi_30
   1000035     1.00000000E+05   # ~chi_40
   1000024     %MCHI%           # ~chi_1+
   1000037     1.00000000E+05   # ~chi_2+

# DECAY TABLE
#         PDG            Width
DECAY   1000001     0.00000000E+00   # sdown_L decays
DECAY   2000001     0.00000000E+00   # sdown_R decays
DECAY   1000002     0.00000000E+00   # sup_L decays
DECAY   2000002     0.00000000E+00   # sup_R decays
DECAY   1000003     0.00000000E+00   # sstrange_L decays
DECAY   2000003     0.00000000E+00   # sstrange_R decays
DECAY   1000004     0.00000000E+00   # scharm_L decays
DECAY   2000004     0.00000000E+00   # scharm_R decays
DECAY   1000005     0.00000000E+00   # sbottom1 decays
DECAY   2000005     0.00000000E+00   # sbottom2 decays
DECAY   1000006     1.00000000E+00   # stop1 decays # taken from T2bt
    0.00000000E+00    3    1000022      5     24  # dummy allowed decay, in order to turn on off-shell decays
    0.50000000E+00    2    1000022      6
    0.50000000E+00    2    1000024      5
DECAY   2000006     0.00000000E+00   # stop2 decays

DECAY   1000011     0.00000000E+00   # selectron_L decays
DECAY   2000011     0.00000000E+00   # selectron_R decays
DECAY   1000012     0.00000000E+00   # snu_elL decays
DECAY   1000013     0.00000000E+00   # smuon_L decays
DECAY   2000013     0.00000000E+00   # smuon_R decays
DECAY   1000014     0.00000000E+00   # snu_muL decays
DECAY   1000015     0.00000000E+00   # stau_1 decays
DECAY   2000015     0.00000000E+00   # stau_2 decays
DECAY   1000016     0.00000000E+00   # snu_tauL decays
DECAY   1000021     0.00000000E+00   # gluino decays
DECAY   1000022     0.00000000E+00   # neutralino1 decays
DECAY   1000023     0.00000000E+00   # neutralino2 decays
DECAY   1000024     %WCHI%           # chargino1 decays # taken from T2bW_X05_dM-10to80 (or better https://github.com/CMS-SUS-XPAG/GenLHEfiles/blob/master/GridpackWorkflow/production/models/T2bt/T2bt_fragment.py#L71-80 ?)
#   0.00000000E+00    3    1000022    12   -11  # dummy allowed decay, in order to turn on off-shell decays
    1.00000000E+00    2    211  1000022         # x1+  -->  n1 pi+
DECAY   1000025     0.00000000E+00   # neutralino3 decays
DECAY   1000035     0.00000000E+00   # neutralino4 decays
DECAY   1000037     0.00000000E+00   # chargino2+ decays
"""

generator = cms.EDFilter("Pythia8GeneratorFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    RandomizedParameters = cms.VPSet(),
)

model = "T2bt-LLChipm_ctau-"

ctau =  {"10cm":[0.32485759,1.97327052176253113e-15],"200cm":[0.18288376,0.9866600820631833e-16]} # Tag : [dM, width]

# weighted average of matching efficiencies for the full scan
# must equal the number entered in McM generator params
mcm_eff = 0.2427

def matchParams(mass):
    if mass>99 and mass<199: return 62., 0.498
    elif mass<299: return 62., 0.361
    elif mass<399: return 62., 0.302
    elif mass<499: return 64., 0.275
    elif mass<599: return 64., 0.254
    elif mass<1299: return 68., 0.237
    elif mass<1451: return 70., 0.243
    elif mass<1801: return 74., 0.246
    elif mass<2001: return 76., 0.267
    elif mass<2201: return 78., 0.287
    elif mass<2601: return 80., 0.320
    elif mass<2801: return 84., 0.347
    elif mass<3801: return 84., 0.347

def xsec(mass): #Analytical fit to the xsec
  if mass < 300: return 319925471928717.38*math.pow(mass, -4.10396285974583*math.exp(mass*0.0001317804474363))
  else: return 6953884830281245*math.pow(mass, -4.7171617288678069*math.exp(mass*6.1752771466190749e-05))

# Parameters that define the grid in the bulk and diagonal
class gridBlock:
  def __init__(self, xmin, xmax, xstep, ystep):
    self.xmin = xmin
    self.xmax = xmax
    self.xstep = xstep
    self.ystep = ystep

# Number of events: min(goalLumi*xsec, maxEvents) (always in thousands)
goalLumi = 400
minLumi = 1e-40 # Skip minimum lumi
minEvents, maxEvents = 20, 70 #Points that require more than 70k events for goal lumi are sure to be excluded/seen so let's cut events there
diagStep, bandStep = 50, 50
midDM, maxDM = 300, 700
addDiag = [183, 167] # DeltaM for additional diagonal lines to be added

scanBlocks = []
scanBlocks.append(gridBlock(400,  1751, 50, 50))
minDM = 85
ymin, ymed, ymax = 0, 0, 1650

# Number of events for mass point, in thousands
def events(mass):
  xs = xsec(mass)
  nev = min(goalLumi*xs, maxEvents*1000)
  if nev < xs*minLumi: nev = xs*minLumi
  nev = max(nev/1000, minEvents)
  return math.ceil(nev) # Rounds up

# -------------------------------
#    Constructing grid

cols = []
Nevents = []
xmin, xmax = 9999, 0
for block in scanBlocks:
  for ct in ctau:
    Nbulk, Ndiag = 0, 0
    for mx in range(block.xmin, block.xmax, min(bandStep, diagStep)):
      #mx==block.xmin : continue
      xmin = min(xmin, block.xmin)
      xmax = max(xmax, block.xmax)
      col = []
      my = 0
      begBand = min(max(ymed, mx-maxDM), mx-minDM)
      begDiag = min(max(ymed, mx-midDM), mx-minDM)
      # Adding bulk points
      if (mx-block.xmin)%block.xstep == 0 :
        for my in range(ymin, begBand, block.ystep):
          if my > ymax: continue
          # Adding extra diagonals to the bulk
          for dm in addDiag:
            #if(len(cols)==0 and batch==1): continue # Don't add point before the beginning
            dm_before = mx-block.xstep -my
            dm_after = mx - my
            if(dm>dm_before and dm<dm_after):
              nev = events(my+dm)
              col.append([mx,mx-dm, nev, ct])
              Nbulk += nev
          nev = events(mx)
          col.append([mx,my, nev, ct])
          Nbulk += nev
      # Adding diagonal points in inside band
      if (mx-block.xmin)%bandStep == 0 :
        for my in range(begBand, mx-midDM, bandStep):
          if my > ymax: continue
          # Adding extra diagonals to the band
          for dm in addDiag:
            #if(len(cols)==0 and batch==1): continue # Don't add point before the beginning
            dm_before = mx-bandStep -my
            dm_after = mx - my
            if(dm>dm_before and dm<dm_after):
              nev = events(my+dm)
              col.append([mx,mx-dm, nev, ct])
              Ndiag += nev
          # Adding standard diagonal points
          nev = events(mx)
          col.append([mx,my, nev, ct])
          Ndiag += nev
      # Adding diagonal points in band closest to outer diagonal
      for my in range(begDiag, mx-minDM+1, diagStep):
        # Adding extra diagonals to the band
        for dm in addDiag:
          #if(len(cols)==0 and batch==1): continue # Don't add point before the beginning
          dm_before = mx-diagStep -my
          dm_after = mx - my
          if(dm>dm_before and dm<dm_after):
            nev = events(my+dm)
            col.append([mx,mx-dm, nev, ct])
            Ndiag += nev
        nev = events(mx)
        col.append([mx,my, nev, ct])
        Ndiag += nev
      if(my !=  mx-minDM and mx-minDM <= ymax):
        my = mx-minDM
        nev = events(mx)
        col.append([mx,my, nev, ct])
        Ndiag += nev
      cols.append(col)
    Nevents.append([Nbulk, Ndiag])

mpoints = []
for col in cols: mpoints.extend(col)

import os
for point in mpoints:
    mstop, mlsp = point[0], point[1]
    qcut, tru_eff = matchParams(mstop)
    wgt = point[2]*(mcm_eff/tru_eff)
    DeltaM = ctau[point[3]][0]
    ChiWidth = ctau[point[3]][1]
    if mlsp==0: mlsp = 1
    mchi = mlsp + DeltaM
    slhatable = baseSLHATable.replace('%MSTOP%','%e' % mstop)
    slhatable = slhatable.replace('%MLSP%','%e' % mlsp)
    slhatable = slhatable.replace('%MCHI%','%e' % mchi)
    slhatable = slhatable.replace('%WCHI%','%e' % ChiWidth)

    basePythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP2SettingsBlock,
        JetMatchingParameters = cms.vstring(
            'JetMatching:setMad = off',
            'JetMatching:scheme = 1',
            'JetMatching:merge = on',
            'JetMatching:jetAlgorithm = 2',
            'JetMatching:etaJetMax = 5.',
            'JetMatching:coneRadius = 1.',
            'JetMatching:slowJetPower = 1',
            'JetMatching:qCut = %.0f' % qcut, #this is the actual merging scale
            'JetMatching:nQmatch = 5', #4 corresponds to 4-flavour scheme (no matching of b-quarks), 5 for 5-flavour scheme
            'JetMatching:nJetMax = 2', #number of partons in born matrix element for highest multiplicity
            'JetMatching:doShowerKt = off', #off for MLM matching, turn on for shower-kT matching
            '6:m0 = 172.5',
            '24:mMin = 0.1',
            'Check:abortIfVeto = on',
        ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP2Settings',
                                    'JetMatchingParameters'
        )
    )

    generator.RandomizedParameters.append(
        cms.PSet(
            ConfigWeight = cms.double(wgt),
            GridpackPath =  cms.string('/cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/madgraph/V5_2.4.2/sus_sms/LO_PDF/SMS-StopStop/v1/SMS-StopStop_mStop-%i_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz' % mstop),
            ConfigDescription = cms.string('%s_%i_%i_ctau-%s' % (model, mstop, mlsp, point[3])),
            SLHATableForPythia8 = cms.string('%s' % slhatable),
            PythiaParameters = basePythiaParameters,
        ),
    )


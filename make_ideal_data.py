# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
from mantid.geometry import CrystalStructure
import matplotlib.pyplot as plt
import numpy as np

from collections import namedtuple

def convert(dictionary):
    return namedtuple('GenericDict', dictionary.keys())(**dictionary)

# --- setup simulated workspace
# lattice constant for Si
# data from Mantid web documentation
lc_silicon = {
    "a": 5.431,  # A 
    "b": 5.431,  # A 
    "c": 5.431,  # A
    "alpha": 90,  # deg
    "beta": 90,  # deg
    "gamma": 90,  # deg
}
silicon = convert(lc_silicon)
cs_silicon = CrystalStructure(
    f"{silicon.a} {silicon.b} {silicon.c}",
    "F d -3 m",
    "Si 0 0 0 1.0 0.05",
)

lc_natrolite = {
    "a": 18.29,  # A
    "b": 18.64,  # A
    "c": 6.56,  # A
    "alpha": 90,  # deg
    "beta": 90,  # deg
    "gamma": 90,  # deg
}
natrolite = convert(lc_natrolite)

# Generate simulated workspace for CORELLI
CreateSimulationWorkspace(
#     Instrument='CORELLI',
    Instrument='TOPAZ',
    BinParams='1,100,10000',
    UnitX='TOF',
    OutputWorkspace='cws',
)
cws = mtd['cws']

# Set the UB matrix for the sample
# u, v is the critical part, we can start with the
# ideal position
SetUB(
    Workspace="cws",
    u='1,0,0',  # vector along k_i, when goniometer is at 0
    v='0,1,0',  # in-plane vector normal to k_i, when goniometer is at 0
#     **lc_silicon,
    **lc_natrolite,
)

# set the crystal structure for virtual workspace
# cws.sample().setCrystalStructure(cs_silicon)

# Generate predicted peak workspace
dspacings = convert({'min': 1.0, 'max': 10.0})
wavelengths = convert({'min': 0.8, 'max': 2.9})

# Collect peaks over a range of omegas
CreatePeaksWorkspace(OutputWorkspace='pws')
omegas = range(0, 180, 3)

for omega in omegas:
    SetGoniometer(
        Workspace="cws",
        Axis0=f"{omega},0,1,0,1",
    )

    PredictPeaks(
        InputWorkspace='cws',
        WavelengthMin=wavelengths.min,
        wavelengthMax=wavelengths.max,
        MinDSpacing=dspacings.min,
        MaxDSpacing=dspacings.max,
        ReflectionCondition='All-face centred',
        OutputWorkspace='_pws',
    )

    CombinePeaksWorkspaces(
        LHSWorkspace="_pws",
        RHSWorkspace="pws",
        OutputWorkspace="pws",
    )

IndexPeaks("pws")

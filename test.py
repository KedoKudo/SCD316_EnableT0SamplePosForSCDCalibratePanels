# necessary import
import numpy as np
from collections import namedtuple
from mantid.simpleapi import *
from mantid.geometry import CrystalStructure
from mantid.kernel import V3D
from corelli.calibration.powder import load_and_rebin

def convert(dictionary):
    return namedtuple('GenericDict', dictionary.keys())(**dictionary)

import os
directory = os.path.dirname(os.path.realpath(__file__))

lc_scolecite = {
    "a": 6.51201,  # A
    "b": 18.95454,  # A
    "c": 9.75822,  # A
    "alpha": 90,  # deg
    "beta": 108.9211 ,  # deg
    "gamma": 90,  # deg
}

scolecite = convert(lc_scolecite)

LoadIsawPeaks("data/SC100K_Monoclinic_C.integrate", OutputWorkspace="pws")
LoadIsawUB('pws', 'data/SC100K_Monoclinic_C.mat')

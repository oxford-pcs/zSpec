'''
  This test program constructs an array of field points for the entrance slit 
  corresponding and then then calculates the WFE for each of these points.
'''

import argparse
from decimal import Decimal

import numpy as np
import pylab as plt
import pyzdde.zdde as pyz    

from spectrograph import Spectrograph
from slit import slit
from detector import detector 
from zController.Controller import Controller

if __name__== "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-co", help="collimator ZEMAX file", default="C:\\Users\\barnsley\\Google Drive\\Spectrograph_Optics\\collimator60.zmx")
  parser.add_argument("-ca", help="camera ZEMAX file", default="C:\\Users\\barnsley\\Google Drive\\Spectrograph_Optics\\camera70.ZMX")    
  parser.add_argument("-ws", help="wavelength start (micron)", default="0.675", type=Decimal)
  parser.add_argument("-we", help="wavelength end (micron)", default="0.925", type=Decimal)
  parser.add_argument("-wi", help="wavelength interval (micron)", default="0.125", type=Decimal)
  parser.add_argument("-s", help="slit name (brick_wall pattern only)", default="SWIFT")
  parser.add_argument("-nf", help="number of fields to be considered per slitlet", default=1, type=int)
  parser.add_argument("-sf", help="slits file", default="slits.json")
  args = parser.parse_args()
  
  zmx_link = pyz.createLink()
  zcontroller = Controller(zmx_link)
  
  s = Spectrograph(args.co, args.ca, zcontroller)
  
  slit_pattern = slit(args.sf, args.s)
  pattern_data = slit_pattern.cfg['pattern_data']
  
  fields = slit_pattern.getFieldsFromSlitPattern(nfields=pattern_data['n_slitlets']*args.nf)

  for w in np.arange(args.ws, args.we+args.wi, args.wi, dtype=Decimal):
    print "Processing wavelength " + str(w) + " micron ..."
    wfe_data_coll, wfe_headers_coll = s.collimator.getWFE(fields, w)
    
  pyz.closeLink()
    
  exit(0)

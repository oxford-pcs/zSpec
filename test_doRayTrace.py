'''
  This test program constructs an array of field points for the entrance slit 
  corresponding to each pixel at the detector plane then raytraces the 
  system for each of these points.
  
  A fictitious detector with 480 micron pixel pitch is used to keep things fast.
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
  parser.add_argument("-s", help="slit name", default="SWIFT")
  parser.add_argument("-d", help="detector name", default="test")
  parser.add_argument("-sf", help="slits file", default="slits.json")
  parser.add_argument("-df", help="detectors file", default="detectors.json")
  args = parser.parse_args()
  
  zmx_link = pyz.createLink()
  zcontroller = Controller(zmx_link)
  
  s = Spectrograph(args.co, args.ca, zcontroller)
  
  slit_pattern = slit(args.sf, args.s)
  detector = detector(args.df, args.d)
  
  wave_c = args.ws + ((args.we - args.ws) / Decimal(2.))

  M = s.calculateMagnification(wave_c)
  detector_pixel_pitch = detector.cfg['detector_data']['pitch'] / 1000. # mm
  size_of_detector_pixel_at_slit_plane = detector_pixel_pitch / M
  
  fields = slit_pattern.getFieldsFromSlitPattern(sampling=size_of_detector_pixel_at_slit_plane)

  for w in np.arange(args.ws, args.we+args.wi, args.wi, dtype=Decimal):
    print "Processing wavelength " + str(w) + " micron ..."
    im_xys = s.doRayTrace(fields, w)
    plt.plot([xy[0] for xy in im_xys], [xy[1] for xy in im_xys], 'o', 
             label=str(w))

  plt.legend()
  plt.show()
    
  pyz.closeLink()
    
  exit(0)

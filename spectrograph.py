import numpy as np
import pylab as plt

from collimator import Collimator
from camera import Camera
from zController.Controller import Controller

class Spectrograph():
  def __init__(self, collimator_zmx_file, camera_zmx_file, zcontroller):
    self.collimator = Collimator(collimator_zmx_file, zcontroller)
    self.camera = Camera(camera_zmx_file, zcontroller)
    self.zcontroller = zcontroller
  
  def calculateMagnification(self, wave, verbose=True, debug=False):
    ''' 
      Calculate spectrograph magnification at a given wavelength where:
      
      magnification = EFL (cam) / EFL (coll) 
    '''
    if verbose:
      print "Calculating spectrographic magnification at wavelength of " +\
        str(wave) + " micron... "
    
    return self.camera.getEFL(wave) / self.collimator.getEFL(wave) 

  def doRayTrace(self, fields, wave):
    '''
      Trace rays through the spectrograph system at wavelength [wavelength, um] 
      for list of xy tuples, fields [fields].
      
      Returns the xy at the image plane for each field.
    '''
    camera_oa = self.collimator.doRayTraceForObjectHeights(fields, wave)
    im_xys = self.camera.doRayTraceForObjectAngles(camera_oa, wave, 
                                                   reverse_fields_xy=True)
  
    return im_xys
  
  def getSystemWFE(self):
    self.collimator.getWFE()
    self.camera.getWFE()

    

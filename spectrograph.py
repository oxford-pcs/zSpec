import numpy as np
import pylab as plt

from component import Collimator, Camera
from zController.Controller import Controller

class Spectrograph():
  def __init__(self, collimator_zmx_file, camera_zmx_file, zcontroller):
    self.collimator = Collimator(collimator_zmx_file, zcontroller)
    self.camera = Camera(camera_zmx_file, zcontroller)
    self.zcontroller = zcontroller
  
  def calculateMagnification(self, wavelength, verbose=True, debug=False):
    ''' 
      Calculate spectrograph magnification at a given wavelength where:
      
      magnification = EFL (cam) / EFL (coll) 
    '''
    if verbose:
      print "Calculating spectrographic magnification at wavelength of " +\
        str(wavelength) + " micron... "
    
    return self.camera.getEFL(wavelength) / self.collimator.getEFL(wavelength) 

  def doSystemRayTrace(self, object_heights, wavelength, flip_camera_OA=False):
    '''
      Trace rays through the spectrograph system at wavelength [wavelength, um] 
      for list of field xy tuples [object_heights].
      
      Returns the camera object angles and xy positions at the image plane for 
      each field.
    '''
    camera_OAs = self.collimator.getOA(object_heights, wavelength)
    if flip_camera_OA:
      camera_OAs = [(angle[1], angle[0]) for angle in camera_OAs]
      
    im_xys = self.camera.getImXY(camera_OAs, wavelength)
  
    return camera_OAs, im_xys
  
  def getSystemWFE(self, fields, wavelength):
    # HELP? do i need to flip pupil xy?
    self.collimator.getWFE(fields, wavelength)
    self.camera.getWFE(fields, wavelength)

    

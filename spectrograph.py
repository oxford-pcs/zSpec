import numpy as np
import pylab as plt
import pyzdde.zdde as pyz    

from component import *
from zController.Controller import Controller

class zSpectrograph():
  def __init__(self, collimator_zmx_file, camera_zmx_file):
    self.zmx_link = pyz.createLink()
    self.zcontroller = Controller(self.zmx_link)

    self.collimator = Collimator(collimator_zmx_file, self.zcontroller)
    self.camera = Camera(camera_zmx_file, self.zcontroller)

  def __del__(self):   
    self.zmx_link.close()

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

  def getSystemAttr(self, wavelength):
    '''
      Get some key attributes of the spectrograph system.
    '''
    attr = {
      "camera_EFFL": self.camera.getEFFL(wavelength),
      "camera_ENPD": self.camera.getENPD(wavelength),
      "camera_EXPD": self.camera.getEXPD(wavelength),
      "camera_WFNO": self.camera.getWFNO(wavelength),
      "collimator_EFFL": self.collimator.getEFFL(wavelength),
      "collimator_ENPD": self.collimator.getENPD(wavelength),
      "collimator_EXPD": self.collimator.getEXPD(wavelength),
      "collimator_WFNO": self.collimator.getWFNO(wavelength),
    }
    return attr

    

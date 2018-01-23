import numpy as np
import pylab as plt
import pyzdde.zdde as pyz

class Component(object):
  def __init__(self, zmx_file, zcontroller, lumultiplier):
    '''
      Initialise a component.

      [lumultiplier] is used to move from Zemax lens units to another
      physical dimension. By default, Zemax does its calculations in
      mm, so a lumultiplier of 1e3 moves this to m.
    '''
    self.file_pathname = zmx_file
    self.zcontroller = zcontroller
    self.lumultiplier = lumultiplier

  def _doAnalysisWFE(self, fields, field_type, wavelength, verbose=True, debug=False):
    if not self.zcontroller.isFileAlreadyLoaded(self.file_pathname):
      self.zcontroller.loadZemaxFile(self.file_pathname)
    self.zcontroller.setWavelengthNumberOf(1)
    self.zcontroller.setWavelengthValue(wavelength, 1)
    
    data, headers = self.zcontroller.getAnalysisWFEForFields(fields, field_type)
    
    return data, headers
  
  def _doRayTrace(self, fields, field_type, wavelength, verbose=True, debug=False):  
    if not self.zcontroller.isFileAlreadyLoaded(self.file_pathname):
      self.zcontroller.loadZemaxFile(self.file_pathname)
    self.zcontroller.setWavelengthNumberOf(1)
    self.zcontroller.setWavelengthValue(wavelength, 1)
    
    rays = self.zcontroller.doRayTraceForFields(fields, field_type=field_type, 
                                                px=0, py=0)
    tmp = []
    for ray in rays:
      tmp.append({
        'x': ray.x * self.lumultiplier,
        'y': ray.y * self.lumultiplier,
        'z': ray.z * self.lumultiplier,
        'dcos_l': ray.dcos_l,
        'dcos_m': ray.dcos_m,
        'dcos_n': ray.dcos_n
        })
    rays = tmp

    if debug:
      for idx, ray in enumerate(rays):
        if idx == 0:
          print
          print "field\tx\ty\tz"
        print idx, '\t', round(ray['x'], 2), '\t', round(ray['y'], 2), \
              '\t', round(ray['z'], 2)
        if idx == len(rays):
          print
          
      plt.plot()
      for field, ray in zip(fields, rays):
        plt.plot(rays['x'], ray['y'], 'o', label=str('[' + str(field[0]) + 
                                      ', ' + str(field[1]) + 
                                      ']'))
      plt.legend(loc='upper right', numpoints=1)
      plt.show()    

    return rays
    
  def getEFL(self, wavelength, verbose=False):
    if verbose:
      print "Getting EFL for component... "
      
    if not self.zcontroller.isFileAlreadyLoaded(self.file_pathname):
      self.zcontroller.loadZemaxFile(self.file_pathname)
    self.zcontroller.setWavelengthNumberOf(1)
    self.zcontroller.setWavelengthValue(wavelength, 1)
    return self.zcontroller.getLensData().EFL*self.lumultiplier

  def getWFNO(self, wavelength, verbose=False):
    if verbose:
      print "Getting WFNO for component... "
      
    if not self.zcontroller.isFileAlreadyLoaded(self.file_pathname):
      self.zcontroller.loadZemaxFile(self.file_pathname)
    self.zcontroller.setWavelengthNumberOf(1)
    self.zcontroller.setWavelengthValue(wavelength, 1)
    return self.zcontroller.getLensData().realWorkFNum

class Camera(Component):
  def __init__(self, camera_zmx_file, zcontroller, lumultiplier=1e-3):
    super(Camera, self).__init__(camera_zmx_file, zcontroller, lumultiplier)
    pass

  def getImXY(self, fields, wavelength, verbose=True, debug=False):
    '''
      Trace the chief ray from each collimated field point through the camera 
      and work out the corresponding (x, y) positions at the image plane.
    '''
    
    if verbose:
      print "Tracing object angles through camera..."
      
    rays = self._doRayTrace(fields, 0, wavelength, verbose=verbose, 
                            debug=debug)
    
    ImXYs = []
    for ray in rays:
      ImXYs.append((ray['x'], ray['y']))

    return ImXYs
 
  def getWFE(self, fields, wavelength, verbose=True, debug=False):
    '''
      Get the pupil WFE after passing through the camera.
    '''
    return self._doAnalysisWFE(fields, 0, wavelength, 
                               verbose=verbose, debug=debug)
    
class Collimator(Component):
  def __init__(self, collimator_zmx_file, zcontroller, lumultiplier=1e-3):
    super(Collimator, self).__init__(collimator_zmx_file, zcontroller,
                                     lumultiplier)
    pass
  
  def getOA(self, fields, wavelength, verbose=True, debug=False):
    '''
      Trace the chief ray for each field point in the slit through the 
      collimator and, using directional cosines and the relations 
      (p53 Zemax manual)
    
        tan(alpha) = direction_cosine(x)/direction_cosine(z)   .. (1)
        tan(beta) = direction_cosine(y)/direction_cosine(z)    .. (2)
      
      calculate the output field angles x and y (alpha and beta respectively).
    '''
    
    if verbose:
      print "Tracing object heights through collimator... "
      
    rays = self._doRayTrace(fields, 1, wavelength, verbose=verbose, 
                            debug=debug)
    
    OAs = []
    for ray in rays:
      OAs.append((np.degrees(np.arctan(ray['dcos_l']/ray['dcos_n'])), 
                             np.degrees(np.arctan(ray['dcos_m']/ray['dcos_n']))))
      
    return OAs
  
  def getWFE(self, fields, wavelength, verbose=True, debug=False):
    '''
      Get the pupil WFE after passing through the collimator.
    '''
    return self._doAnalysisWFE(fields, 1, wavelength, 
                               verbose=verbose, debug=debug)

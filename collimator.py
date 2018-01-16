import numpy as np
import pylab as plt
import pyzdde.zdde as pyz

class Collimator():
  def __init__(self, collimator_zmx_file, zcontroller):
    self.file = collimator_zmx_file
    self.zcontroller = zcontroller
  
  def doRayTraceForObjectHeights(self, object_heights, wavelength, verbose=True, 
                                 debug=False):
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
      
    self.zcontroller.loadZemaxFile(self.file)
    self.zcontroller.setWavelengthNumberOf(1)
    self.zcontroller.setWavelengthValue(wavelength, 1)
    
    rays = self.zcontroller.doRayTraceForFields(object_heights, field_type=1, 
                                                px=0, py=0)
    exit_angles = []
    for idx, ray in enumerate(rays):
      exit_angles.append((np.degrees(np.arctan(ray.dcos_l/ray.dcos_n)), 
                            np.degrees(np.arctan(ray.dcos_m/ray.dcos_n))))
      if debug:
        if idx == 0:
          print
          print "field\tx\ty\tz"
        print idx, '\t', round(ray.x, 2), '\t', round(ray.y, 2), '\t', \
          round(ray.z, 2)
        if idx == len(rays)-1:
          print

    if debug:
      plt.plot()
      for object_height, ray in zip(object_heights, rays):
        plt.plot(ray.x, ray.y, 'o', label=str('[' + str(object_height[0]) + 
                                              ', ' + str(object_height[1]) + 
                                              ']'))
      plt.legend(loc='upper right', numpoints=1)
      plt.show()

    return exit_angles

  def getEFL(self, wavelength):
    self.zcontroller.loadZemaxFile(self.file)
    self.zcontroller.setWavelengthNumberOf(1)
    self.zcontroller.setWavelengthValue(wavelength, 1)
    return self.zcontroller.getLensData().EFL

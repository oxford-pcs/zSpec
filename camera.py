import numpy as np
import pylab as plt
import pyzdde.zdde as pyz

from component import Component

class Camera(Component):
  def __init__(self, camera_zmx_file, zcontroller):
    self.file_pathname = camera_zmx_file
    self.zcontroller = zcontroller

  def doRayTraceForObjectAngles(self, object_angles, wavelength, reverse_fields_xy=False, verbose=True, debug=False):
    '''
      Trace the chief ray from each collimated field point through the camera 
      and work out the corresponding (x, y) positions at the image plane.
    '''
    
    if verbose:
      print "Tracing object angles through camera..."
      
    if reverse_fields_xy:
      object_angles = [(angle[1], angle[0]) for angle in object_angles]
         
    self.zcontroller.loadZemaxFile(self.file_pathname)
    self.zcontroller.setWavelengthNumberOf(1)
    self.zcontroller.setWavelengthValue(wavelength, 1)

    rays = self.zcontroller.doRayTraceForFields(object_angles, field_type=0, px=0, py=0)
    xys = []
    for idx, ray in enumerate(rays):
      xys.append((ray.x, ray.y))
      
      if debug:
        if idx == 0:
          print
          print "field\tx\ty\tz"
        print idx, '\t', round(ray.x, 2), '\t', round(ray.y, 2), '\t', \
          round(ray.z, 2)
        if idx == len(rays):
          print
         
    if debug:
      plt.plot()
      for object_angle, ray in zip(object_angles, rays):
        plt.plot(ray.x, ray.y, 'o', label=str('[' + str(object_angle[0]) + 
                                              ', ' + str(object_angle[1]) + 
                                              ']'))
      plt.legend(loc='upper right', numpoints=1)
      plt.show()    

    return xys
  

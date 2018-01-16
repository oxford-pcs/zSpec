import json

import numpy as np
import pylab as plt

class slit():
  def __init__(self, path, name):
    self.slit_pattern = self._getSlitPatternFromFile(path, name)
    
  def _getSlitPatternFromFile(self, path, name):
      '''
        Return slit with name [name] from a JSON file at path [path].
      '''
      with open(path) as fp:
        cfg = json.load(fp)
        
      slit = None
      for c in cfg:
        if c['name'] == name:
          slit = c
          break;
        else:
          continue
      try:
        assert slit is not None
      except AssertionError:
        print "slit config not found"
      
      return slit   
    
  def getFieldsFromSlitPattern(self, sampling, verbose=True, debug=False):
    '''
      Takes the slit pattern [slit_pattern] and a spatial sampling parameter 
      [sampling] (in lens units) and returns a list of field points at the 
      entrance slit.
    '''
    fields = []
    if self.slit_pattern['pattern'] == 'brick_wall':
      pattern_data = self.slit_pattern['pattern_data']
      slit_length = (pattern_data['n_slitlets'] * \
                     pattern_data['slitlet_length']) + \
                    ((pattern_data['n_slitlets'] - 1) * \
                     pattern_data['slitlet_separation'])
                  
      slitlet_x_regions = []    # list of tuples
      slitlet_ys = []
      for i in range(0, pattern_data['n_slitlets']):
        slitlet_x_regions.append((i*pattern_data['slitlet_length'] + \
                                  i*pattern_data['slitlet_separation'] - \
                                  slit_length/2., \
                                  (i+1)*pattern_data['slitlet_length'] + \
                                  i*pattern_data['slitlet_separation'] - \
                                  slit_length/2.))
        this_slitlet_y = pattern_data['stagger_length'] / 2.
        if i % 2 == 0:
          this_slitlet_y *= -1
        slitlet_ys.append(this_slitlet_y)

      # Now iterate through x at the sampling requested, checking if the 
      # current point lies within a slitlet. If so, add this point to the 
      # field list and continue.
      #
      for x in np.arange(-slit_length/2., slit_length/2.+sampling, sampling):
        in_region_idx = -1
        for region_idx, region in enumerate(slitlet_x_regions):
          if x >= region[0] and x <= region[1]:
            in_region_idx = region_idx
            break
        if in_region_idx == -1:
          continue
        else:
          fields.append((x, slitlet_ys[in_region_idx], in_region_idx))
                        
    if debug:
      plt.plot([xy[0] for xy in fields], [xy[1] for xy in fields], 'ko')
      plt.show()
      
    return fields

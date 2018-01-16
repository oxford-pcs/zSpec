class Component():
  def __init__(self, zmx_file, zcontroller):
    self.file_pathname = zmx_file
    self.zcontroller = zcontroller

  def getEFL(self, wavelength):
    if not self.zcontroller.isFileAlreadyLoaded(self.file_pathname):
      self.zcontroller.loadZemaxFile(self.file_pathname)
    self.zcontroller.setWavelengthNumberOf(1)
    self.zcontroller.setWavelengthValue(wavelength, 1)
    return self.zcontroller.getLensData().EFL

  def getWFE(self):
    if not self.zcontroller.isFileAlreadyLoaded(self.file_pathname):
      self.zcontroller.loadZemaxFile(self.file_pathname)
    self.zcontroller.getAnalysisWFE()

class DiffractionPattern(object):
    version = dict(major=0, minor=1, tiny=0)
    """docstring for DiffractionPattern"""
    def __init__(self, crystal, wavelength='Cu'):
        super(DiffractionPattern, self).__init__()
        self._crystal = crystal
        self._wavelength = wavelength
        self._pattern = {}
        self.calculate()
    
    @property
    def wavelength(self):
        """docstring for wavelength"""
        return self._wavelength
        
    def calculate(self):
        """docstring for calculate"""
        pass
        
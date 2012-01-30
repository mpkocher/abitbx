class DiffractionPattern(object):
    version = dict(major=0, minor=1, tiny=0)
    def __init__(self, crystal, wavelength='Cu'):
        # xray crystal structure
        self._crystal = crystal
        self._wavelength = wavelength
        self._pattern = {}
        self.calculate()
    
    @property
    def wavelength(self):
        """docstring for wavelength"""
        return self._wavelength
        
    def calculate(self, wavelength=None):
        # returns a dict of crystal structure
        pass
        
#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
ToDo:
    - Sort out this label business
    - Validate element name
    - Implement load_from_dict
    - Add xyz (since it's immutable?)
'''

class Site(object):

    """docstring for Site"""
    def __init__(self, name= None, label=None, abc=(0.0,0.0,0.0), occupancy=1.0, meta={} ):
        """
        Initialize a site object with the following fields. 
        
        string name             Site name - usually atom name. 
        string label            Site label - usually atomname-number. 
        float a,b,c             Lattice parameters
        """
        if name is None:
            self._name = label
        else:
            self._name = name

        self.label = label

        if label is None:
            self.label = name
        
        #make things immmutable
        self._a = abc[0]
        self._b = abc[1]
        self._c = abc[2]

        self._occupancy = occupancy

    @property
    def a(self):
        return self._a
    
    @property
    def b(self):
        return self._b
        
    @property
    def c(self):
        return self._c

    @property
    def name(self):
        return self._name
    
    @property
    def occupancy(self):
        return self._occupancy
    
    @staticmethod
    def load_from_dict(d):
        """not implemented"""
        raise NotImplementedError()
        
    @property
    def abc(self):
        """ Return a list of the lattice parameters. """
        return [self.a, self.b, self.c]

    def summary(self):
        """ Return a string summary of the site. """
        outs = []
        outs.append("name: %s abc: [%0.6f, %0.6f, %0.6f] occ: %0.2f" % (self.name, self.a, self.b, self.c, self.occupancy))
        return outs

    def print_summary(self):
        """ Print a string summary of the site. """
        print "\n".join(self.summary())

    def to_dict(self):
        """ Generate return a dictionary of the site. """
        return self.to_db()

    def to_db(self):
        # consistent with xdict schema
        d = dict(abc=self.abc, name = self.name, occupancy = self.occupancy)
        return d


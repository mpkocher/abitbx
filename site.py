#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
ToDo:
    - Sort out this label business
    - Validate element name
    - Implement load_from_dict
    - Add xyz (since it's immutable?)
'''
import periodictable

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

        #FIXME
        # is label/name coherent and valid

        #make things immmutable
        self._a = Site._in_unit_cellizer(abc[0])
        self._b = Site._in_unit_cellizer(abc[1])
        self._c = Site._in_unit_cellizer(abc[2])

        self._occupancy = occupancy

        # Sanity Checks
        assert((self.name in [e.symbol for e in periodictable.elements]) == True)
        assert(all([isinstance(i, (float, int)) for i in abc]) == True)
        assert((self._occupancy <= 1.0) == True)

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
    def abc(self):
        """ Return a list of the lattice parameters. """
        return [self.a, self.b, self.c]

    @property
    def name(self):
        #this should be taken out and replaced by 'label'
        # 'label' is of the form 'Fe' or 'Fe-1'
        # and symbol is the 'Fe'
        return self._name
    
    @property
    def symbol(self):
        return self._name

    @property
    def occupancy(self):
        return self._occupancy
    
    @staticmethod
    def load_from_dict(d):
        """not implemented"""
        raise NotImplementedError()
        
    def summary(self):
        """ Return a string summary of the site. """
        outs = []
        outs.append("name: %s abc: [%0.6f, %0.6f, %0.6f] occ: %0.2f" % (self.name, self.a, self.b, self.c, self.occupancy))
        return outs

    def print_summary(self):
        print "\n".join(self.summary())

    @staticmethod
    def _in_unit_cellizer(n):
        if n >= 1.0:
            return Site._in_unit_cellizer(n - 1)
        elif n < 0.0:
            return Site._in_unit_cellizer(n + 1)
        else:
            return n

    def to_dict(self):
        """ Generate return a dictionary of the site. """
        return self.to_db()

    def to_db(self):
        # consistent with xdict schema
        d = dict(abc=self.abc, name = self.name, occupancy = self.occupancy)
        return d


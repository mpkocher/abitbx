#!/usr/bin/python
# -*- coding: utf-8 -*-
from cctbx import uctbx

class Lattice(object):

    """docstring for Lattice"""

    def __init__(self, a,b,c,alpha,beta,gamma):
        """
        Lattice object with the following parameters.
        
        float a,b,c                     Lattice vectors. 
        float alpha, beta, gamma        Lattice angles. 
        """
        self.a = float(a)
        self.b = float(b)
        self.c = float(c)
        self.alpha = float(alpha)
        self.beta = float(beta)
        self.gamma = float(gamma)

    @property
    def abc(self):
        """ Return a list of the lattice vectors. """
        return [self.a, self.b, self.c]

    @property
    def angles(self):
        """ Return a list of the lattice angles. """
        return [self.alpha, self.beta, self.gamma]

    def to_dict(self):
        """ Return a dictionary representation of the lattice. """ 
        return self.to_db()

    def to_db(self):
        """ Return a dictionary representation of the lattice. """ 

        return {
            'a': self.a,
            'b': self.b,
            'c': self.c,
            'alpha': self.alpha,
            'beta': self.beta,
            'gamma': self.gamma,
            'volume': self.volume
            }

    def __str__(self):
        """ 
        String rep of lattice. 
        Users should not need to call. 
        """
        # this for unit_cell
        n = [
            self.a,
            self.b,
            self.c,
            self.alpha,
            self.beta,
            self.gamma,
            ]
        s = [str(i) for i in n]
        return ' '.join(s)

    @property
    def unit_cell(self):
        """ Return the cctbx representation of the unit cell. """
        cell = uctbx.unit_cell(str(self))
        return cell

    def fractionalize(self, xyz):
        """ Convert cartesian representation of coordinates to fractional for this lattice. """ 
        return self.unit_cell.fractionalize(xyz)

    def orthogonalize(self, abc):
        """ Convert fractional representation of coordinates to cartesian for this lattice. """
        return self.unit_cell.orthogonalize(abc)

    def distance(self, abc1, abc2):
        """ 
        Get distance between two points. 
        Warning: this doesn't account for periodicity.
        use Crystal.get_distance_periodic instead. 
        """
        return self.unit_cell.distance(abc1, abc2)

    @property
    def volume(self):
        """ Return volume of unit cell. """
        cell = uctbx.unit_cell(str(self))
        return cell.volume()

    def summary(self):
        """ Return summary of unit cell. """
        outs = []
        outs.append(str(self))
        return outs

    def print_summary(self):
        """ Return summary of unit cell. """
        print "\n".join(self.summary())

#!/usr/bin/python
# -*- coding: utf-8 -*-
#import sys
#import os
import json
import re

#import warnings
#import copy
#import math
#import random

from cctbx import sgtbx, uctbx, crystal, xray
from cctbx.eltbx import wavelengths
from cctbx.array_family import flex

# this isn't used
#from cctbx import symmetry_search

# Where is the pulling from?
#from periodictable import elements

from abitbx.space_group import SpaceGroup
from abitbx.site import Site
from abitbx.lattice import Lattice

class Crystal(object):
    
    """
    Crystal object.
    Functions as a wrapper to a cctbx xray.structure object,
    but adds additional variables and functionality.
    Core object of this package.
    """
    
    def __init__(self, space_group = SpaceGroup('P 1'), lattice = Lattice(1.0, 1.0, 1.0, 90.0, 90.0, 90.0), sites=[]):
        """
        Crystal object.
        Functions as a wrapper to a cctbx xray.structure object,
        but adds additional variables and functionality.
        Core object of this package.
        
        Input:
            SpaceGroup  space_group                            space group for the current crystal
            List of Site objects  sites                        List of Site objects.
        
        Warning:
            'crystal_structure' must be given,
            or 'space_group', 'lattice', and 'sites' must be given,
            or creation of the crystal will fail.
        """
        
        try:
            crystal_symmetry = crystal.symmetry(unit_cell=str(lattice), space_group_symbol=space_group.cctbx_name)
        except Exception as e:
            raise SymmetryError("SpaceGroup {s} is incompatible with Lattice -> {l} cctbx error {e}".format(l=str(lattice), s=SpaceGroup.cctbx_name, e=e))

        scatterers = flex.xray_scatterer()
        for i, site in enumerate(sites):
            # the element name can be pulled from scatterer via the s.element_symbol() method (if it's an element!!!)
            # example: 'atom-b-12',or 'vacancy-c-3'
            # we need to set the scattering_type so we can freely use the label to store metadata
            
            #scattering_type = something
            #scatterers.append(xray.scatterer(label=atom.name, site=tuple(atom.abc), occupancy=atom.occupancy), scattering_type=atom.name)
            
            #Method #2
            # explicitly add metadata to _meta
            st_temp, dash, num = site.label.partition("-")
            if dash == "-":
                k = site.label
            else:
                k = "-".join([site.label, str(i)])
            
            # problems here not sure what's up
            k = str(k)
            # print "label = ", k, ' type of label = ', type(k)
            # print "site = ", tuple(site.abc)
            # print "occupancy = ", site.occupancy
            scatterers.append(xray.scatterer(label=k, site=tuple(site.abc), occupancy=site.occupancy))
        
        # Test for coherency of Lattice and SpaceGroup
        self.crystal_structure = xray.structure(crystal_symmetry=crystal_symmetry, scatterers=scatterers)

    @staticmethod
    def from_crystal_structure(crystal_structure):
        c = Crystal(space_group=SpaceGroup('P1'))
        c.crystal_structure = crystal_structure
        return c
    
    @staticmethod
    def from_cif(file_name):
        """ Create a crystal object from a cif file. """
        # why doesn't this work?
        # http://cctbx.sourceforge.net/current/python/cctbx.xray.structure.html
        with open(file_name,'r') as f:
            # only return the first one, 
            # mulitple cifs are not supported
            dict_cifs = xray.structure.from_cif(f)

        crystal_structure = dict_cifs[dict_cifs.keys()[0]]
        c = Crystal.from_crystal_structure(crystal_structure)
        return c
    
    
    @staticmethod
    def load_from_xdict(args):
        """
        Create a crystal object from a dictionary.
        
        The input dictionary must have all used fields or key errors will result.
        """
        #print args
        sites = [Site(label=a['name'], abc=a['abc'], occupancy=a['occupancy'] )  for a in args['sites']]
        # Lattice and SpaceGroup could be initialized from dict or Lattice/SpaceGroup objects
        # right not crystal is initialized by dict
        lattice = Lattice(args['lattice']['a'],args['lattice']['b'],args['lattice']['c'],args['lattice']['alpha'],args['lattice']['beta'],args['lattice']['gamma'])
        # self.cctbx_name = args["space_group"]["cctbx_name"]
        # name should be of the type : "P m m n :2"
        cctbx_name = args['space_group']['cctbx_name']
        space_group = SpaceGroup(cctbx_name)
        # necessary data from db
        transforms = args.get('transforms',[])
        crystal = Crystal(sites=sites, lattice=lattice, space_group=space_group, transforms=transforms)
        return crystal
    
    
    @staticmethod
    def from_json(file_name):
        """ Create a crystal object from a json file. """
        
        f = open(file_name, "r")
        dict_rep = json.load(f)
        f.close()
        
        return Crystal.load_from_json_dict(dict_rep)
    
    
    
    @property
    def space_group(self):
        """ Return the space group of the crystal. """
        sgt = self.crystal_structure.space_group().type()
        symbol =  sgt.lookup_symbol()
        name = ''
        if re.search(r'\(', symbol):
            name = symbol.split("(")[0].rstrip()
        else:
            name = symbol
        return SpaceGroup(name)

    
    @property
    def sites(self):
        """
        Return a list of COPIES of the sites in the crystal.
        
        Warning:
            This function returns a copy. Do not modify the returned list and expect to modify the crystal itself.
        """
        _sites = []
        for i, s in enumerate(self.crystal_structure.scatterers()):
            name = s.label.split("-")[0]
            _sites.append(Site(label=s.label, name=name, abc=s.site, occupancy=s.occupancy))
        return _sites
    
    #site maninpulation methods
    def add_site(self, s):
        """ Adds the specified site object to the crystal_structure. """
        # translate Site().to_scatterer()
        self.crystal_structure.add_scatterer( s.to_scatterer())
    
    def add_sites(self, new_sites):
        for s in new_sites:
            self.add_site(s)
    
    def remove_site_at(self,abc):
        raise NotImplementedError("Crystal#remove_site_at")
        
    def remove_site_at_index(self,i):
        raise NotImplementedError("Crystal#remove_site_at_index")
    pass
    
    
    # verbose java-y way to make it clear that it's Immutable
    def get_lattice(self):
        """ Return the a copy of the crystal lattice as a Lattice object. """
        p = self.crystal_structure.unit_cell().parameters()
        return Lattice(p[0], p[1], p[2], p[3], p[4], p[5])
    
    @property
    def volume(self):
        return self.crystal_structure.unit_cell().volume()
    
    @property
    def density(self):
        # units are in grams per cubic centimeter
        return self.crystal_structure.crystal_density()
    
    
    def to_niggli(self):
        """docstring for to_niggli"""
        niggli_structure = self.crystal_structure.niggli_cell()
        c = Crystal.from_crystal_structure(niggli_structure)
        return c
    
    def to_standard(self):
        """docstring for t_standard"""
        cb_op =  self.crystal_structure.change_of_basis_op_to_reference_setting()
        standard_structure = self.crystal_structure.change_basis(cb_op=cb_op)
        return Crystal.from_crystal_structure(standard_structure)

    
    def to_p1(self):
        p1_structure = self.crystal_structure.expand_to_p1()
        return Crystal.from_crystal_structure(p1_structure)
    
    def to_dict(self):
        """ Return a dictionary representation of the current crystal. """
        #print [s.to_dict() for s in self.sites]
        return {
                'sites': [i.to_dict() for i in self.sites],
                'lattice': self.get_lattice().to_dict(),
                'space_group': self.space_group.to_dict(),
                }
    
    
    def chemical_formula(self):
        """ Return the chemical formula for the current crystal"""
        # this is probably buggy
        chemical_formula = self.crystal_structure.niggli_cell().unit_cell_content()
        return chemical_formula
    
    def print_summary(self):
        #FIXME
        return "Summary"

    def get_coordination_number(self, scatterer):
        #FIXME
        return 4.0

    def assign_wyckoff(self, abc, tol=0.1):
        #FIXME This needs improvement and to be tested
        cctbx_name = self.space_group.cctbx_name
        sg_symbol = sgtbx.space_group_symbols(cctbx_name)
        sg = sgtbx.space_group(sg_symbol)
        unit_cell = uctbx.unit_cell(str(self.get_lattice()))
        symmetry = crystal.symmetry(unit_cell=unit_cell, space_group=sg)
        special_position_settings = crystal.special_position_settings(symmetry,min_distance_sym_equiv=0.5)
        site_symmetry = special_position_settings.site_symmetry(abc)
        wyckoff_table = special_position_settings.space_group_info().wyckoff_table()
        wyckoff_mapping = wyckoff_table.mapping(site_symmetry)
        letter = wyckoff_mapping.position().letter()
        return letter


class SymmetryError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "Symmetry Error -> " + self.msg

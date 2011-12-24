#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import json
from cctbx import sgtbx

def _load_icsd_to_cctbx():
    _name = 'icsd_name_to_cctbx_name.json'
    file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), _name)
    with open(file_name, 'r') as f:
        d = json.loads(f.read())
    return d


class SpaceGroup(object):

    # this is really stupid to do
    ICSD_TO_CCTBX = _load_icsd_to_cctbx()

    def __init__(self, name):

        # wtf is name
        self.space_group_info = sgtbx.space_group_info(symbol=str(name))
        #self.space_group_info = sgtbx.space_group_info(symbol=str(name))
        #self.name = str(self.space_group_info)
        #self.space_group = sgtbx.space_group_symbols(self.name)

        # should add centering as a method

    @staticmethod
    def is_valid(name):
        """docstring for is_valid"""
        #this isn't available to python
        # http://cctbx.sourceforge.net/current/c_plus_plus/classcctbx_1_1sgtbx_1_1space__group__symbols.html#_details
        #s = sgtbx.space_group_symbols(name)
        #return s.is_valid(name)
        s = SpaceGroup(name)
        if s.number() != 0:
            return True
        else:
            return False

    
    @staticmethod
    def from_icsd_name(icsd_name):
        if icsd_name in SpaceGroup.ICSD_TO_CCTBX:
            return SpaceGroup.ICSD_TO_CCTBX[icsd_name]
        else:
            return None

    @property
    def icsd_name(self):
        #FIXME This is a bit flakey and slow as mudz
        r = None
        for k,v in SpaceGroup.ICSD_TO_CCTBX.items():
            if v.encode('utf8') == self.cctbx_name:
                r = k
        if r is None:
            return None
        else:
            return r[0]

    @property
    def cctbx_name(self):
        """docstring for cctbx_name"""
        #this is the cctbx look up name
        # sometimes the symbol is of the form
        # 'F d -3 m :1'
        # but it can also be
        # 'F d -3 m :2 (-x+y+z+1/8,x-y+z+1/8,x+y-z+1/8)'
        # for primitive cells
        t = self.space_group_info.type()
        symbol =  t.lookup_symbol()
        name = ''
        if re.search(r'\(', symbol):
            name = symbol.split("(")[0].rstrip()
        else:
            name = symbol
        return name
            
    @property
    def raw_cctbx_name(self):
        """docstring for raw_cctbx_name"""
        t = self.space_group_info.type()
        symbol =  t.lookup_symbol()
        return symbol

    def is_reference_setting(self):
        """docstring for is_reference_setting()"""
        return self.space_group_info.is_reference_setting()
    
    @property
    def number(self):
        """docstring for number"""
        return self.space_group_info.type().number()
    
    @property
    def hall(self):
        """docstring for hall"""

        return self.space_group_info.type().hall_symbol()

    @property
    def hm(self):
        """docstring for hm"""

        return self.space_group_info.type().universal_hermann_mauguin_symbol()

    @property
    def hermann_mauguin(self):
        """docstring for hermann_mauguin"""
        return self.hm
    
    @property
    def crystal_system(self):
        """docstring for crystal_system"""

        return self.space_group_info.group().crystal_system()
    
    @property
    def schoenflies(self):
        """docstring for schoenflies"""
        sy =  sgtbx.space_group_symbols(self.cctbx_name)
        return sy.schoenflies()
    
    @property
    def point_group(self):
        """docstring for point_group"""
        return self.space_group_info.group().point_group_type()
    
    @property
    def centering(self):
        """docstring for centering"""
        #this is the CONVENTIONAL !!!!!
        return self.space_group_info.group().conventional_centring_type_symbol()

    @property
    def laue(self):
        """docstring for laue"""
        return self.space_group_info.group().laue_group_type()
        
    def is_standard(self):
        """docstring for is_standard"""
        return self.is_reference_setting()

    def to_dict(self):
        """docstring for to_dict"""
        d =  {"cctbx_name":self.cctbx_name, 'hall':self.hall, 'centering':self.centering, 
        'hermann_mauguin':self.hermann_mauguin, 'point_group':self.point_group, 'schoenflies':self.schoenflies, 
        'crystal_system': self.crystal_system, 'number':self.number, 'laue':self.laue, 'is_standard':self.is_standard()}
        return d
    
    def to_db(self):
        """docstring for to_db"""
        return self.to_dict()
        
    def summary(self):
        """docstring for summary"""
        outs = []
        outs.append('Space Group')
        outs.append('      cctbx name : %s' % self.cctbx_name)
        outs.append(' hermann_mauguin : %s' % self.hermann_mauguin)
        outs.append('          number : %d' % self.number)
        outs.append('            hall : %s' % self.hall)
        outs.append('  crystal system : %s' % self.crystal_system)
        outs.append('       centering : %s' % self.centering)
        outs.append('        standard : %s' % self.is_standard())
        outs.append('     schoenflies : %s' % self.schoenflies)
        outs.append('     point group : %s' % self.point_group)
        outs.append('')
        return outs


class SpaceGroupSymbolError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "SpaceGroup Error -> Unable to interpet " + self.msg

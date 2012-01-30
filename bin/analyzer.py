#!/usr/bin/env python
import os
import sys
import json
from pprint import pprint as pp
from optparse import OptionParser
import abitbx.utils as utils 

def space_group_summary(crystal_structure):
    sg, was_successful = utils.find_symmetry_from_crystal_structure(crystal_structure)
    pp((sg, was_successful))
    
def xrd_summary(crystal_structure, wavelength='Cu', output_file=None):
    d = utils.to_diffraction_pattern(crystal_structure)
    pp(d)
    if output_file is not None:
        with open(output_file, 'w') as f:
            f.write(json.dump(d))

def _file_name_to_crystal_structure(file_name):
    c = None
    if os.path.exists(os.path.abspath(file_name)):
        if file_name.endswith(".json"):
            with open(os.path.abspath(file_name), 'r') as f:
                d = json.loads(f.read())
                c = utils.mg_structure_dict_to_cctbx_crystal_structure(d)
        elif file_name.endswith(".cif"):
            c = cctbx_crystal_structure_from_cif(file_name)
        else:
            print "Unable to determine format. cif and .json (MaterialsProject Structure.to_dict() format)"
    else:
        print "Unable to find file_name '{f}'".format(f=file_name)
    return c


def main(file_name, analyze_space_group=False, analyze_xrd=False, output_file=None):
    c = _file_name_to_crystal_structure(file_name)
    if c is not None:
        if analyze_space_group:
            space_group_summary(c)
        if analyze_xrd:
            xrd_summary(c, output_file)
    return 0
    
if __name__ == '__main__':
    # usage
    # cctbx file_name.cif
    # cctbx file_name.cif --space_group 
    # cctbx file_name.json --space_group
    # cctbx file_name.cif --xrd
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="file_name", help="File to analyze (e.g, LiCoO2.json LiCoO2.cif)")
    parser.add_option("-s", "--space_group", dest='analyze_space_group', action="store_true", default=False, help='Print the SpaceGroup')
    parser.add_option("-x", "--xrd", dest='analyze_xrd', action="store_true", default=False, help='Calculate XRD pattern')
    parser.add_option("-o", "--out", dest='output_file', default=None, help="output file to write to")
    (options, args) = parser.parse_args()
    print options
    sys.exit(main(options.file_name, options.analyze_space_group, options.analyze_xrd, options.output_file))
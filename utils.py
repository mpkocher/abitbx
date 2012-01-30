import re

from cctbx import uctbx, crystal, xray
from cctbx import symmetry_search
from cctbx.array_family import flex 
from cctbx.eltbx import wavelengths

def _sanatize(s):
    # Some settings have 'C m c m (x-y, x+y, y+z)' format
    rx = re.compile('\(')
    if rx.search(s) is not None:
        return s.split('(')[0]
    else:
        return s

def _space_group_info_to_dict(space_group_info):
    '''
    Make compatible with MG db format
    '''
    space_group_type = space_group_info.type()
    hall = space_group_type.hall_symbol()
    hermann_mauguin = space_group_type.universal_hermann_mauguin_symbol()
    number = space_group_type.number()
    symbol = space_group_type.lookup_symbol()
    crystal_system = space_group_type.group().crystal_system() 
    #return dict(hall=hall, hermann_mauguin=hermann_mauguin, number=number, crystal_system=crystal_system, cctbx_name = symbol)
    return dict(hall=_sanatize(hall), hermann_mauguin=_sanatize(hermann_mauguin), number=number, crystal_system=crystal_system, cctbx_name = _sanatize(symbol))

def find_symmetry_from_crystal_structure(crystal_structure):
    work_f_calc = crystal_structure.structure_factors(d_min=1).f_calc().expand_to_p1()
    sg_dict = {}
    state = False
    try:
        sf_symm = symmetry_search.structure_factor_symmetry(f_in_p1=work_f_calc)
        sgi = sf_symm.space_group_info
        sg_dict = _space_group_info_to_dict(sgi)
        state = True
    except Exception as e:
        sg_dict = dict(hall='P 1', hermann_mauguin='P 1', number=1, crystal_system='Triclinic', cctbx_name='P 1')
    #return both the space group and a flag to specify that the assignment was successful
    return (sg_dict, state)

def find_symmetry(dict_or_xtl):
    """
    Args: dict_or_xtl (can be a MaterialsProject Structure.to_dict or a cctbx xray crystal structure object
   
    Returns: tuple (dict, bool) Dictionary of space group, was determination of the space group successful (i.e, did the algo throw an exception)
    """
    if isinstance(dict_or_xtl, dict):
        c = mg_structure_dict_to_cctbx_crystal_structure(dict_or_xtl)
    else:
        #isinstance(dict_or_xtl, xray.crystal)
        c = dict_or_xtl
    return find_symmetry_from_crystal_structure(c)

def cctbx_crystal_structure_to_mg_structure_dict(xtl):
    """
    Args: xtl (cctbx xray.crystal_structure)

    Returns: dict consistent with the MaterialsProject Structure.to_dict format
    """
    d = {}
    return d
    
def cctbx_crystal_structure_from_cif(file_name, name=None):
    """
    Args:
        name is keyname in cif. By default the first crystal is used.
    """
    with open(file_name,'r') as f:
        # only return the first one, 
        # mulitple cifs are not supported
        cs = xray.structure.from_cif(f)
        crystal = cs[cs.keys()[0]]
        #crystal.show_summary()
        #crystal.show_scatterers()
    return crystal
    
def mg_structure_dict_to_cctbx_crystal_structure(d):
    """ 
    Compatible with pymatgen Structure.to_dict() format
    to a cctbx crystal structure object
    """
    params = " ".join([str(o) for o in [d['lattice']['a'], d['lattice']['b'], d['lattice']['c'], d['lattice']['alpha'], d['lattice']['beta'], d['lattice']['gamma']]])
    unit_cell = uctbx.unit_cell(params)
    symbol = 'P 1'
    crystal_symmetry = crystal.symmetry(unit_cell=unit_cell, space_group_symbol=symbol)
    """
    site = tuple([0.0, 0.20, 0.3])
    scatterers.append(xray.scatterer(label=lable, site=site, occupancy=occupancy)

    crystal_structure = xray.structure(crystal_symmetry=crystal_symmetry, scatterers=scatterers)
    """
    scatterers = flex.xray_scatterer()
    for site in d['sites']:
        abc = tuple(site['abc'])
        for specie in site['species']:
            label = specie['element'].encode('utf8')
            occupancy = float(specie['occu'])
            scatterers.append(xray.scatterer(label=label, site=abc, occupancy=occupancy))
    crystal_structure = xray.structure(crystal_symmetry=crystal_symmetry, scatterers=scatterers)
    return crystal_structure

def to_diffraction_pattern(crystal_structure, wavelength='Cu'):
    """
    Args:
        wavelength = (Cr, Fe, Cu, Mo, Ag)

    Return structure:
        {'wavelength':wavelength, 'meta':['d_spacing', 'two_theta', 'amplitude', 'hkl'], 'data':[]}

    Wavelengths from cctbx/eltbx/wavelengths.cpp
    // BEGIN_COMPILED_IN_REFERENCE_DATA
          {"CrA1", 2.28970}, {"CrA2", 2.29361}, {"Cr", 2.2909},
          {"FeA1", 1.93604}, {"FeA2", 1.93998}, {"Fe", 1.9373},
          {"CuA1", 1.54056}, {"CuA2", 1.54439}, {"Cu", 1.5418},
          {"MoA1", 0.70930}, {"MoA2", 0.71359}, {"Mo", 0.7107},
          {"AgA1", 0.55941}, {"AgA2", 0.56380}, {"Ag", 0.5608},
          {"", 0}
    // END_COMPILED_IN_REFERENCE_DATA
    """

    #d_min = 3
    # f_calc is the intensity?
    # Need to sanatize the Site labels !!

    miller_indices = crystal_structure.build_miller_set(anomalous_flag=False, d_min=1, d_max=20)
    wavelength_in_ang = wavelengths.characteristic(wavelength).as_angstrom()
    unit_cell = crystal_structure.unit_cell()
    pattern = []
    f_calc = crystal_structure.structure_factors(d_min=1, algorithm="direct").f_calc()
    for hkl, j in zip(f_calc.indices(), f_calc.data()):
        two_theta = unit_cell.two_theta(hkl, wavelength_in_ang, deg=True)
        d = unit_cell.d(hkl)
        #print hkl, d, abs(j), two_theta
        #xrds.append({"hkl":list(hkl), "amplitude":abs(j), "d-spacing":d, "two_theta":two_theta})
        pattern.append([abs(j), list(hkl), two_theta, d])

    #return xrds

    '''
    f_calc = crystal_structure.structure_factors(d_min=d_min).f_calc()
    millers = crystal_structure.structure_factors(d_min=d_min).miller_set()
    miller_indices =  millers.indices()
    wavelength = wavelengths.characteristic('CU').as_angstrom()
    two_thetas = crystal_structure.unit_cell().two_theta(millers.indices(), wavelength, deg=True)
    d_spacings = f_calc.d_spacings()
    unit_cell = c.crystal_structure.unit_cell()
    '''
    d = {'wavelength':{'element':wavelength, 'in_angstroms': wavelength_in_ang}, 'meta':['amplitude', 'hkl', 'two_theta', 'd_spacing'], 'pattern':pattern}
    return d






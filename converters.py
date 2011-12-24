from abitbx.crystal import Crystal
from abitbx.lattice import Lattice
from abitbx.space_group import SpaceGroup

# Convert MP Schema doc 1.0 to crystal structure object
def crystal_doc_to_crystal(doc):
    pass

def task_doc_to_crystal(doc):
    '''
    Output of task doc to crystal object
    '''
    pass


# Coherent with the Schema MP 1.0
def _space_group_to_doc(space_group):
    """
    space_group is a abitbx.space_group.SpaceGroup 
    """
    doc = {}
    doc['cctbx_name'] = space_group.cctbx_name
    doc['crystal_system'] = space_group.crystal_system
    doc['icsd_name'] = space_group.icsd_name
    doc['number'] = space_group.number
    doc['hall'] = space_group.hall
    doc['hermann_mauguin'] = space_group.hm
    doc['laue'] = space_group.laue
    doc['is_standard'] = space_group.is_standard()
    doc['centering'] = space_group.centering
    doc['point_group'] = space_group.point_group
    doc['schoenflies'] = space_group.schoenflies
    return doc

def _site_to_doc(site):
    """
    site is abitbx.site.Site
    """
    doc = {}
    doc['label'] = site.label
    doc['symbol'] = site.name
    doc['abc'] = site.abc
    return doc

def _lattice_to_doc(lattice):
    doc = {}
    doc['a'] = lattice.a
    doc['b'] = lattice.b
    doc['c'] = lattice.c
    doc['alpha'] = lattice.alpha
    doc['beta'] = lattice.beta
    doc['gamma'] = lattice.gamma
    doc['volume'] = lattice.volume
    return doc

def crystal_to_doc(crystal):
    """
    crystal is abitbx.crystal.Crystal instance
    """
    doc = {}
    doc['space_group'] = _space_group_to_doc(crystal.space_group)
    doc['sites'] =[_site_to_doc(s) for s in crystal.sites] 
    doc['lattice'] = _lattice_to_doc(crystal.get_lattice())
    doc['density'] = crystal.density
    doc['elements'] = list(set([s['symbol'] for s in doc['sites']]))
    doc['nelements'] = len(doc['elements'])
    return doc

__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2018-2021, Vanessa Sochat"
__license__ = "MPL 2.0"

from schemaorg.utils import ( get_installdir, read_csv )
from schemaorg.logger import bot
import os


################################################################################
# Software Versions
################################################################################

def get_versions():
    '''list versions available, based on subfolders in a subfolder under the
       database. We default to listing those under "release."
    '''
    base = get_database()
    versions = os.listdir(os.path.join(base, "releases"))
    versions = [float(x) for x in versions]
    versions.sort()
    return [str(x) for x in versions]

def get_schemaorg_version():
    '''determine the schemaorg version to use based on an environmental variable
       first followed by  using the latest.
    '''
    from schemaorg.defaults import SCHEMAORG_VERSION as version

    if version is None:
        version = get_versions()[-1]

    bot.debug("schemaorg version %s selected" % version)
    return version


def get_release(version = None):
    '''get a subfolder for a particular release, defaults to latest
    '''
    base = get_database()
    if version is None:
        version = get_schemaorg_version()
    return os.path.join(base, "releases", version)


def get_database():
    '''get the data folder with "release" and "ext" subfolders
    '''
    return os.path.join(get_installdir(), "schemaorg", "data")


# courtesy functions for schema.org exports

''' List of available csv --------------------------------------
all-layers-properties.csv  ext-health-lifesci-properties.csv
all-layers-types.csv       ext-health-lifesci-types.csv
ext-attic-properties.csv   ext-meta-properties.csv
ext-attic-types.csv        ext-meta-types.csv
ext-auto-properties.csv    ext-pending-properties.csv
ext-auto-types.csv         ext-pending-types.csv
ext-bib-properties.csv     schemaorg-all-https-properties.csv
ext-bib-types.csv          schemaorg-all-http-types.csv
'''

def read_properties_csv(keyfield='id', version=None):
    '''read in the properties csv (with all types), defaulting to using
       the "id" as the lookup key. We do this because the properties listed
       in the types csv include the full uri.
  
       Parameters
       ==========
       keyfield: the key to use to generate the lookup, a header in the csv
       version: release version under data/releases to use, defaults to latest
    '''
    release_dir = get_release(version=version)
    filename = os.path.join(release_dir, 'schemaorg-all-https-properties.csv')
    return read_csv(filename, keyfield=keyfield)


def read_types_csv(keyfield='label', version=None):
    '''read in the types csv, with default lookup key as "label" since the
       likely use case will be the user searching for an item of interest.

       Parameters
       ==========
       keyfield: the key to use to generate the lookup, a header in the csv
       version: release version under data/releases to use, defaults to latest
    '''
    release_dir = get_release(version = version)
    filename = os.path.join(release_dir, 'schemaorg-all-https-types.csv')
    return read_csv(filename, keyfield=keyfield)


def find_similar_types(term, version=None):
    '''find similar types, with intent to show to the user in case 
       capitalization was off.

       Parameters
       ==========
       term: a term to search for, in entirety. Casing doesn't matter
       version: release version under data/releases to use, defaults to latest
    '''
    print(term)
    typs = read_types_csv(version=version)

    # In case the user provided a url, remove it
    term = term.split('/')[-1].lower()

    # Look for entire term
    return [x for x in typs if term in x.lower()]

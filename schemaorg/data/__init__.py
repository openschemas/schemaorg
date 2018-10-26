'''

Copyright (C) 2018 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

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
    versions.sort()
    return versions

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
ext-bib-properties.csv     schema-properties.csv
ext-bib-types.csv          schema-types.csv
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
    filename = os.path.join(release_dir, 'schema-properties.csv')
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
    filename = os.path.join(release_dir, 'schema-types.csv')
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

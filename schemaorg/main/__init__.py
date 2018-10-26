'''

A class to represent a specification schema

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
from schemaorg.data import (
    find_similar_types, 
    read_types_csv, 
    read_properties_csv, 
    get_versions
)
from schemaorg.logger import bot
import os
import re
import sys

class Schema(object):

    def __init__(self, schema_type, version=None, base=None):
 
        # Does the user want a custom base?
        self.type = None
        self._set_base(base)
        self._set_version(version)
        self.load_type(schema_type)

    def __str__(self):
        return self.type

    def __repr__(self):
        return self.__str__()


# Validate

    def _set_base(self, base):
        '''set the base variable for the object, only if it has been defined

           Parameters
           ==========
           base: the base (http/https) to set.
        '''
        # Default to schema.org
        if base is None:
            base = "http://www.schema.org"

        # Must be a url, starting with http or https
        if not re.search("^http", base):
            bot.exit('%s must be a valid URL starting with http or https.')
     
        bot.info("Specification base set to %s" % base)
        self.base = base
 
    def _set_version(self, version):
        '''ensure the version folder exists, or is installed with the
           application, and set to be used for the schema. This should only
           be called upon init when the data (with corresponding version)
           are then loaded.
 
           Parameters
           ==========
           a version string or float.
        ''' 
        # Available versions, sorted to latest
        available = get_versions()

        # If version is None, just use latest
        if version is None:
            version = available[-1]

        version = str(version)

        # Version not valid, default to use latest
        if not version in available:
            bot.warning('Version %s is not found in the data folder.' % version)
            version = available[-1]

        bot.info('Using Version %s' % version)
        self.version = version

# Load

    def load_type(self, schema_type):
        '''load a type. Expected to be called upon init, but also allowed
           to be called once already loaded. The type and properties must be
           loaded together to ensure being in sync.
 
           Parameters
           ==========
           schema_type: the type to load
        '''

        # Load type, followed by type attributes and properties
        self._load_type(schema_type) 
        self._load_attributes()
        self._load_props()

    def _load_props(self):
        '''load properties based on the type defined for the object. Can
           (or should) only be called wit load_type, so the two are in sync
        '''
        lookup = read_properties_csv(version = self.version)

        # Keep them in a dictionary for now
        self.properties = dict()

        # Need to parse, split by comma and strip empty spaces
        props = self.type_spec['properties'].split(',')
        props = [p.strip() for p in props]

        for prop in props:
            if prop in lookup:
                self.properties[prop] = lookup[prop]

        bot.info('Loaded %s properties for %s' %(len(properties), self.type))

    def _load_type(self, schema_type):
        '''load the tyepe file, depending on the set version. This means:
           1. Setting the url to be the base (schema.org) followed by type
           2. Loading the types csv based on the version defined for the object
           3. Verifying that the type exists in the data
              - if not, show alternatives and exit
           4. Loading the type spec into self.type_spec
        '''
        typs = read_types_csv(version = self.version)

        # Type must be in keys
        if schema_type in typs:

            # It's good! Save to object
            self.type = schema_type

            # Assemble the type url
            self.url = "%s/%s" % (self.base, self.type)

        # Print similar based on name, then exit
        else:
            bot.error('%s is not a valid type!' % schema_type)
            self.print_similar_types(schema_type)
            sys.exit(1)

        bot.info('Found %s' % self.url)
 
        # Load the type, or save to the object
        self.type_spec = typs[self.type]

    def _load_attributes(self):
        ''' add the attributes from the loaded type_spec to the class.
        '''
        # Add as attributes to the object
        for attr in list(self.type_spec.keys()):
            if attr not in ['properties']:
                setattr(self, attr, self.type_spec[attr])

    def _load_props(self):
        '''load the properties csv file, depending on the set version.
        '''
        props = read_properties_csv(version = self.version)


# Print

    def print_similar_types(self, schema_type = None):
        '''A courtesy function to print similar types based on name,
           if they are found.
        '''    
        # Find similar types by name
        contenders = find_similar_types(schema_type or self.type)

        # If we find contenders, show the user
        if len(contenders) > 0:
            bot.info('Did you mean:')
            print('\n'.join(contenders))

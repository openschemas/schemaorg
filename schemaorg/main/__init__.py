'''

A class to represent a specification schema

Copyright (C) 2018-2019 Vanessa Sochat.

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

from schemaorg.utils import ( 
    get_installdir, 
    print_json,
    read_csv,
    read_file,
    read_yaml,
    _read_yaml
)
from schemaorg.data import (
    find_similar_types, 
    read_types_csv, 
    read_properties_csv, 
    get_versions
)
from schemaorg.logger import bot
import json
import os
import re
import sys

class Schema(object):

    def __init__(self, schema_type, version=None, base=None):

        self.type = None
        self.properties = {}
 
        # Does the user want a custom base?
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

# Properties

    def add_property(self, name, value):
        '''add a property, only given that it's defined under self._properties.
    
            Parameters
            ==========
            name: the name of the property, made to lowercase
            value: the value to add
        '''
        if value not in ["", None, [], ()]:
            if name in self._properties:
                lookup = self._properties[name]
                self.properties[name] = value
                bot.debug('%s set to %s' %(name, value))

    def remove_property(self, name):
        '''remove a property, meaning the instance property > self.properties
    
            Parameters
            ==========
            name: the name of the property, made to lowercase
        '''
        del self.properties[name.lower()] 


    def dump_json(self, pretty_print=False):
        '''get and them dump the json into a string, for writing into templates
        
           Parameters
           ==========
           pretty_print: if True, pretty print the json (default is false)
        '''
        metadata = self.get_json()
        if pretty_print:
            return print_json(metadata)
        return json.dumps(metadata)


    def get_json(self):
        '''Extract the json representation of the Schema,
           meaning that we recursively unwrap other Schemas, along with
           including the context and type.
        '''
        from schemaorg.templates.metadata import unwrap_properties
        metadata = unwrap_properties(self.properties)
        metadata['@context'] = self.base
        metadata['@type'] = self.type
        return metadata

    def get_flattened(self):
        '''Extract a flat representation of the Schema,
           meaning that we recursively unwrap other Schemas, along with
           including the context and type into a single level dictionary
        '''
        from schemaorg.templates.metadata import flatten_schema
        metadata = flatten_schema(self.properties)
        metadata['@context'] = self.base
        metadata['@type'] = self.type
        return metadata


# Load

    def load_type(self, schema_type):
        '''load a type. Expected to be called upon init, but also allowed
           to be called once already loaded. The type and properties must be
           loaded together to ensure being in sync.
 
           Parameters
           ==========
           schema_type: the type to load
        '''
        # Keep property definitions here
        self._properties = dict()

        # If we are given a file, it's likely a custom specification
        if os.path.isfile(schema_type):
            self._load_custom_type(schema_type)
            self._load_custom_props()

        # Load type (defined or custom) followed by properties
        else:
            self._load_type(schema_type)
            self._load_props()

        self._load_attributes()


    def _load_custom_type(self, file_path):
        '''load a custom file into the schema, usually a yaml or html file.

           Parameters
           ==========
           file_path: the file to load, either yaml or html
        '''
        if file_path.endswith('html'):
            stream = read_file(file_path, readlines=False)
            self.loaded = _read_yaml(stream, quiet=True)

        # Yaml file
        else:
            self.loaded = read_yaml(file_path, quiet=True)

        # Set the type and url
        self._set_type(self.loaded['name'])

        # Load the type, or save to the object (very error prone)
        self.type_spec = self.loaded['spec_info']
        self.type_spec['id'] = self.url
        self.type_spec['label'] = self.loaded['name']
        self.type_spec['comment'] = self.loaded['description']
        self.type_spec['subTypeOf'] = self.loaded['parent_type']

# Properties

    def _load_custom_props(self, key = 'mapping', field="property"):
        '''load custom properties will extract properties into the Schema from
           a list, where some field in the list is the ID to give to the
           self._properties dictionary. This function assumes the openschemas
           draft export, where the main key in the yaml dict is "mapping"
           and the name of the property is "property." We allow for properties
           that are not defined (new with the proposed specification).

           Parameters
           ==========
           key: the key in self.loaded (the yaml) with properties
           field: the field of each property that holds the name (the id)
        '''
        lookup = read_properties_csv(version=self.version)

        # Need to parse, under key "mapping" and with uid "property"
        props = self.loaded[key]

        for prop in props:
            name = "http://schema.org/%s" % prop[field]

            self._properties[prop[field]] = dict()
  
            # Filter out empty ones
            prop = {k:v for k,v in prop.items() if v}

            # First add schema.org
            if name in lookup:

                # The label is the most human friendly key
                self._properties[prop[field]] = lookup[name]

            # Update with custom
            self._properties[prop[field]].update(prop)

        bot.info('%s: found %s properties' %(self.type, len(self._properties)))


    def _load_props(self):
        '''load properties based on the type defined for the object. Can
           (or should) only be called with load_type, so the two are in sync
           This function is strict in that it will error if there is a missing
           property in the lookup, so it is not meant for custom properties.

           self._properties: a lookup of those allowed, with definitions, etc.
           self.properties: another lookup, but with the property values
        '''
        lookup = read_properties_csv(version = self.version)

        # Need to parse, split by comma and strip empty spaces
        props = self.type_spec['properties'].split(',')
        props = [p.strip() for p in props]

        for prop in props:
            if prop in lookup:

                # The label is the most human friendly key
                self._properties[lookup[prop]['label']] = lookup[prop]

        bot.info('%s: found %s properties' %(self.type, len(self._properties)))


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
        if schema_type not in typs:
            bot.error('%s is not a valid type!' % schema_type)
            self.print_similar_types(schema_type)
            sys.exit(1)

        self._set_type(schema_type)
        bot.info('Found %s' % self.url)

        # Load the type, or save to the object
        self.type_spec = typs[self.type]
 

    def _set_type(self, schema_type):
        '''Given a string schema type, load the type from the lookup dictionary,
           and set the url of the class from the base.

           Parameters
           ==========
           schema_type: the type to save to the self.type attribute
        '''
        # It's good! Save to object
        self.type = schema_type

        # Assemble the type url
        self.url = "%s/%s" % (self.base, self.type)


    def _load_attributes(self):
        ''' add the attributes from the loaded type_spec to the class.
        '''
        # Add as attributes to the object
        for attr in list(self.type_spec.keys()):
            if attr not in ['properties']:
                setattr(self, attr, self.type_spec[attr])


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

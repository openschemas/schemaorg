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

import json
import tempfile
import os
import re
import sys

from schemaorg.logger import bot
from schemaorg.utils import ( 
    read_file,
    write_file,
    read_yaml,
    write_yaml 
)
from schemaorg.main.parse.base import RecipeBase
from schemaorg.main.parse.validate import validate

class RecipeParser(RecipeBase):

    filename = None

    def __init__(self, recipe=None):
        '''a recipe parses an input recipe file, a yaml file, into the expected 
           fields of labels, comments, and lists of required fields.

           Parameters
           ==========
           recipe: the recipe file (yaml)

        '''

        self.loaded = {}

        # Did the user provide a path to load?
        if recipe is not None:
            self.set_filename(recipe)
        super(RecipeParser, self).__init__(recipe)


    def set_filename(self, file_path):
        if self._validate_exists(file_path):
            self.filename = file_path
        else:
            bot.warning("%s does not exist." % file_path)

 
    def _parse(self):
        '''parse is the base function for parsing the recipe, and extracting
           elements into the correct data structures. Everything is parsed into
           lists or dictionaries that can be assembled again on demand.     
        '''
        self.load()

    def _validate_exists(self, filename = None):
        '''first determine if the filename is defined, with preference
           to a potentially new file set by the user at runtime. If not set,
           use previously loaded file. In both cases, first check if the
           file exists. Return False if not defined or doesn't exist

           Parameters
           ==========
           filename: a yaml file path, if desired, to override previously set
        '''
        if not filename:
            filename = self.filename

        if filename not in ['', None]:
            if os.path.exists(filename):
                return True
            else:
                bot.warning("%s does not exist." % filename)
        else:
            bot.warning("Yaml file is not defined.")
        return False

    def load(self, file_path=None):
        '''load the yaml file depending on its extension

           Parameters
           ==========
           file_path: a yaml/html file path, if desired, to override previous
        '''

        if not file_path:
            file_path = self.filename

        # Read in raw content
        if self._validate_exists(file_path):

            # Read in yaml as frontend matter from html
            if file_path.endswith('html'):
                self._load_html(file_path)

            # Read in standard yaml
            else:
                self._load_yaml(file_path)


            # Unpack or statements
            self._finish_load()
            return self.loaded

# Loading

    def _load_yaml(self, file_path):
        '''load the yaml file

           Parameters
           ==========
           file_path: the yaml file path to read
        '''
        self.loaded = read_yaml(file_path)

        
    def _load_html(self, file_path):
        '''load the yaml as frontend matter from an html file

           Parameters
           ==========
           file_path: an html file path to read
        '''
        stream = read_file(file_path, readlines=False)
        self.loaded = frontmatter.loads(stream).metadata


    def _finish_load(self):
        '''The user is allowed to package "or" statements in the Yaml, meaning
           that a redundant entry for an equally defined Person and Organization
           could be written as "Person|Organization." To unwrap this, we put
           each into its own duplicated field.
        '''
        finished = dict()
        for name, value in self.loaded['schemas'].items():
            finished[name] = value
            if "|" in name:
                for part in name.split('|'):
                    finished[part] = value
                    
        self.loaded['schemas'] = finished

# Saving

    def save_yml(self, output_file, content=None, mode = 'w', ext='yml'):
        '''save a yml file, either provided by the client (content)
           or if not provided, the loaded content.
         
           Parameters
           ==========
           output_file: the output file to save to. Should end in yml or yaml
           content: the content to parse to yaml, can be str or dict
           mode: the mode to use (default is w, write)

        '''
        # If content isn't provided, use client loaded content (must be dict)
        if not content:
            content = self.loaded
        
        # Remove any derivation (won'account for compressed e.g., .tar.gz)
        output_file, _ = os.path.splitext(output_file)

        # Ensure ends with a yml derivative extension
        if not re.search('(%s$)' % ext, output_file):
            output_file = "%s.%s" % (output_file, ext)

        # Write the yaml to file
        write_yaml(content, output_file, mode) 

    def save_yaml(self, output_file, content=None, mode = 'w'):
        return self.save_yml(output_file, content, mode, ext='yaml')


# Reading

    def get_key(self, key='schemas'):
        '''return a portion of the yml file based on key

           Parameters
           ==========
           key: defaults to specifications
        '''
        # If not yet loaded, load it based on extension
        if not hasattr(self, 'loaded'):
            self.load(self.filename)
        return self.loaded[key]

# Validation

    def validate(self, schema):
        '''validate a schema, meaning checking that it includes all properties
           required by the recipe.
        '''
        if self.loaded:
            return validate(schema, self)
        bot.error('Recipe has not been loaded. Try recipe.load().')
        return False

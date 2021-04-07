__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2018-2021, Vanessa Sochat"
__license__ = "MPL 2.0"

import json
import tempfile
import os
import re
import sys

from schemaorg.logger import bot
from schemaorg.utils import ( 
    read_file,
    read_frontmatter,
    write_file,
    read_yaml,
    write_yaml 
)
from schemaorg.main.parse.base import RecipeBase
from schemaorg.main.parse.validate import validate


class RecipeParser(RecipeBase):

    def __init__(self, recipe=None):
        '''a recipe parses an input recipe file, a yaml file, into the expected 
           fields of labels, comments, and lists of required fields.

           Parameters
           ==========
           recipe: the recipe file (yaml)

        '''
        # The base will load the recipe, and then return to _load
        super(RecipeParser, self).__init__(recipe)
 

    def _load(self):
        '''The user is allowed to package "or" statements in the Yaml, meaning
           that a redundant entry for an equally defined Person and Organization
           could be written as "Person|Organization." To unwrap this, we put
           each into its own duplicated field.
        '''
        finished = dict()

        # If we aren't loading schemas, won't have this attribute.

        if 'schemas' in self.loaded:
            for name, value in self.loaded['schemas'].items():
                finished[name] = value
                if "|" in name:
                    for part in name.split('|'):
                        finished[part] = value
                    
        self.loaded['schemas'] = finished


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

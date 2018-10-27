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
from schemaorg.utils import ( read_file, write_file )


class RecipeBase(object):
    '''A recipe base is a template for a domain specific recipe parser.

       Parameters
       ==========
       recipe: the original recipe file.

    '''

    def __init__(self, recipe=None):
        self.load(recipe)

    def load(self, recipe):
        '''load a recipe file into the client, first performing checks, and
           then parsing the file.

           Parameters
           ==========
           recipe: the original recipe file, parsed by subclass
 
        '''
        self.filename = recipe           # the recipe file
        self._run_checks()             # does the recipe file exist?
        self.parse()

    def __str__(self):
        ''' show the user the recipe object, along with the type. E.g.,       
            [schemaorg-recipe][SoftwareSourceCode]

        '''

        base = "[schemaorg-recipe]"
        if self.filename:
            base = "%s[%s]" %(base, self.filename)
        return base

    def __repr__(self):
        return self.__str__()


    def _run_checks(self):
        '''basic sanity checks for the file name (and others if needed) before
           attempting parsing.
        '''
        if self.filename is not None:

            # Does the recipe provided exist?
            if not os.path.exists(self.filename):
                bot.error("Cannot find %s, is the path correct?" %self.filename)
                sys.exit(1)

            # Ensure we carry fullpath
            self.filename = os.path.abspath(self.filename)


# Parse

    def parse(self):
        '''parse is the base function for parsing the recipe. Right now, this
           function basically calls the subclass _parse function if the recipe
           has been defined.
        '''

        if self.filename:

            # If properly instantiated by Docker or Singularity Recipe, parse
            if hasattr(self, '_parse'):
                self._parse()

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
    read_frontmatter,
    write_file,
    read_yaml,
    write_yaml 
)


class RecipeBase(object):
    '''A recipe base is a template for a domain specific recipe parser.

       Parameters
       ==========
       recipe: the original recipe file.

    '''

    loaded = {}
    filename = None

    def __init__(self, recipe=None):

        # Did the user provide a path to load?
        if recipe is not None:
            self.set_filename(recipe)

        # Load the recipe if provided and exists
        if self.filename is not None:
            self.load()

    def set_filename(self, file_path):
        '''add the filename to be parsed to the class

           Parameters
           ==========
           file_path: the original recipe file, parsed by subclass
        '''
        if self._validate_exists(file_path):
            self.filename = file_path
        else:
            bot.warning("%s does not exist." % file_path)


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


    def _validate_exists(self, filename=None):
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

        if filename in ['', None]:
            bot.warning("Yaml file is not defined.")
        elif not os.path.exists(filename):
            bot.warning("%s does not exist." % filename)
        return os.path.exists(filename or '')


# Load


    def load(self, file_path=None):
        '''load the yaml file depending on its extension. We can handle
           html with json-ld, json-ld (or just json), markdown, and yaml.

           Parameters
           ==========
           file_path: a yaml/html file path, if desired, to override previous
        '''

        if not file_path:
            file_path = self.filename

        # Read in raw content
        if self._validate_exists(file_path):

            # Read in yaml as json-ld from html
            if file_path.endswith('html'):
                self._load_html(file_path)

            # Read in yaml as frontend matter
            elif re.search('(md|markdown)$', file_path):
                self.loaded = read_frontmatter(file_path)
        
            elif file_path.endswith('json'):
                self.loaded = read_json(file_path)

            # Read in standard yaml
            else:
                self.loaded = read_yaml(file_path, quiet=True)

            # If the subclass has a load function, call now
            if hasattr(self, '_load'):
                self._load()

            # Unpack or statements
            return self.loaded
             


# Loading Helpers


    def _load_html(self, file_path, encoding='utf-8'):
        '''load as json-ld from html

           Parameters
           ==========
           file_path: an html file path to read
        '''
        import lxml.html
        import lxml
        jsonld = lxml.etree.XPath('descendant-or-self::script[@type="application/ld+json"]')

        try:
            parser = lxml.html.HTMLParser(encoding=encoding)
            content = read_file(file_path, readlines=False)
            tree = lxml.html.fromstring(content, parser=parser)
            self.loaded = json.loads(jsonld(tree)[0].text)
        except:
            bot.error('Error loading %s, is there json-ld in a script tag?' % file_path)


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

#!/usr/bin/python

# Copyright (C) 2019 Vanessa Sochat.

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
# License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from schemaorg.templates.google import make_person
from schemaorg.main.parse import RecipeParser
from schemaorg.main import Schema
import shutil
import os
import unittest
import tempfile

print("######################################################## test_schema")

class TestSchema(unittest.TestCase):

    def setUp(self):
        self.tmpdir = os.path.join(tempfile.gettempdir(), 'schemaorg-test')

        if not os.path.exists(self.tmpdir):
            os.mkdir(self.tmpdir)

        self.here = os.path.abspath(os.path.dirname(__file__))
        recipe_yml = os.path.join(self.here, "recipe.yml")
        self.recipe = RecipeParser(recipe_yml)
        self.dataset = Schema("Dataset")
        self.templates = ['google/dataset-table.html',  # bootstrap
                          'google/visual-dataset.html', # default
                          'google/dataset.html',        # json only 
                          'google/dataset-vue-table.html'] # vue js

        person = make_person(name="Dinosaur Pancakes", 
                             description='Dataset maintainer',
                             url='https://www.github.com/vsoch',
                             contact_type='customer suppoert',
                             telephone = '999-999-9999')
        self.dataset.add_property('creator', person)

        self.dataset.add_property('version', "1.0.0")
        self.dataset.add_property('description', "This is the best dataset.")
        self.dataset.add_property('name', "Dinosaur Dataset")
        self.dataset.add_property('thumbnailUrl', 'https://vsoch.github.io/datasets/assets/img/avocado.png')
        self.dataset.add_property('about', "This is a dataset")
        self.recipe.validate(self.dataset)        

    def tearDown(self):
        pass


    def test_schema(self):

        print('Testing flattened...')
        flat = self.dataset.get_flattened()
        print(flat)
        self.assertTrue(isinstance(flat, dict))


if __name__ == '__main__':
    unittest.main()

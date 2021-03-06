__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2018-2021, Vanessa Sochat"
__license__ = "MPL 2.0"

from schemaorg.templates.google import ( 
    make_dataset, 
    make_person
)
from schemaorg.main.parse import RecipeParser
from schemaorg.main import Schema
import ast
import shutil
import os
import tempfile
import unittest

print("######################################################## test_templates")

class TestTemplates(unittest.TestCase):

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
                             contact_type='customer support',
                             telephone = '999-999-9999')
        self.dataset.add_property('creator', person)
        self.dataset.add_property('version', "1.0.0")
        self.dataset.add_property('description', "This is the best dataset.")
        self.dataset.add_property('name', "Dinosaur Dataset")
        self.dataset.add_property('thumbnailUrl', 'https://vsoch.github.io/datasets/assets/img/avocado.png')
        self.dataset.add_property('about', "This is a dataset")
        download = Schema('DataDownload')
        download.add_property('contentUrl', 'https://vsoch.github.io/datasets/assets/img/avocado.png')
        download.add_property('encodingFormat', 'CSV')
        self.dataset.add_property('distribution', [download])
        self.recipe.validate(self.dataset)        

    def tearDown(self):
        pass
        #shutil.rmtree(self.tmpdir)


    def test_templates(self):

        print('Testing templates generation...')
        for template in self.templates:
            prefix, ext = os.path.splitext(template)
            output_file = os.path.join(self.tmpdir, os.path.basename(prefix) + '.html')
            html = make_dataset(self.dataset, output_file, template=template)
            print(output_file)


if __name__ == '__main__':
    unittest.main()

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

import os
import re
import sys

from schemaorg.main import Schema
from schemaorg.utils import write_file
from schemaorg.templates import get_template

# Google Dataset Helpers

def make_person(name, description, url="", telephone="", email=""):

    # Create an individual (persona)
    person = Schema('Person')
    person.add_property('name', name)
    contactPoint = Schema('ContactPoint')

    # Update the contact point
    contactPoint.add_property('telephone', telephone)
    contactPoint.add_property('email', email)

    # Update the person with it
    person.add_property('contactPoint', contactPoint)
    return person

def make_template_base(schema, template, pretty_print):
    template = get_template(template)
    metadata = schema.dump_json(pretty_print)
    template = template.replace("{{ SCHEMAORG_JSON }}", metadata)
    return template    


def make_dataset(schema,
                 output_file=None,
                 pretty_print=True,
                 template="google/visual-dataset.html"):

    '''write a dataset. By default, this means a schema.org "Dataset" and we use
       the Dataset.html template. You can substitute any of the input parameters
       to change these variables. If an output file is provided, we write the
       template to the file. Otherwise, we just return it.
    '''
    template = make_template_base(schema, template, pretty_print)
    if output_file is not None:
        write_file(output_file, template)
    return template


def make_table(schema,
               rows,                 
               output_file=None,
               pretty_print=True,
               title=None,
               template="google/visual-table.html"):

    '''write a data catalog, meaning rows of data. You should include, as rows,
       a list of rows as you want them (e.g., each with <tr><td>...</tr></td>.
       If an output file is provided, we write to file.
    '''
    template = make_template_base(schema, template, pretty_print)
    template = template.replace("{{ SCHEMAORG_TITLE }}", title or "Schema.org Data Catalog")
    template = template.replace('{{ SCHEMAORG_TABLE }}', '\n'.join(rows))
    if output_file is not None:
        write_file(output_file, template)
    return template

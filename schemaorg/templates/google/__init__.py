'''

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

import os
import re
import sys

from schemaorg.main import Schema
from schemaorg.utils import write_file
from schemaorg.templates import get_template

# Google Dataset Helpers

def make_person(name, description, url="", telephone="", email="", 
                contact_type="customer support"):

    # Create an individual (persona)
    person = Schema('Person')
    person.add_property('name', name)
    contactPoint = Schema('ContactPoint')

    # Update the contact point
    contactPoint.add_property('telephone', telephone)
    contactPoint.add_property('email', email)
    contactPoint.add_property('url', url)
    contactPoint.add_property('contactType', contact_type)

    # Update the person with it
    person.add_property('contactPoint', contactPoint)
    return person

def make_template_base(schema, template, pretty_print):
    '''make template base is the simplest function to export (and replace)
       only SCHEMAORG_JSON template tags.
    '''
    template = get_template(template)
    metadata = schema.dump_json(pretty_print)
    template = template.replace("{{ SCHEMAORG_JSON }}", metadata)
    return template    


def make_vue_table(schema, template, pretty_print, title=None, output_file=None):
    '''google/dataset-vue-table.html
       SCHEMAORG_ITEMS needs to be a list of key value pairs
       with properties, e.g., { name: 'One', value: '98' }
    '''
    template = get_template(template)

    # Set the title
    title = schema.properties.get('name', 'Google Dataset')
    template = template.replace("{{ SCHEMAORG_TITLE }}", title)

    # Metadata (properties) are rendered into table
    metadata = []
    for key, value in schema.get_flattened().items():
        metadata.append({"name": key, "value": value})
    template = template.replace("{{ SCHEMAORG_ITEMS }}", str(metadata))

    thumbnail = get_thumbnail_url(schema)
    template = template.replace("{{ SCHEMAORG_THUMBNAIL }}", thumbnail)        

    metadata = schema.dump_json(pretty_print)
    template = template.replace("{{ SCHEMAORG_JSON }}", metadata)

    # Write to file, if an output file provided
    if output_file is not None:
        write_file(output_file, template)

    return template    


def get_thumbnail_url(schema):
    thumbnail = ''

    # If there is a thumbnail, replace it.
    if "thumbnailUrl" in schema.properties:
        thumbnail = schema.properties.get('thumbnailUrl', '')
        if thumbnail != '':
            thumbnail = '<img style="position:absolute;top:10px;right:10px" src="%s" width=150px>' % thumbnail
    return thumbnail


def make_bootstrap_table(schema, template, pretty_print, output_file=None):
    '''google/dataset-table.html
    '''
    template = get_template(template)

    # Set the title
    title = schema.properties.get('name', 'Google Dataset')
    description = schema.properties.get('description', 'This is a Google Dataset.')
    template = template.replace("{{ SCHEMAORG_TITLE }}", title)
    template = template.replace("{{ SCHEMAORG_DESCRIPTION }}", description)

    # Rows of the table
    rows = []
    for key, value in schema.get_flattened().items():
        rows.append('<tr><td>%s</td><td>%s</td></tr>' %(key, value))   
    template = template.replace("{{ SCHEMAORG_ROWS }}", '\n'.join(rows))

    thumbnail = get_thumbnail_url(schema)
    template = template.replace("{{ SCHEMAORG_THUMBNAIL }}", thumbnail)        

    metadata = schema.dump_json(pretty_print)
    template = template.replace("{{ SCHEMAORG_JSON }}", metadata)

    # Write to file, if an output file provided
    if output_file is not None:
        write_file(output_file, template)

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
    # Option 1, a visual of the json on the page
    if template == "google/visual-dataset.html":
        template = make_template_base(schema, template, pretty_print)

    # Option 2, google/dataset-vue-table.html
    elif template == 'google/dataset-vue-table.html':
        template = make_vue_table(schema, template, pretty_print)

    # Option 3, google/dataset-table.html (bootstrap)
    elif template == 'google/dataset-table.html':
        template = make_bootstrap_table(schema, template, pretty_print)

    # Option 4: default 
    elif template == 'google/dataset.html':
        template = make_template_base(schema, template, pretty_print)

    if output_file is not None:
        write_file(output_file, template)
    return template


def make_table(schema,
               rows=None,                 
               output_file=None,
               pretty_print=True,
               title=None,
               template="google/visual-table.html"):

    '''write a data catalog, meaning rows of data. You should include, as rows,
       a list of rows as you want them (e.g., each with <tr><td>...</tr></td>.
       If no rows are provided, the schema is export into rows.
       If an output file is provided, we write to file.
    '''
    # If the user doesn't provide rows, create them
    if rows == None:
        rows = []
        for key, value in schema.properties.items():
            rows.append('<tr><td>%s</td><td>%s</td></tr>' %(key, value))

    template = make_template_base(schema, template, pretty_print)
    template = template.replace("{{ SCHEMAORG_TITLE }}", title or "Schema.org Data Catalog")
    template = template.replace('{{ SCHEMAORG_TABLE }}', '\n'.join(rows))
    if output_file is not None:
        write_file(output_file, template)
    return template

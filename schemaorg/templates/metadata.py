'''

Interaction with metadata and properties

Copyright (C) 2018-2020 Vanessa Sochat.

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

from schemaorg.logger import bot
import os
import re
import sys

def unwrap_properties(metadata):
    '''unwrap a Schema properties dictionary, meaning if we find additional
       Schemas, return their dictionary representation. This function does not 
       provide a top level context, this is provided by the Schema class.
       
       Parameters
       ==========
       metadata: the dictionary to unwrap, usually the highest 
                 level schema.properties
    '''
    from schemaorg.main import Schema

    # In case the user provides the schema directly
    if isinstance(metadata, Schema):
        metadata = metadata.properties

    unwrapped = dict()
    for prop, value in metadata.items():
        if isinstance(value, Schema):
            unwrapped[prop] = unwrap_properties(value.properties)
            unwrapped[prop].update({'@type': value.type})
        elif isinstance(value, list):
            items = []
            for item in value:
                if isinstance(item, Schema):
                    new_item = unwrap_properties(item.properties)
                    new_item.update({'@type': item.type})
                else:
                    new_item = item
                items.append(new_item)
            unwrapped[prop] = items
        else:
            unwrapped[prop] = metadata[prop]
    return unwrapped

def flatten_schema(metadata, prefix='', flattened=None):
    '''flatten a Schema properties dictionary into a list, 
       meaning if we find additional Schemas, return them flat.

       Parameters
       ==========
       metadata: the dictionary to unwrap, usually the highest 
                 level schema.properties
    '''
    from schemaorg.main import Schema

    if isinstance(metadata, Schema):
        prefix = prefix + '.' + metadata.type
        original = prefix
        metadata = metadata.properties
   
    # First call into recursion, will be None
    if flattened == None:
        flattened = dict()

    # Flatten the metadata
    for prop, value in metadata.items():
        prefix = ('%s.%s' %(prefix, prop)).lstrip('.')

        # Option 1: Another schema, call recursively
        if isinstance(value, Schema):
            flattened = flatten_schema(value, prefix, flattened)
            flattened[prefix + "@type"] = value.type

        # Option 2: Unwrap a list
        elif isinstance(value, list):
            for i in range(len(value)):
                item = value[i]
                prefix = prefix + '.' + str(i)
                if isinstance(item, Schema):
                    flattened = flatten_schema(item, prefix, flattened)
                    flattened[prefix + '@type'] = item.type
                else:
                    flattened[prefix] = item
        else:
            flattened[prefix] = metadata[prop]
        prefix = original
    return flattened

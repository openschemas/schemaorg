'''

Interaction with metadata and properties

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
        else:
            unwrapped[prop] = metadata[prop]
    return unwrapped

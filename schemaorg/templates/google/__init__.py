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


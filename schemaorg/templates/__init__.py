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

from schemaorg.utils import ( get_installdir, read_file )
from schemaorg.logger import bot
import os

def get_template(name="google/dataset.html"):
    '''get a template from the templates folder base. By default, we return
       the Google Datasets schema.org template, since there aren't any others
       defined yet :)

       Parameters
       ==========
       name: the name (subfolder and filename) of the template under templates

    '''
    filename = os.path.join(get_installdir(), 'schemaorg', 'templates', name)
    if os.path.exists(filename):
        return read_file(filename, readlines=False)
    bot.warning('Cannot find %s' % filename)

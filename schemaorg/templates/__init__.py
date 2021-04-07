__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2018-2021, Vanessa Sochat"
__license__ = "MPL 2.0"

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

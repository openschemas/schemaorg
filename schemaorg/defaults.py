__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2018-2021, Vanessa Sochat"
__license__ = "MPL 2.0"

from schemaorg.logger import bot
import tempfile
import os
import sys

################################################################################
# environment / options
################################################################################

def convert2boolean(arg):
    '''convert2boolean is used for environmental variables
       that must be returned as boolean

       Parameters
       ==========
       arg: the argument to convert to boolean. Must be a string given
       grabbed from environment.
    '''
    if not isinstance(arg, bool):
        return arg.lower() in ("yes", "true", "t", "1", "y")
    return arg


def getenv(variable_key, default=None, required=False, silent=True):
    '''getenv will attempt to get an environment variable. If the variable
       is not found, None is returned.
 
       Parameters
       ==========   
       variable_key: the variable name
       required: exit with error if not found
        silent: Do not print debugging information for variable
    '''
    variable = os.environ.get(variable_key, default)
    if variable is None and required:
        bot.error("Cannot find environment variable %s, exiting." %variable_key)
        sys.exit(1)

    if not silent and variable is not None:
            bot.verbose("%s found as %s" %(variable_key,variable))

    return variable


################################################################################
# SchemaOrg Python


#########################
# Global Settings
#########################

# Version of schema.org to use, defaults to latest in list of installed
SCHEMAORG_VERSION = getenv('SCHEMAORG_VERSION')

#########################
# Temporary Storage
#########################

SCHEMAORG_TMPDIR = os.environ.get('SCHEMAORG_TMPDIR', tempfile.gettempdir())

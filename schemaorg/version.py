__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2018-2021, Vanessa Sochat"
__license__ = "MPL 2.0"

__version__ = "0.1.0"
AUTHOR = 'Vanessa Sochat'
AUTHOR_EMAIL = 'vsoch@users.noreply.github.com'
NAME = 'schemaorg'
PACKAGE_URL = "https://github.com/openschemas/schemaorg"
KEYWORDS = 'openschemas, schema.org'
DESCRIPTION = "Python functions for applied use of schema.org"
LICENSE = "LICENSE"

################################################################################
# Global requirements

INSTALL_REQUIRES = (
   ('pyaml', {'min_version': '17.12.1'}),
   ('lxml', {'min_version': '4.1.1' })
)

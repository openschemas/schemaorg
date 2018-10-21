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

import hashlib
import errno
import pwd
import re
import shutil
import tempfile
import csv

import json
from schemaorg.logger import bot
from subprocess import (
    Popen,
    PIPE,
    STDOUT
)
import os

################################################################################
# Software Versions
################################################################################


def get_schemaorg_version():
    '''determine the schemaorg version to use based on an environmental variable
       first followed by  using the latest.
    '''
    from schemaorg.defaults import SCHEMAORG_VERSION as version

    if version is None:
        base = get_database()
        versions = os.listdir(base)
        versions.sort()
        version = versions[-1]

    bot.debug("schemaorg version %s selected" % version)
    return version

def get_installdir():
    '''get_installdir returns the installation directory of the application
    '''
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def get_release(version = None):
    '''get a subfolder for a particular release, defaults to latest
    '''
    base = get_database()
    if version is None:
        version = get_schemaorg_version()
    return os.path.join(base, "releases", version)


def get_database():
    '''get the data folder with "release" and "ext" subfolders
    '''
    return os.path.join(get_installdir(), "data")


def run_command(cmd, sudo=False):
    '''run_command uses subprocess to send a command to the terminal.

        Parameters
        ==========
        cmd: the command to send, should be a list for subprocess
        error_message: the error message to give to user if fails,
        if none specified, will alert that command failed.

    '''
    if sudo is True:
        cmd = ['sudo'] + cmd

    try:
        output = Popen(cmd, stderr=STDOUT, stdout=PIPE)

    except FileNotFoundError:
        cmd.pop(0)
        output = Popen(cmd, stderr=STDOUT, stdout=PIPE)

    t = output.communicate()[0],output.returncode
    output = {'message':t[0],
              'return_code':t[1]}

    if isinstance(output['message'], bytes):
        output['message'] = output['message'].decode('utf-8')

    return output


################################################################################
## FOLDER OPERATIONS ###########################################################
################################################################################


def mkdir_p(path):
    '''mkdir_p attempts to get the same functionality as mkdir -p
    :param path: the path to create.
    '''
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            bot.error("Error creating path %s, exiting." % path)
            sys.exit(1)


def get_tmpfile(requested_tmpdir=None, prefix=""):
    '''get a temporary file with an optional prefix. By default will be
       created in /tmp unless SCHEMAORG_TMPDIR is set. By default, the file
       is closed (and just a name returned).

       Parameters
       ==========
       requested_tmpdir: an optional requested temporary directory, first
       priority as is coming from calling function.
       prefix: Given a need for a sandbox (or similar), prefix the file
       with this string.
    '''

    # First priority for the base goes to the user requested.
    tmpdir = get_tmpdir(requested_tmpdir)

    # If tmpdir is set, add to prefix
    if tmpdir is not None:
        prefix = os.path.join(tmpdir, os.path.basename(prefix))

    fd, tmp_file = tempfile.mkstemp(prefix=prefix) 
    os.close(fd)

    return tmp_file


def get_tmpdir(requested_tmpdir=None, prefix="", create=True):
    '''get a temporary directory for an operation. If SREGISTRY_TMPDIR
       is set, return that. Otherwise, return the output of tempfile.mkdtemp

       Parameters
       ==========
       requested_tmpdir: an optional requested temporary directory, first
       priority as is coming from calling function.
       prefix: Given a need for a sandbox (or similar), we will need to 
       create a subfolder *within* the SREGISTRY_TMPDIR.
       create: boolean to determine if we should create folder (True)
    '''
    from schemaorg.defaults import SCHEMAORG_TMPDIR

    # First priority for the base goes to the user requested.
    tmpdir = requested_tmpdir or SCHEMAORG_TMPDIR

    prefix = prefix or "schemaorg-tmp"
    prefix = "%s.%s" %(prefix, next(tempfile._get_candidate_names()))
    tmpdir = os.path.join(tmpdir, prefix)

    if not os.path.exists(tmpdir) and create is True:
        os.mkdir(tmpdir)

    return tmpdir

def get_userhome():
    '''get the user home based on the effective uid
    '''
    return pwd.getpwuid(os.getuid())[5]


def get_content_hash(contents):
    '''get_content_hash will return a hash for a list of content (bytes/other)
    '''
    hasher = hashlib.sha256()
    for content in contents:
        if isinstance(content, io.BytesIO):
            content = content.getvalue()
        if not isinstance(content, bytes):
            content = bytes(content)
        hasher.update(content)
    return hasher.hexdigest()


################################################################################
## FILE OPERATIONS #############################################################
################################################################################

def copyfile(source, destination, force=True):
    '''copy a file from a source to its destination.
    '''
    # Case 1: It's already there, we aren't replacing it :)
    if source == destination and force is False:
        return destination

    # Case 2: It's already there, we ARE replacing it :)
    if os.path.exists(destination) and force is True:
        os.remove(destination)

    shutil.copyfile(source, destination)
    return destination


def write_file(filename, content, mode="w"):
    '''write_file will open a file, "filename" and write content, "content"
       and properly close the file
    '''
    with open(filename, mode) as filey:
        filey.writelines(content)
    return filename


def read_file(filename, mode="r", readlines=True):
    '''write_file will open a file, "filename" and write content, "content"
       and properly close the file
    '''
    with open(filename, mode) as filey:
        if readlines is True:
            content = filey.readlines()
        else:
            content = filey.read()
    return content


# Json

def write_json(json_obj, filename, mode="w", print_pretty=True):
    '''write_json will (optionally,pretty print) a json object to file

       Parameters
       ==========
       json_obj: the dict to print to json
       filename: the output file to write to
       pretty_print: if True, will use nicer formatting
    '''
    with open(filename, mode) as filey:
        if print_pretty:
            filey.writelines(print_json(json_obj))
        else:
            filey.writelines(json.dumps(json_obj))
    return filename



def print_json(json_obj):
    ''' just dump the json in a "pretty print" format
    '''
    return json.dumps(
                    json_obj,
                    indent=4,
                    separators=(
                        ',',
                        ': '))


def read_json(filename, mode='r'):
    '''read_json reads in a json file and returns
       the data structure as dict.
    '''
    with open(filename, mode) as filey:
        data = json.load(filey)
    return data


# csv

def read_csv(filename, mode='r', delim=',', header=None, keyfield=None):
    '''read a comma separated value file, with default delimiter as comma.
       we assume reading a header, and use some identifier as key.

       Parameters
       ==========
       filename: the name of the csv file to read
       mode: the mode to read in (defaults to r)
       delim: the delimiter (defaults to comma)
    '''
    if not os.path.exists(filename):
        bot.exit('%s does not exist.' % filename)           

    # If we have a keyfield, return dictionary
    data = []
    if keyfield is not None:
        data = dict()

    with open(filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, fieldnames=header)
        for row in csv_reader:
            if keyfield is not None:
                data[row[keyfield]] = row
            else:
                data.append(row)
    return data

# courtesy functions for schema.org exports

'''
List of available csv --------------------------------------
all-layers-properties.csv  ext-health-lifesci-properties.csv
all-layers-types.csv       ext-health-lifesci-types.csv
ext-attic-properties.csv   ext-meta-properties.csv
ext-attic-types.csv        ext-meta-types.csv
ext-auto-properties.csv    ext-pending-properties.csv
ext-auto-types.csv         ext-pending-types.csv
ext-bib-properties.csv     schema-properties.csv
ext-bib-types.csv          schema-types.csv
'''

def read_properties_csv(keyfield='id', version=None):
    '''read in the properties csv (with all types), defaulting to using
       the "id" as the lookup key. We do this because the properties listed
       in the types csv include the full uri.
  
       Parameters
       ==========
       keyfield: the key to use to generate the lookup, a header in the csv
       version: release version under data/releases to use, defaults to latest
    '''
    release_dir = get_release(version = version)
    filename = os.path.join(release_dir, 'schema-properties.csv')
    return read_csv(filename, keyfield=keyfield)


def read_types_csv(keyfield='label', version=None):
    '''read in the types csv, with default lookup key as "label" since the
       likely use case will be the user searching for an item of interest.

       Parameters
       ==========
       keyfield: the key to use to generate the lookup, a header in the csv
       version: release version under data/releases to use, defaults to latest
    '''
    release_dir = get_release(version = version)
    filename = os.path.join(release_dir, 'schema-types.csv')
    return read_csv(filename, keyfield=keyfield)

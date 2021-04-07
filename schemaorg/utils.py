__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2018-2021, Vanessa Sochat"
__license__ = "MPL 2.0"

import hashlib
import errno
import re
import shutil
import tempfile
import yaml
import csv

import json
from schemaorg.logger import bot
from subprocess import (
    Popen,
    PIPE,
    STDOUT
)
import os


def get_installdir():
    '''get_installdir returns the installation directory of the application
    '''
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


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

# Yaml

def read_yaml(filename, mode='r', quiet=False):
    '''read a yaml file, only including sections between dashes
    '''
    stream = read_file(filename, mode, readlines=False)
    return yaml.load(stream, Loader=yaml.FullLoader)


def write_yaml(yaml_dict, filename, mode="w"):
    '''write a dictionary to yaml file
 
       Parameters
       ==========
       yaml_dict: the dict to print to yaml
       filename: the output file to write to
       pretty_print: if True, will use nicer formatting
    '''
    with open(filename, mode) as filey:
        filey.writelines(yaml.dump(yaml_dict))
    return filename


# Markdown and frontmatter

def read_frontmatter(filename, mode='r', quiet=False):
    '''read a yaml file, only including sections between dashes
    '''
    stream = read_file(filename, mode, readlines=False)

    # The yml section always comes after the --- of the frontmatter
    section = stream.split('---')[1]
    return yaml.load(section, Loader=yaml.FullLoader)


def read_markdown(filename, mode='r'):
    '''read the OTHER part of the markdown file (remove the frontend matter)
    '''
    stream = read_file(filename, mode, readlines=False)

    # The yml section always comes after the --- of the frontmatter
    return stream.split('---')[-1]


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

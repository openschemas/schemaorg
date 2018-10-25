#!/usr/bin/env python

'''
This script will demonstrate how we can extract metadata from a Dockerfile,
and then generate a (html) web template to serve with it so that it is
able to be indexed by Google Datasets (or ideally, similar with the recipe
as a ContainerRecipe.

Author: @vsoch
October 21, 2018

This is a "custom" specification (ContainerRecipe) that is represented in the 
local file, ContainerRecipe.yml. If/when the community can add some representation
to schema.org, you would retrieve the types as follows:

from schemaorg.data import ( read_types_csv, read_properties_csv )
typs = read_types_csv()

props = read_properties_csv()


But since the community is slow to review these changes, I'll be using the
local file that is programatically generated.

    Thing > CreativeWork > SoftwareSourceCode > ContainerRecipe

If you think this is wrong, then put your money where your mouth is
and help the community to define the right spot :)

 - https://groups.google.com/a/opencontainers.org/forum/#!topic/dev/vEupyIGtvJs
 - https://github.com/schemaorg/schemaorg/issues/2059#issuecomment-427208907

'''

## A ContainerRecipe
# Thing > CreativeWork > SoftwareSourceCode > ContainerRecipe

# Step 1. Read in the specification, defaults to latest version
# We have to read in the yml for the custom type
spec = read_yaml("ContainerRecipe.yml")

# Here is how you see the properties
for field in spec['mapping']:
    print(field['property'])

# This is important, so I'll write it out. We need to define these fields,
# and then write them into something that looks quasi like Google Datasets
# https://developers.google.com/search/docs/data-types/dataset

'''
alternateName
applicationCategory
brands
citation          * recommended
ContainerImage
dateCreated
dateModified
description       * required
downloadUrl
entrypoint
featureList
hasPart
help
identifier        * recommended
input
keywords          * recommended
labels
license           * recommended
name              * required
operatingSystem
output
publisher
softwareHelp
softwareRequirements
softwareVersion   * recommended (called version)
url               * recommended
'''
# The goal of what we want is here https://search.google.com/structured-data/testing-tool
# Extra attributes not in our properties (I consider most of these not applicable)

'''
sameAs            * recommended
spatialCoverage   * recommended
temporalCoverage  * recommended
variableMeasured  * recommended
'''

# Step 2. Read in the recipe to tag
from spython.main.parse import DockerRecipe
parser = DockerRecipe()
parser.load("Dockerfile")


## A Container Image
# Thing > ContainerImage

# Step 3. Extract more stuffs wit container-diff
from schemaorg.utils import run_command
'''
Might want to run this separately :)
docker pull "${CONTAINER_NAME}:${tag}";
docker inspect "${CONTAINER_NAME}:${tag}" > "${DOCKER_MANIFEST}";
container-diff analyze "${CONTAINER_NAME}:${tag}" --type=pip --type=file --type=apt --type=history --json > "inspect-${tag}.json";
'''

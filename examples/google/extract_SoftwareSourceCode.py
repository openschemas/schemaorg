#!/usr/bin/env python

'''
This script will demonstrate how we can extract metadata from a Dockerfile,
and then generate a (html) web template to serve with it so that it is
able to be indexed by Google Datasets, but not as a Dataset, as a SoftwareSourceCode.
Google search doesn't have an endpoint for SoftwareSourceCode, so we are
mostly pretending.

Author: @vsoch
October 21, 2018

This is a "custom" specification (ContainerRecipe) that is represented in the 
local file, ContainerRecipe.yml. 

    Thing > CreativeWork > SoftwareSourceCode > ContainerRecipe

But for this first example, we will only use
specifications that are "official" and defined in schema.org so we stop
at "SoftwareSourceCode"

    Thing > CreativeWork > SoftwareSourceCode

If you think this is wrong, then put your money where your mouth is
and help the community to define the right spot. :)

 - https://groups.google.com/a/opencontainers.org/forum/#!topic/dev/vEupyIGtvJs
 - https://github.com/schemaorg/schemaorg/issues/2059#issuecomment-427208907

'''

from schemaorg.main.parse import RecipeParser
from schemaorg.main import Schema

################################################################################
## Example 1: Define Dockerfile with SoftwareSourceCode
## Thing > CreativeWork > SoftwareSourceCode
################################################################################

# Step 1: Show required and recommended fields from recipe

recipe = RecipeParser("recipe_SoftwareSourceCode.yml")
print(recipe.loaded)

# Step 2: Generate a Person (these are Google Helper functions)
from schemaorg.templates.google import ( make_person, make_dataset )

# make_person(name, description, url="", telephone="", email="")
person = make_person(name="@vsoch",
                     description='research software engineer, dinosaur')

# Step 3: Create SoftwareSourceCode

from spython.main.parse.parsers import DockerParser
parser = DockerParser('Dockerfile').parse()

sourceCode = Schema("SoftwareSourceCode")

# sourceCode.properties

sourceCode.add_property('creator', person)
sourceCode.add_property('version', sourceCode.version)
sourceCode.add_property('description', 'A Dockerfile build recipe')
sourceCode.add_property('name', parser.fromHeader)


# Step 4: Validate Data Structure

recipe.validate(sourceCode)

# Step 5a: Add additional fields (extra parsing!)
#         Since this is a demo, we won't do this here (we don't have URI)
#         I'll do a separate example for this using vsoch/dockerfiles on Github

# Step 5b: Generate dataset, meaning writing metadata into template.
#          If we provide an output file it, it would write to it.

dataset = make_dataset(sourceCode)
print(dataset)

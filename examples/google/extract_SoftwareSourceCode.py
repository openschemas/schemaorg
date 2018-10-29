#!/usr/bin/env python

'''
This script will demonstrate how we can extract metadata from a Dockerfile,
and then generate a (html) web template to serve with it so that it is
able to be indexed by Google Datasets (or ideally, similar with the recipe
as a ContainerRecipe).

Author: @vsoch
October 21, 2018

This is a "custom" specification (ContainerRecipe) that is represented in the 
local file, ContainerRecipe.yml. We will review several example parsings
of this file, including specifications already defined in Schema.org 
(e.g., as a SoftwareSourceCode) and ones that should be (e.g., ContainerRecipe).

Since the community is slow to review these changes, for the latter I'll be 
using the local file that is programatically generated.

    Thing > CreativeWork > SoftwareSourceCode > ContainerRecipe

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

from spython.main.parse import DockerRecipe
parser = DockerRecipe("Dockerfile")

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

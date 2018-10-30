#!/usr/bin/env python

'''
This script will demonstrate how we can extract metadata from a Dockerfile,
and then generate a (html) web template to serve with it so that it is
able to be indexed by Google Datasets (or ideally, similar with the recipe
as a ContainerRecipe).

Author: @vsoch
October 31, 2018 Muahahhaa Halloween

This is a "custom" specification (ContainerRecipe) that is represented in the 
local file, ContainerRecipe.yml. It fits into schema.org like this:

    Thing > CreativeWork > SoftwareSourceCode > ContainerRecipe

If you want to see the "only production schema.org" example, see
extract_SoftwareSourceCode.py. If you think this categorization is wrong, 
then please speak up.

 - https://groups.google.com/a/opencontainers.org/forum/#!topic/dev/vEupyIGtvJs
 - https://github.com/schemaorg/schemaorg/issues/2059#issuecomment-427208907

'''

from schemaorg.main.parse import RecipeParser
from schemaorg.main import Schema

################################################################################
## Example 1: Define Dockerfile with SoftwareSourceCode
## Thing > CreativeWork > SoftwareSourceCode
################################################################################

# Step 1: Read in the (custom) yaml file as a custom (under development) Schema

containerRecipe = Schema("ContainerRecipe.yml")

# Step 2: Show required and recommended fields from recipe
# STOPPED HERE - currently writing this recipe :)

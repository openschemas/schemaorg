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

Other suggestions from the OCI Community for fitting names:

    Thing > CreativeWork > SoftwareSourceCode > BuildDefinition
    Thing > CreativeWork > SoftwareSourceCode > BuildInstructions
    Thing > CreativeWork > SoftwareSourceCode > BuildPlan
    Thing > CreativeWork > SoftwareSourceCode > BuildRecipe
    Thing > CreativeWork > SoftwareSourceCode > Configuration
    Thing > CreativeWork > SoftwareSourceCode > ContainerConfig
    Thing > CreativeWork > SoftwareSourceCode > ImageDefinition

If you want to see the "only production schema.org" example, see
extract_SoftwareSourceCode.py. If you think this categorization is wrong, 
then please speak up! I'll be updating the list here (and the examples that
follow) based on the community feedback. Thanks!

 - https://groups.google.com/a/opencontainers.org/forum/#!topic/dev/vEupyIGtvJs
 - https://github.com/schemaorg/schemaorg/issues/2059#issuecomment-427208907

'''

from schemaorg.main.parse import RecipeParser
from schemaorg.main import Schema

################################################################################
## Example 1: Define Dockerfile with ContainerRecipe
## Thing > CreativeWork > SoftwareSourceCode > ContainerRecipe
################################################################################

# Step 1: Read in the (custom) yaml file as a custom (under development) Schema

containerRecipe = Schema("ContainerRecipe.yml")

# Step 2: Show required and recommended fields from recipe

recipe = RecipeParser("recipe_ContainerRecipe.yml")
print(recipe.loaded)

# Step 3: Extract Container Things! First, the recipe file

from spython.main.parse.parsers import DockerParser
parser = DockerParser('Dockerfile').parse()

# containerRecipe.properties

containerRecipe.add_property('version', containerRecipe.version)
containerRecipe.add_property('labels', parser.labels) # currently lists
containerRecipe.add_property('environment', parser.environ) # currently a list
containerRecipe.add_property('entrypoint', parser.entrypoint)
containerRecipe.add_property('description', 'A Dockerfile build recipe')

# This would be extracted at build --> push time, so we know the uri.
containerRecipe.add_property('name', "toasterlint/storjshare-cli")
containerRecipe.add_property('ContainerImage', parser.fromHeader)


# Step 4: Validate Data Structure

recipe.validate(containerRecipe)

# Step 5, get extra metadata we would get with container-diff!
# Kids don't run command line things from Python at home, it's just bad :)

from schemaorg.utils import run_command
import json

### BELOW should be defined with ContainerImage, as the attributes are from the
# ImageManifest I'm not modeling that here, so we can add them to the example
uri = containerRecipe.properties['name']
response = run_command(['docker', 'pull', uri])    # Pull
response = run_command(['docker', 'inspect', uri]) # Inspect
if response['return_code'] == 0:
    manifest = json.loads(response['message'])[0]
    

# Add more (not required) fields - some of these belon with ContainerImage
containerRecipe.add_property('operatingSystem', manifest['Os']) 
containerRecipe.add_property('softwareVersion', manifest['Id'])  # shasum
containerRecipe.add_property('identifier', manifest['RepoTags']) # tag

# Note to readers - we can parse a ContainerRecipe from a manifest!
# manifest['ContainerConfig'] And it has a name! Hmm.

# Container Diff
response = run_command(["container-diff", "analyze", uri,
                        "--type=pip", "--type=file", "--type=apt", "--type=history",
                        "--json", '--quiet','--verbosity=panic'])

# note that we can also get pip, apt, packages here...
if response['return_code'] == 0:
    layers = json.loads(response['message'])
    for layer in layers:
        if layer['AnalyzeType'] == "File":
            print('Found %s files!' %len(layer['Analysis']))

# Found 12615 files!
# Here we can go to town parsing the guts to label the container meaningfully
# TODO: we need some lamma magic / NLP here to extract software tokens

# Step 6. When above is done, generate json-ld
from schemaorg.templates.google import make_dataset
dataset = make_dataset(containerRecipe)
print(dataset)

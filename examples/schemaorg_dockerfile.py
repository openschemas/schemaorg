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

from schemaorg.main.parse import RecipeParser

# Step 1. Read in the recipe to know what we need

recipe = "Recipe-SoftwareSourceCode.yml"
parser = RecipeParser(recipe)


'''
TODO: based on recipe provided, need to programatically create Person and SoftwareSourceCode

shared: {'required': ['description', 'name']}
version: 1
schemas: {'SoftwareSourceCode': {'required': ['citation'], 'recommended': [{'softwareVersion': 'version'}, 'citation', 'identifier', 'keywords', 'license', 'url', 'sameAs', 'spatialCoverage', 'temporalCoverage', 'variableMeasured']}, 'Person|Organization': {'required': ['name']}}

In [5]: parser
Out[5]: [schemaorg-recipe][Recipe-SoftwareSourceCode.yml]

In [6]: parser.loaded
Out[6]: 
{'schemas': {'Person|Organization': {'required': ['name']},
  'SoftwareSourceCode': {'recommended': [{'softwareVersion': 'version'},
    'citation',
    'identifier',
    'keywords',
    'license',
    'url',
    'sameAs',
    'spatialCoverage',
    'temporalCoverage',
    'variableMeasured'],
   'required': ['citation']}},
 'shared': {'required': ['description', 'name']},
 'version': 1}

## A Person

from schemaorg.main import Schema
person = Schema("Person")

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

# Let's do this! We've created a function to (help with) filling in required fields

from schemaorg.main import Schema

person = make_person(name="@vsoch")
dataset = make_dataset("SoftwareSourceCode",
                       creator=person)


def make_person(name, url="", telephone="", email=""):

    # Create an individual (persona)
    person = Schema('Person')
    contactPoint = Schema('ContactPoint')

    contactPoint.properties['telephone']

    # Update the contact point
    contactPoint.add_property('telephone', telephone)
    contactPoint.add_property('email', email)

    # Update the person with it
    person.add_property('contactPoint', contactPoint)
    return person


def make_dataset(schema_type="Dataset",
                 context="http://schema.org",
                 creator=None):

    '''write a dataset. By default, this means a schema.org "Dataset" and we use
       the Dataset.html template. You can substitute any of the input parameters
       to change these variables.
    '''
    # If a creator is given, it must be a Person or Organization
    if creator is not None:
        if creator.label not in ['Organization', 'Person']:
            bot.exit('creator must be an Organization or Person.')

    # These are required and recommended properties
    required_props = ["description", "name"]
    recommended = []
   

    schema_type="SoftwareSourceCode"
    context="http://schema.org"
    spec = Schema(schema_type, base=context)

    metadata = {"@context": context,
                "@type": spec.type}



   # TODO: the rest should be loaded from the spec above
  "name":"NCDC Storm Events Database",
  "description":"Storm Data is provided by the National Weather Service (NWS) and contain statistics on...",
  "url":"https://catalog.data.gov/dataset/ncdc-storm-events-database",
  "sameAs":"https://gis.ncdc.noaa.gov/geoportal/catalog/search/resource/details.page?id=gov.noaa.ncdc:C00510",
  "keywords":[
     "ATMOSPHERE > ATMOSPHERIC PHENOMENA > CYCLONES",
     "ATMOSPHERE > ATMOSPHERIC PHENOMENA > DROUGHT",
     "ATMOSPHERE > ATMOSPHERIC PHENOMENA > FOG",
     "ATMOSPHERE > ATMOSPHERIC PHENOMENA > FREEZE"
  ],
  "creator":{
     "@type":"Organization",
     "url": "https://www.ncei.noaa.gov/",
     "name":"OC/NOAA/NESDIS/NCEI > National Centers for Environmental Information, NESDIS, NOAA, U.S. Department of Commerce",
     "contactPoint":{
        "@type":"ContactPoint",
        "contactType": "customer service",
        "telephone":"+1-828-271-4800",
        "email":"ncei.orders@noaa.gov"
     }
  },
  "includedInDataCatalog":{
     "@type":"DataCatalog",
     "name":"data.gov"
  },
  "distribution":[
     {
        "@type":"DataDownload",
        "encodingFormat":"CSV",
        "contentUrl":"http://www.ncdc.noaa.gov/stormevents/ftp.jsp"
     },
     {
        "@type":"DataDownload",
        "encodingFormat":"XML",
        "contentUrl":"http://gis.ncdc.noaa.gov/all-records/catalog/search/resource/details.page?id=gov.noaa.ncdc:C00510"
     }
  ],
  "temporalCoverage":"1950-01-01/2013-12-18",
  "spatialCoverage":{
     "@type":"Place",
     "geo":{
        "@type":"GeoShape",
        "box":"18.0 -65.0 72.0 172.0"
     }
  }
}





containerRecipe = alternateName
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

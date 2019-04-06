# Schemaorg Python

This is early development of schemaorg Python, and in this document I will detail
the purpose of this Python module.

## Installation

The package is provided [on pip](https://pypi.org/project/schemaorg/) but you can also install from source.

```bash
pip install schemaorg
```
```bash
git clone https://www.github.com/openschemas/schemaorg
cd schemaorg
python setup.py install
```

## Goals

### High Level

The high level goal is to make it easy to tag datasets, containers, and other software to
be accessible via Google Search as a [dataset](https://developers.google.com/search/docs/data-types/dataset)
(or similar as Google develops these search types) or programatically via an API. This means that:

**If I'm a researcher**

 - I can search Google to find datasets or software of interest based on schema.org organization
 - I can use the corresponding search API to find a subset of datasets / software for my research

**If I'm a developer**

 - I can develop tools for my users to find content of a particular type
 - I can iterate over content to computationally derive some optimal environment for a type (see Container example)
 - I can build software that understands the categorization and organization of a particular type


### Specific Goals

The goals for this early development are simple - to define a "Container" in schema.org so that we
can then discover and query the (currently) expansive and disorganized universe of containers. This comes
down to:

**1. Container Definition in Schema.org**

Defining "ContainerRecipe" and "ContainerImage" in schema.org. While imperfect, after discussion with the OCI community I am doing an early proposal:

```
Thing > ContainerImage
Thing > CreativeWork > SoftwareSourceCode > ContainerRecipe
```

I summarize the discussion and rationale [here](https://github.com/openschemas/specifications/pull/9).

**2. Tagging of Dockerfiles as ContainerRecipe**

Next I would want to be able to tag [these Dockerfiles](https://www.github.com/vsoch/dockerfiles)
as ContainerRecipe. Since we don't have this entity added to schema.org yet and I'm impatient to 
wait for meetings, I will give this a first shot and just call them "Datasets" and use
this exercise to develop the codebase here.


## Usage

This is brief usage. For complete examples, see the next section. For this
example, let's prepare metadata for a `SoftwareSourceCode`


### 1. Imports

The recipe defines what the properties are needed for a specific use case. This
might be the minimum set for a registry, for example. The Schema object will
represent the schema itself.

```python
from schemaorg.main.parse import RecipeParser
from schemaorg.main import Schema
```

### 2. The Specification Recipe
First let's read in our recipe.yml file. This file looks like this:

```yaml
version: 1
schemas:
  SoftwareSourceCode:
    recommended:
      - softwareVersion: version
      - citation
      - identifier
      - keywords
      - license
      - url
      - sameAs
      - spatialCoverage
      - temporalCoverage
      - variableMeasured
    required:
      - description
      - name
  Person|Organization:
    required:
      - description
      - name
```

you can see it tells us the required and recommended fields that we need, along with
the actual specification types.

### 3. Read in the Schema
We can first read in our specification. This is production and provided with
the python library.

```python
spec = Schema("SoftwareSourceCode")
Specification base set to http://www.schema.org
Using Version 3.4
Found http://www.schema.org/SoftwareSourceCode
SoftwareSourceCode: found 101 properties
```
It's pretty straight forward - we read in the specification from the library,
it tells us the version, and the number of properties. Now let's read in our
recipe.


### 4. Read in the Recipe

```python
recipe = RecipeParser("recipe.yml")
print(recipe.loaded)
```

Once the recipe is loaded, you can see the properties that are required at "recipe.loaded"
For the entire list of properties that are defined for our SoftwareSourceCode, you
can look at "spec._properties". For those that you've extracted and added, look
at "spec.properties."

### 5. Fill in the Recipe Template

At this point, you want to extract your information from the Dockerfile until
the recipe validates against the schema. To do this, I used the Singularity
Python [Dockerfile parser](https://singularityhub.github.io/singularity-cli/recipes#python-api).

```bash
pip install spython
```
```python
from spython.main.parse import DockerRecipe
parser = DockerRecipe("Dockerfile")
```
Now here is how I add a property. Let's add the obvious ones from the Dockerfile.

```python
spec.add_property('version', containerRecipe.version)
spec.add_property('environment', parser.environ) # currently a list
spec.add_property('entrypoint', parser.entrypoint)
spec.add_property('description', 'A Dockerfile build recipe')
```

This would be extracted at build --> push time, so we know the uri.

```python
spec.add_property('name', "vanessa/sregistry")
spec.add_property('ContainerImage', parser.fromHeader)
```

Depending on where you are doing this (a CI server, your computer, or elsewhere)
this is where you can do interesting things like use Google's container-diff to
get dependencies, or any other kind of parsing of the container guts. The 
metadata that you add here will help with search, so add meaningful things.

### 6: Validate Data Structure
When you are done, validate your specification.

```python
recipe.validate(spec)
```
### 7. Embed in HTML with json-ld

The module includes a simple html template to embed the html and make
a pretty web page to view it. You can change the template argument, or just
use one of the templates provided here.

```python
from schemaorg.templates.google import make_dataset
dataset = make_dataset(spec, "index.html")
print(dataset)
```

For the pretty templates, see the examples folder below.

### 8. Read HTML with json-ld

If you've generated an embedded json-ld, how do you load it again?
You can actually use the BaseParser of the recipe to do this.

```python
result = RecipeParser('SoftwareSourceCode.html')
[schemaorg-recipe][SoftwareSourceCode.html]
```
```
result.loaded
{'@context': 'http://www.schema.org',
 '@type': 'SoftwareSourceCode',
 'about': 'This is a Dockerfile provided by the Dinosaur Dataset collection.',
 'codeRepository': 'https://www.github.com/openschemas/dockerfiles',
 'creator': {'@type': 'Person',
  'contactPoint': {'@type': 'ContactPoint'},
  'name': '@vsoch'},
 'description': 'A Dockerfile build recipe',
 'name': 'deforce/alpine-wxpython:latest',
 'runtime': 'Docker',
 'sameAs': 'ImageDefinition',
 'schemas': {},
 'thumbnailUrl': 'https://vsoch.github.io/datasets/assets/img/avocado.png',
 'version': '3.4'}
```

If there is interest, we could easily add to the library to look at the type,
and the version, and load the initial schema with it. Please open an issue if 
this would be useful to you!

## Examples

 - [openbases/extractor-dockerfile](https://www.github.com/openbases/extractor-dockerfile) is an minimal example showing how to extract metadata for a Dockerfile, for each of a containerRecipe and SoftwareSourceCode.
 - [Zenodo-ml](https://vsoch.github.io/zenodo-ml/) is an example of using the default template (google/dataset-visual.html) to render metadata about a dataset.

# Schemaorg Example Parser

This is an example of using schema.org to label a Dockerfile, and a Singularity Recipe.
Note that updated examples are kept separately in [openbases/extract-dockerfile](https://www.github.com/openbases/extract-dockerfile). Specifically, we are following the Google Dataset guidelines, but pretending that they
encompass a SoftwareSourceCode (e.g., a container recipe such as a Docker or Singularity
recipe file). The example is shown in [extract_SoftwareSourceCode.py](extract_SoftwareSourceCode.py)
and files included here are described in more detail below. Before running
these examples, make sure you have installed the module.

```bash
pip install schemaorg # or
cd ../../ && python setup.py install
```

## What are the files in this folder?

### Dockerfile
The [Dockerfile](Dockerfile) is of course the recipe that I want to describe with schema.org,
and the base file that we use for the following simple examples. My goal is to generate a 
schema.org metadata specification to describe it that I could serve alongside the file 
in some webby place. A search index bot could then index the content to
help users find my container recipe. While it is not represented here, this particular
Dockerfile is for [toasterlint/storjshare-cli](https://hub.docker.com/r/toasterlint/storjshare-cli/).

## recipe_* Files
If I am a provider of a service and want my users to label their data for my service,
I need to tell them how to do this. I do this by way of a recipe file, in this
example folder called [recipe_SoftwareSourceCode.yml](recipe_SoftwareSourceCode.yml). 
This is a simple listing of required fields defined for the entities that are needed
for my "SoftwareSourceCode" (Dockerfile) definition, including SoftwareSourceCode
and an Organization or Person. This recipe is used to help guide the extractor (e.g.,
I know this schema.org specification has 121 properties, here are the small number I
require and recommend for my tool) and also to validate what fields are finally extracted.

## How does it work?

You can look at any of the example files to get a gist. Generally we:

 - Read in a specific version of the *schemaorg definitions* provided by the library
 - Read in a *recipe* for a template that we want to populate (e.g., google/dataset)
 - Use helper functions provided by the template (or our own) to *extract*
 - Extract, *validate*, and generate the final dataset

The goal of the software is to provide enough structure to help the user (typically a developer)
but not so much as to be annoying to use generally. The examples below print (flattened)
with the tool, and are printed pretty for display here.

## Example 1: SoftwareSourceCode from a Dockerfile

Here we can parse a minimal schema.org SoftwareSourceCode from the Dockerfile here:

```bash
python extract_SoftwareSourceCode.py
```
There is verbose output to the screen about versions and what is going on, but the
resulting data structure is printed last:

```html
<script type="application/ld+json">
{
   "creator":{
      "name":"@vsoch",
      "@type":"Person"
   },
   "version":"3.4",
   "description":"A Dockerfile build recipe",
   "name":"gliderlabs/alpine:3.4",
   "@context":"http://www.schema.org"
}
</script>
```

The information here is minimal as the example is. The idea is that some version of
this metadata to describe the Dockerfile would be included with a webby place that
serves the recipe file.

## Example 2: ContainerRecipe from a Dockerfile

This second example is for a specification that is not production, primarily because
it takes forever and a half to develop a standard. Ain't nobody got time for that.
Thus, the (not production) [ContainerRecipe](https://openschemas.github.io/specifications/ContainerRecipe/)
specification is the following:

```bash
Thing > CreativeWork > SoftwareSourceCode > ContainerRecipe
```

Instead of being fully represented in the library here, is represented with the [ContainerRecipe.yml](ContainerRecipe.yml) file here that was obtained from [here](https://raw.githubusercontent.com/openschemas/spec-container/gh-pages/_yaml/ContainerRecipe.yml).

```bash
wget https://raw.githubusercontent.com/openschemas/spec-container/gh-pages/_yaml/ContainerRecipe.yml
```

The example is similar to the first, but also includes properties that are defined here
that are more specific to a Container Recipe. This would be my preference for the fields to 
capture for such an object. See the script [extract_ContainerRecipe.py] as an example.

```bash
python extract_ContainerRecipe.py
```
```html
<script type="application/ld+json">
{
   "labels":[
      [
         "MAINTAINER",
         "toasterlint \"henry@toasterlint.com"
      ]
   ],
   "environment":[
      "USE_HOSTNAME_SUFFIX=FALSE",
      "DATADIR=/storj",
      "WALLET_ADDRESS=",
      "SHARE_SIZE=1TB",
      "RPCADDRESS=0.0.0.0",
      "RPCPORT=4000"
   ],
   "entrypoint":[
      "[\"/entrypoint\"]"
   ],
   "description":"A Dockerfile build recipe",
   "name":"toasterlint/storjshare-cli",
   "ContainerImage":"gliderlabs/alpine:3.4",
   "operatingSystem":"linux",
   "softwareVersion":"sha256:04ce81ba384870f84ccb5abf8a76a926055f6f781fa82729f810878ec59919fa",
   "identifier":[
      "toasterlint/storjshare-cli:latest"
   ],
   "@context":"http://www.schema.org"
}
</script>
```

The above is missing the most important part - tags based on the software found with
container-diff! We can use container-diff to extract this metadata too, and add a list
to the extraction for software dependencies.

See the [extractors](https://github.com/openschemas/extractors) repository for more examples.

# Schemaorg Example Parser

This is an example of using schema.org to label a Dockerfile, and a Singularity Recipe.
Specifically, we are following the Google Dataset guidelines, but pretending that they
encompass a SoftwareSourceCode (e.g., a container recipe such as a Docker or Singularity
recipe file). The example is shown in [schemaorg_dataset.py](schemaorg_dataset.py)
and files included here are described in more detail below.

## Dockerfile
The Dockerfile is of course the recipe that I want to describe with schema.org. Specificlally,
my goal is to generate a schema.org metadata specification to describe it that I could serve
alongside the file in some webby place. A search index bot could then index the content to
help users find my container recipe.

## Schemaorg Python Recipes
If I am a provider of a service and want my users to label their data for my service,
I need to tell them how to do this. I do this by way of a recipe file, in this
example folder called [Recipe-SoftwareSourceCode.yml](Recipe-SoftwareSourceCode.yml). 
This is a simple listing of required fields defined for the entities that are needed
for my "SoftwareSourceCode" (Dockerfile) definition, including SoftwareSourceCode
and an Organization or Person.

**still being written**

## ContainerRecipe
To do this, we use a (not production) [ContainerRecipe](https://openschemas.github.io/specifications/ContainerRecipe/) specification, represented with the [ContainerRecipe.yml](ContainerRecipe.yml) file here that was obtained from [here](https://raw.githubusercontent.com/openschemas/spec-container/gh-pages/_yaml/ContainerRecipe.yml).

```bash
wget https://raw.githubusercontent.com/openschemas/spec-container/gh-pages/_yaml/ContainerRecipe.yml
```

Yaml is annoying and a tabular (column based) file would be more appropriate for this
case, and since we don't need to make inferences over a graph but just do labels,
this will be considered for some future use.


# Schemaorg Python

This is early development of schemaorg Python, and in this document I will detail
the purpose of this Python module.

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


## Examples

 - [openbases/extractor-dockerfile](https://www.github.com/openbases/extractor-dockerfile) is an minimal example showing how to extract metadata for a Dockerfile, for each of a containerRecipe and SoftwareSourceCode.

## Challenges

### Documentation

The software, and contribution instructions, are not well defined and I'm having 
a very hard time engaging with both schema.org and the OCI community to do this.
All I can do is my best effort, and working with minimal guidance and much uncertainty.

### Tools

Along with documentation, there are no easy to use, and nice tools for developing standards.
The steps of exporting from Google Drive, then editing (for testing) and manually discussing
are incredibly burdensome to do once, let alone multiple times to make changes.

# schemaorg Python

This module will serve functions for researchers and users to apply schema.org
definitions to their datasets, software, and other worldly things. For 
development functions with Python along with the web interface that
serves the published specifications, please see [https://www.github.com/schemaorg/schemaorg](https://www.github.com/schemaorg/schemaorg).

## What is this not?

This library is not intended to provide advanced functions around querying the ontology,
but rather accessing the definitions and tagging content with them.

## What is this for?

Please reference the [development](https://openschemas.github.io/schemaorg/) documentation
to read about the intended use cases that we are working on.

## Organization

Generally, we are extracting metadata from datasets and software, and then shoving
that metadata into a specification from schema.org. The final thing that we produce
is likely to be some form of json (e.g., json-ld) that can be embedded in a web 
page or similar, intended to power search.  Since the specific needs of a particular
webby place may vary, along with a data type we are extracting, the module provides
"templates" in the [templates](schemaorg/templates) directory. Specifically:

 - The subfolders represent different use cases. For example, [templates/google](schemaorg/templates/google) has a simple html template, and a requirements file (called a recipe) to produce a Dataset and SoftwareSourceCode.
 - Each subfolder, in an optional `__init__.py` file, also contains helper functions toward this goal. For example, the same google subfolder has such a file with a `make_person` function that users can quickly use to generate a person object.
 - For each corresponding subfolder, there is generally an example in the [examples](examples) folder that also helps to see how it works.

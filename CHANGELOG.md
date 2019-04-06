# Changelog

This is a manually generated log to track changes to the repository for each release. 
Each section should include general headers such as **Implemented enhancements** 
and **Merged pull requests**. All closed issued and bug fixes should be 
represented by the pull requests that fixed them.
Critical items to know are:

 - renamed commands
 - deprecated / removed commands
 - changed defaults
 - backward incompatible changes
 - migration guidance
 - changed behaviour

versions here coincide with releases on pypi.

## [master](https://github.com/openschemas/schemaorg/tree/master)
 - Added additional templates for rendering into tables (0.0.20)
 - Forgot to add url to the ContactPoint in function to create person! (0.0.19)
 - ensuring that a Google Dataset contact_type is defined, and that empty lists / tuples are not added to Datasets (0.0.18)
 - Schema input should not check if the provided string exists, but is directory [issue](https://github.com/openschemas/schemaorg/issues/14) (0.0.17)
 - RecipeParser needs to honor verbosity level (and be quiet) (0.0.16)
 - added parser for json-ld embedded in html (0.0.15)
 - adding visual catalog template (0.0.14)
 - required/recommended should not be required for a recipe! [issue](https://github.com/openschemas/schemaorg/issues/6) (0.0.13)
 - missing top level of type to close [this issue](https://github.com/openschemas/schemaorg/issues/4) (0.0.12)
 - addition of main modules, and templates (0.0.11)
 - package registration (still under development) (0.0.1)

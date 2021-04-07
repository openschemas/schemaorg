__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2018-2021, Vanessa Sochat"
__license__ = "MPL 2.0"

from schemaorg.logger import bot

def validate(schema, recipe):
    '''validate a schema, meaning checking that it includes all properties
       required by the recipe.

       Parameters
       ==========
       schema: the loaded schema, of class schemaorg.main.Schema
       loaded: the loaded recipe, rschemaorg.main.parse.RecipeParser.loaded
    '''
    # Is the yaml formatted correctly?
    if not "schemas" in recipe.loaded:
        bot.error('Missing "schemas" as key in recipe file.')
        return False

    # What is the recipe type?
    bot.info('Looking for primary schema %s definition' % schema.type)
    if not schema.type in recipe.loaded['schemas']:
        bot.error('Missing main schema under recipe["schemas"]')
        return False

    # Required properties for main schema
    if "required" not in recipe.loaded['schemas'][schema.type]:
        bot.debug('This recipe has no required attributes.')
        return True

    bot.debug('Looking for required relations for %s' % schema.type)
    for prop in recipe.loaded['schemas'][schema.type]['required']:

        # If it's not a property, it might be a subclass
        if prop not in schema.properties:

            if "|" in prop:
                options = prop.split('|')
                bot.info('Looking for one of %s' % ' or '.join(options)) 
                has_class = False

                # Do we have the subclass?
                for value in schema.properties.values():
                     if isinstance(value, 'schemaorg.main.Schema'):
                        if value.type in options:
                            has_class = True
                            break

                if not has_class:
                    options = ' or '.join(options)
                    bot.error('Schema %s is missing one of %s' % options)
                    return False
        
                # If we have the type, recursively validate it too
                if not validate(value, recipe):
                    return False
 
            # Otherwise, it's a missing property for the schema!
            else:    
                bot.error('Missing required property %s' % prop)
                return False

    return True

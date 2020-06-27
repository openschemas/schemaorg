# Sports Event

In this example, we are going to walk through creating a [SportsEvent](https://schema.org/SportsEvent) and then validating it. First, let's install the library if you haven't
yet. You can do either:

```bash
pip install schemaorg
```
or
```bash
git clone https://www.github.com/openschemas/schemaorg
cd schemaorg
python setup.py install
```

For this example we are using schemaorg version 0.0.24.

## 1. Define your Criteria

To validate any schema, you have to decide what attributes are required and optional,
which might be different between use cases. Let's write this file, [recipe.yml](recipe.yml)
for attributes that we want required and optional for our SportsEvent. Also note that
since a SportsEvent includes properties that are of type `Person` and `SportsEvent` we include
those too in our recipe.

```yaml
version: 1
schemas:
  SportsEvent:
    recommended:
      - inLanguage
      - isAccessibleForFree
      - location
      - maximumAttendeeCapacity
      - url
    required:
      - description
      - name
      - competitor
      - homeTeam
      - awayTeam
  SportsTeam:
     required:
      - athlete
      - coach
  Person:
    required:
      - description
      - name
```

## 2. Load Recipe and Schema

Next we want to load in the recipe, create an empty schema, and validate it.
Load needed modules:

```python
from schemaorg.main.parse import RecipeParser
from schemaorg.main import Schema
```

And then create an empty SportsEvent
```python
schema = Schema("SportsEvent")
Specification base set to http://www.schema.org
Using Version 7.03
Found http://www.schema.org/SportsEvent
SportsEvent: found 50 properties
```

Load in the recipe:
```python
recipe = RecipeParser("recipe.yml")
print(recipe.loaded)
{'version': 1,
 'schemas': {'SportsEvent': {'recommended': ['inLanguage',
    'isAccessibleForFree',
    'location',
    'maximumAttendeeCapacity',
    'url'],
   'required': ['description', 'name', 'competitor', 'homeTeam', 'awayTeam']},
  'SportsTeam': {'required': ['athlete', 'coach']},
  'Person': {'required': ['description', 'name']}}}
```

Confirm that an empty schema is not valid!

```python
recipe.validate(schema)
Looking for primary schema SportsEvent definition
ERROR Missing required property description
Out[5]: False
```

## 3. Add properties

We need to add properties to the schema so it will validate! As we showed above,
we need t define minimally:

 - name
 - competitor
 - homeTeam
 - awayTeam

And the competitor homeTeam, and awayTeam should all be of type People or SportsTeam
( we can learn this by looking at the properties on [schema.org](https://schema.org/SportsEvent). We can do the easy ones first - these can just be text strings.

```python
schema.add_property("name", "Dinosaur Bowl")
schema.add_property("description", "a bowling event between champions")
```

Take a look at the json-ld:

```
schema.dump_json()                                                      
'{"name": "Dinosaur Bowl", "description": "a bowling event between champions", "@context": "http://www.schema.org", "@type": "SportsEvent"}'
```

Now let's define our homeTeam, awayTeam, and competitor (that will be the awayTeam again).
Since we are dealing with bowling, we are going to use People instead of SportsTeam for the home
and away teams!

```python
homeTeam = Schema('Person')
homeTeam.add_property("name", "Dinosaur Pancakes")
homeTeam.add_property("description", "the leading champion")

awayTeam = Schema('Person')
awayTeam.add_property("name", "Birdie Bananas")
awayTeam.add_property("description", "not the leading champion")
```

Add them to our sports event!

```python
schema.add_property("awayTeam", awayTeam)
schema.add_property("homeTeam", homeTeam)
```

Just for a sanity check, we know that we still need to define the competitor,
but we want to ensure that it won't validate yet.

```python
recipe.validate(schema)
Looking for primary schema SportsEvent definition
ERROR Missing required property competitor
Out[14]: False
```

Let's finally add the competitor

```python
schema.add_property("competitor", awayTeam)
```

And now it's valid!

```python
In [29]: recipe.validate(schema)                                                
Looking for primary schema SportsEvent definition
Out[29]: True
```

We could of course export it to json (you would write this to file)

```python
print(schema.dump_json())                                              
{"name": "Dinosaur Bowl", "description": "a bowling event between champions", "awayTeam": {"name": "Birdie Bananas", "description": "not the leading champion", "@type": "Person"}, "homeTeam": {"name": "Dinosaur Pancakes", "description": "the leading champion", "@type": "Person"}, "competitor": {"name": "Birdie Bananas", "description": "not the leading champion", "@type": "Person"}, "@context": "http://www.schema.org", "@type": "SportsEvent"}
```

You can also get a flattened version:

```python
schema.get_flattened()                                                 
Out[31]: 
{'SportsEvent.name': 'Dinosaur Bowl',
 'SportsEvent.description': 'a bowling event between champions',
 'SportsEvent.awayTeam.Person.name': 'Birdie Bananas',
 'SportsEvent.awayTeam.Person.description': 'not the leading champion',
 'SportsEvent.awayTeam@type': 'Person',
 'SportsEvent.homeTeam.Person.name': 'Dinosaur Pancakes',
 'SportsEvent.homeTeam.Person.description': 'the leading champion',
 'SportsEvent.homeTeam@type': 'Person',
 'SportsEvent.competitor.Person.name': 'Birdie Bananas',
 'SportsEvent.competitor.Person.description': 'not the leading champion',
 'SportsEvent.competitor@type': 'Person',
 '@context': 'http://www.schema.org',
 '@type': 'SportsEvent'}
```

You can export a json-ld embedded html template too:

```python
from schemaorg.templates.google import make_dataset
dataset = make_dataset(schema, "index.html")
print(dataset)
```
see [index.html](index.html) for the export. And then of course if you already
had a web page, you could load it:

```python
result = RecipeParser('index.html')
[schemaorg-recipe][index.html]
result.loaded
{'name': 'Dinosaur Bowl',
 'description': 'a bowling event between champions',
 'awayTeam': {'name': 'Birdie Bananas',
  'description': 'not the leading champion',
  '@type': 'Person'},
 'homeTeam': {'name': 'Dinosaur Pancakes',
  'description': 'the leading champion',
  '@type': 'Person'},
 'competitor': {'name': 'Birdie Bananas',
  'description': 'not the leading champion',
  '@type': 'Person'},
 '@context': 'http://www.schema.org',
 '@type': 'SportsEvent',
 'schemas': {}}
```

Keep in mind that different versions of schema.org might vary from what you
see in the web interface. You can look in the [data/releases](https://github.com/openschemas/schemaorg/tree/master/schemaorg/data/releases) folder for raw files describing the entities,
or inspect a particular schema that you've loaded by looking at it's:

```python
schema._properties
{'about': OrderedDict([('id', 'http://schema.org/about'),
              ('label', 'about'),
              ('comment', 'The subject matter of the content.'),
              ('subPropertyOf', ''),
              ('equivalentProperty', ''),
              ('subproperties', 'http://schema.org/mainEntity'),
              ('domainIncludes',
               'http://schema.org/CommunicateAction, http://schema.org/CreativeWork, http://schema.org/Event'),
...
              ('subPropertyOf', 'http://schema.org/workFeatured'),
              ('equivalentProperty', ''),
              ('subproperties', ''),
              ('domainIncludes', 'http://schema.org/Event'),
              ('rangeIncludes', 'http://schema.org/CreativeWork'),
              ('inverseOf', ''),
              ('supersedes', ''),
              ('supersededBy', ''),
              ('isPartOf', None)])}
```

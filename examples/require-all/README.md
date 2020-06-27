# Require All

In this example, we are going to walk through creating a recipe for a [SportsEvent](https://schema.org/SportsEvent) that requires all fields. First, install schemaorg:

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

## 1. Create your Schema

Let's start with an "empty" recipe, [empty.yml](empty.yml)


```yaml
version: 1
schemas:
  SportsEvent:
    recommended:
    required:
```

and load into Python

```python
from schemaorg.utils import read_yaml, write_yaml
recipe = read_yaml('empty.yml')
```

## 2. Get Properties

At this point, we need to get all the properties for a SportEvent.

```python
from schemaorg.main import Schema
schema = Schema("SportsEvent")
```

And add them to our recipe. As we go, we will keep track of other types to add.

```python
toadd = set()
for name, meta in schema._properties.items():
    recipe['schemas']['SportsEvent']['required'].append(name)
    related = [x.strip() for x in meta.get('domainIncludes', '').split(',')]
    [toadd.add(x) for x in related];
```

At this point our schema just has the top level properties, we don't make any requirement
on the nested classes (e.g., Event, Service, Schedule, etc). This simple recipe would
still require these fields to be defined, but wouldn't validate them.

```python
write_yaml(recipe, 'minimal.yml')
```

You can see this recipe under [minimal.yml](minimal.yml). Note that we have 47 other
types that also have properties that need to be defined.

```python
len(toadd)
47
```

## 3. Get Nested Types and Properties

At this point you could do the same for all the other types that are required. This
is where the recipe can really blow up. We are again going to save another
list for the classes required for that:

```python
anotherset = set()
for schema_name in toadd:
    schema_name = schema_name.split('/')[-1]
    if schema_name not in recipe['schemas']:
        try:
            recipe['schemas'][schema_name] = {"required": []}
            new_schema = Schema(schema_name)
            for name, meta in new_schema._properties.items():
                recipe['schemas'][schema_name]['required'].append(name)
                related = [x.strip() for x in meta.get('domainIncludes', '').split(',')]
                [anotherset.add(x) for x in related];
        except:
            pass
```

Since we haven't loaded extensions, we use a try / except to handle that.
You can see how this is getting messy. Let's save the output anyway.

```python
write_yaml(recipe, 'bloated.yml')
```

I hope that you see that it's a much better strategy to clearly define a
set of entity types and required / optional properties for each. It's hugely
unlikely that you would want to require *every* single one.

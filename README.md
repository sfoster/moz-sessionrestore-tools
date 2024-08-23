# moz-sessionrestore-tools
Tools and prototypes for working with firefox session restore files

## `mozlz4json.py`

Builds on [mozlz4a.py, by Tilman Blumenbach](https://gist.github.com/kaefer3000/73febe1eec898cd50ce4de1af79a332a) to add a couple of options so you can pretty-print the json output when decompressing. 

Usage:

```
# decompress a session restore file
python3 mozlz4a.py -d --pretty ./previous.jsonlz4 output.json

# re-compress a session restore JSON document, ready to copy to a firefox profile directory
python3 mozlz4a.py -d --pretty ./previous.json sessionstore.jsonlz4

# NB: output is to stdout unless you provide the output argument, so you can redirect to a file or whatever
```

## `validate.py`

Validate a de-compressed session restore file against a JSON Schema

Usage:

```
# Using the default schema, which is provided alongside validate.py as session-schema.json
python3 validate.py ./previous.json

# Using a different schema file
python3 validate.py ./previous.json --schema some-schema.json

```


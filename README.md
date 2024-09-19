# moz-sessionrestore-tools
Tools and prototypes for working with Firefox session restore files

## `mozlz4json.py`

Based on mozlz4a.py, which is copyright Tilman Blumenbach and *not* covered by the MIT license. I built on [this gist](https://gist.github.com/kaefer3000/73febe1eec898cd50ce4de1af79a332a), but what looks like the same file is also housed at https://github.com/baillow/mozlz4, where it is given what looks like BSD-2 license. My fork adds a couple of options so you can pretty-print the json output when decompressing. 

Session restore files are created in your Firefox profile directory. You'll want to enable `Open previous windows and tabs` in about:preferences. The primary restore file is `sessionstore.jsonlz4`, and we take snapshots for backup/rollback in the `sessionstore-backups/` sub-directory. 

**Note: this requires the lz4 package which you can install with `pip3 install lz4`**

#### Usage:

```
# To decompress a session restore file
python3 mozlz4json.py -d --pretty ./previous.jsonlz4 output.json

# To re-compress a session restore JSON document, ready to copy to a firefox profile directory
python3 mozlz4json.py -d --pretty ./previous.json sessionstore.jsonlz4

# NB: output is to stdout unless you provide the output argument, so you can redirect to a file or whatever
```

## `validate.py`

Validate a session restore file against a JSON Schema.

**You must decompress the session file to "normal" JSON before validating it.**

#### Usage:

```
# Using the default schema, which is provided alongside validate.py as session-schema.json
python3 validate.py ./previous.json

# Using a different schema file
python3 validate.py ./previous.json --schema some-schema.json

```


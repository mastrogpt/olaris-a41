## Synopsis

```text
Usage:
  text csvimp <file> [<field>] [--meta=<metafield>] [<substring>] [--collection=<collection>] [--group=<count>]
```

This command requires:

```
<file> is a CSV File
<field> is the field number o name to import
<substring> filter the fields with it
<collection> is a collection name, in format `name[:size]` (size defaults to 4096)
<count> number of fields to be grouped
```
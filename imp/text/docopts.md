## Synopsis

```text
Usage:
  text csv <filecsv> [<field>] [<substring>] [--meta=<metafield>]  [--collection=<collection>] [--group=<count>]
  text dir <dir> [<substring>] [--collection=<collection>] [--group=<count>] [--filter=<action>]
```

This command requires:

```
<filecsv> is a CSV File
<dir> is a directory
<field> is the field number o name to import
<metafield> is the field number o name to use as metadata
<substring> filter the fields with it
<collection> is a collection name, in format `name[:size]` (size defaults to 4096)
<count> number of fields to be grouped
<action> to invoke to filter the importent content - receive {"text","meta", "embed"} returns{ "text","meta", "embed"}
```
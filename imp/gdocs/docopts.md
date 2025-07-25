## Synopsis

```text
Usage:
  gdocs list <folder> [<substring>]
  gdocs parse <document> [<file>]
  gdocs import <folder> [<substring>] [--process=<action>] [--collection=<collection>] [--save=<dir>]
```

This command requires:
- create a service account on Google with access to Google Docs and Google Drive APISs
- put the json credentials in .google.json
- assign the folder to the service account pseudo-email (listed in the .json)

```text
<folder> is a GDocs folder url
<document> is GDocs document url
<collection> is a collection name, in format `name[:size]` (size defaults to 4096)
<substring> of the name to select
<dir> is a local directory where to save data
```
import os, sys
import csv
from pathlib import Path
from common import create_collection, post_text, post_text_append, post_text_flush

ACTION = "mastrogpt/loader"

def main(argv):
    """
    Parse Document
    """

    [FILE, FIELD, META, SUBSTRING, COLLECTION, GROUP] = argv
    print(FILE, FIELD, META, COLLECTION, SUBSTRING, GROUP)

    if COLLECTION !="":
        print(f"Creating collection {COLLECTION}")
        create_collection(ACTION, COLLECTION)
        # remove the size from the collection name once created
        COLLECTION = COLLECTION.split(":")[0]
    
    # read csv file
    maxlen = 0
    count = 0
    group = 1
    try: 
        group = int(GROUP or "1")
    except:
        group = 1

    print(f"Grouping: {group}")

    os.chdir(os.environ.get("OPS_PWD", "."))
    with open(FILE, "r") as f:
        reader = csv.reader(f)
        fields = next(reader)
        skipped = 0

        nfield = -1
        try:
            nfield = int(FIELD or "-1")
        except:
            nfield = fields.index(FIELD)

        mfield = -1
        try:
            mfield = int(META or "-1")
        except:
            mfield = fields.index(META)

        if nfield == -1:
            print("Please select either the field number or the field name")
            print(f"Fields (0-{len(fields)}): ", fields)
            sys.exit(0)

        for row in reader:
            text = row[nfield]    
            meta = row[mfield] if mfield > -1 else None

            if not SUBSTRING in text:
                skipped += 1
                continue

            count += 1
            maxlen = max(maxlen, len(text))

            if COLLECTION !="":
                if group > 1:
                    post_text_append(text, meta, COLLECTION, ACTION, group)
                else:
                    post_text(text, meta, COLLECTION, ACTION)
            else:
                if meta:
                    print(meta, text)
                else:
                    print(text)

        post_text_flush(COLLECTION, ACTION)

    print("--------------------------------")
    print(f"Total: {count} Skipped: {skipped}")
    print(f"Max Length: {maxlen}")
    print(f"Field: #{nfield} {fields[nfield]}")
    if mfield != -1:
        print(f"Meta: #{mfield} {fields[mfield]}")
    print("--------------------------------")
    
        

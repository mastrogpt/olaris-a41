import os, sys
import csv
from pathlib import Path
from common import create_collection, post_text, post_text_append, post_text_flush

ACTION = "mastrogpt/loader"

def main(argv):
    """
    Parse Document
    """

    [DIR, SUBSTRING, COLLECTION, GROUP, FILTER] = argv
    print(DIR, SUBSTRING, COLLECTION, GROUP, FILTER)

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
        print(f"Grouping by {group}")
    except:
        group = 1


    os.chdir(os.environ.get("OPS_PWD", "."))

    # list files in directory
    maxlen = 0
    count = 0
    skipped = 0
    files = os.listdir(DIR)
    for file in files:
        if not SUBSTRING in file:
            skipped += 1
            continue

        count += 1
        text = Path(os.path.join(DIR, file)).read_text()
        meta = file
        maxlen = max(maxlen, len(text))

        if COLLECTION !="":
            if group > 1:
                post_text_append(text, meta, COLLECTION, ACTION, group)
            else:
                print(f"Posting with {FILTER}")
                post_text(text, ACTION, meta, COLLECTION, filter=FILTER)
        else:
            if meta:
                print(meta, text)
            else:
                print(text)

        post_text_flush(COLLECTION, ACTION)

    print("--------------------------------")
    print(f"Total: {count} Skipped: {skipped}")
    print(f"Max Length: {maxlen}")
    print("--------------------------------")
    
        

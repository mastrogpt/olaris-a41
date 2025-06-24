import gdocs.list
import gdocs.parse
from pathlib import Path
from common import create_collection, post_text
import os, json

ACTION = "mastrogpt/loader"

def main(argv):
    """
    Parse Document
    """
    [FOLDER, JSON, COLLECTION, SUBSTRING] = argv
    print(FOLDER, JSON, COLLECTION, SUBSTRING)

    os.chdir(os.environ.get("OPS_PWD", "."))

    if COLLECTION !="":
        print(f"Creating collection {COLLECTION}")
        create_collection(ACTION, COLLECTION)
        # remove the size from the collection name once created
        COLLECTION = COLLECTION.split(":")[0]
    
    result = gdocs.list.list_folder(FOLDER)
    
    maxlen = 0
    count = 0
    dids = []

    json_data = {}

    for file in result.get("files", []):
        did = file.get("id")
        dids.append(did)
        name = file.get("name")
        if not SUBSTRING in name:
            print("skipping", name)
            continue
        if did:
            count += 1
            try:
                name, text = gdocs.parse.parse_doc(did)
            except Exception as e:
                print(f"Error parsing {did}: {e}")
                continue
            
            if len(text) > maxlen:
                maxlen = len(text)

            if COLLECTION !="":
                post_text(text, file.get("name", "unknown"), COLLECTION,  ACTION)
            elif JSON !="":
                json_data[name] = text
                with open(JSON, "w") as f:
                    f.write(json.dumps(json_data, indent=2))
            else:
                print(text)

    print("--------------------------------")
    print(f"Total: {count}")
    print(f"Max Length: {maxlen}")
    print("--------------------------------")
    

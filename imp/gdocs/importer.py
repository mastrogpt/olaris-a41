import gdocs.list
import gdocs.parse
from pathlib import Path
from common import create_collection, post_text

ACTION = "mastrogpt/loader"


def main(argv):
    """
    Parse Document
    """
    [FOLDER, COLLECTION, SUBSTRING] = argv
    print(FOLDER, COLLECTION, SUBSTRING)

    if COLLECTION !="":
        print(f"Creating collection {COLLECTION}")
        create_collection(ACTION, COLLECTION)
        # remove the size from the collection name once created
        COLLECTION = COLLECTION.split(":")[0]
    
    result = gdocs.list.list_folder(FOLDER)
    
    maxlen = 0
    count = 0
    dids = []
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
                text = gdocs.parse.parse_doc(did)
            except Exception as e:
                print(f"Error parsing {did}: {e}")
                continue
            
            if len(text) > maxlen:
                maxlen = len(text)

            if COLLECTION !="":
                post_text(text, COLLECTION,  ACTION)
            else:
                print(text)
    
    print("--------------------------------")
    print(f"Total: {count}")
    print(f"Max Length: {maxlen}")
    print("--------------------------------")
    

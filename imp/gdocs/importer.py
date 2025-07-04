import gdocs.list
import gdocs.parse
from pathlib import Path
from common import create_collection, post_text, save_text
import os, json

ACTION = "agent41/loader"

def main(argv):
    """
    Parse Document
    """
    [FOLDER, PROCESS, SAVE, COLLECTION, SUBSTRING] = argv
    print(FOLDER, PROCESS, SAVE, COLLECTION, SUBSTRING)

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

    for file in result.get("files", []):
        did = file.get("id")
        dids.append(did)
        name = file.get("name")
        if not SUBSTRING in name:
            #print("skipping", name)
            continue
        if did:
            count += 1
            try:
                name, text = gdocs.parse.parse_doc(did)
                body  = f"<!-- {name} -->\n{text}\n"
            except Exception as e:
                print(f"Error parsing {did}: {e}")
                continue
            
            if len(text) > maxlen:
                maxlen = len(text)

            if PROCESS != "":
                print(f"Processing {name}")
                text = post_text(text, PROCESS, name)
                if text is None:
                    print(f"Error processing {name}")
                    continue
            
            if SAVE !="":
                #print(text)
                save_text(SAVE, text, name)
         
            if COLLECTION !="":
                res = post_text(text, file.get("name", "unknown"), COLLECTION,  ACTION)
                if res is None:
                    print(f"Error posting {name}")
                    continue

            if SAVE == "" and COLLECTION == "":
                print(text)


    print("--------------------------------")
    print(f"Total: {count}")
    print(f"Max Length: {maxlen}")
    print("--------------------------------")
    

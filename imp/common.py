import sys, os, pathlib
from google.oauth2 import service_account
from googleapiclient.discovery import build


SERVICE_ACCOUNT_FILE =  os.path.join(os.getenv("OPS_PWD"), ".google.json")
SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive'
]

def drive_sv():
    try:
        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        return build('drive', 'v3', credentials=creds)
    except Exception as e:
        print(e)
        return None

def docs_sv():
    try:
        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        return build('docs', 'v1', credentials=creds)
    except Exception as e:
        return None

def get_id(url, type):
    import urllib.parse
    parts = urllib.parse.urlparse(url)
    if type == "folder":
        pref = "/drive/folders/"
    elif type == "doc":
        pref = "/document/d/"
    else:
        return None
    
    if parts.path.startswith(pref):
        split = parts.path.split("/")
        #print(split)
        return split[3]
    else:
        return None

import subprocess, json, tempfile

def create_collection(action, collection):
    cmd = ["ops", "invoke", action, "-p", "input", f"@{collection}"]
    try:
        res = subprocess.run(cmd, check=True, capture_output=True)
    except Exception as e:
        print(f"Failed to create collection {collection}: {e}")
        print(f"Command: {" ".join(cmd)}")
        print(e)
        sys.exit(1)


def save_text(dir, text, name=None):
    base = os.getenv("OPS_PWD") or "."
    os.makedirs(os.path.join(base, dir), exist_ok=True)
    if name is None:
        import hashlib
        hash = hashlib.sha256(text.encode()).hexdigest()[:16]
    else:
        hash = name

    with open(os.path.join(base, dir, hash), "w") as f:
        f.write(text)
    print(f"Saved text to {os.path.join(base, dir, hash)}")

def check_post(collection, text):
    """
    Calculate a hash of the text.
    Open a file collecition.txt, create it if it does not exist, and check if the hash is in the file.
    If it is, return True.
    If it is not, return False and append the hash to the file.
    """
    import hashlib
    hash = hashlib.sha256(text.encode()).hexdigest()
    dir = os.getenv("OPS_PWD") or "."
    filename = os.path.join(dir, f"{collection}.hash")
    try:
        with open(filename, "r") as f:
            if hash in f.read():
                print(f"{hash[:8]} already posted to {collection}.")
                return True
    except FileNotFoundError:
        pass
    
    with open(filename, "a+") as f:
        f.write(hash + "\n")
    
    return False

def post_text(text, action, meta=None, collection=None, sep=None, filter=None):
    msg = {"input": text }
    if collection is not None:
        msg["state"] = collection
        if check_post(collection, text):
            return
    if meta:
        msg["meta"] = meta
    if sep:
        msg["sep"] = sep
    if filter:
        msg["filter"] = filter
        print(msg)

        # a temp file
    res = None
    with tempfile.NamedTemporaryFile(mode='w+', delete=True) as temp_file:
        temp_file.write(json.dumps(msg))
        temp_file.flush() 
        cmd = ["ops", "invoke", action, "-P", temp_file.name ]
        try:
            res = subprocess.run(cmd, check=True, capture_output=True)
        except Exception as e:
            print("Failed to execute:", str(e))
            errors = os.path.join(os.getenv("OPS_PWD", "."), "errors.txt")
            with open(errors, "a") as f:
                # current time
                from datetime import datetime
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"=== {now} [{meta or ""}] {" ".join(cmd)}\n")
                f.write(json.dumps(msg, indent=2))
                print(res)
                #f.write(f"out: {res.stdout.decode('utf-8')}\n")
                #f.write(f"err: {res.stderr.decode('utf-8')}\n")
            return None

    output = res.stdout.decode("utf-8")
    try:
        output = json.dumps(json.loads(output).get("body", {}).get("output", {}))
    except: 
        pass
    return output

text_group = []
meta_group = []

def post_text_append(text, meta, collection, action, group):
    global text_group, meta_group
    text_group.append(text)
    meta_group.append(meta)
    if len(text_group) == group:
        post_text_flush(collection, action)
        text_group = []
        meta_group = []

def post_text_flush(collection, action):
    global text_group, meta_group
    if len(text_group) == 0:
        return
    text = "\n".join(text_group)
    meta = "\n".join(meta_group)
    #print(text)
    #print(meta)
    post_text(text, action, meta, collection, sep="\n")

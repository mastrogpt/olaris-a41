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
    res = subprocess.run(cmd, check=True, capture_output=True)
    print(res.stdout.decode("utf-8"))

def post_text(text, meta, collection, action, sep=None):
    res = None
    try:
        msg = {"input": text, "state": collection }
        if meta:
            msg["meta"] = meta
        if sep:
            msg["sep"] = sep
        # a temp file
        with tempfile.NamedTemporaryFile(mode='w+', delete=True) as temp_file:
            #print(msg)
            temp_file.write(json.dumps(msg))
            temp_file.flush() 
            cmd = ["ops", "invoke", action, "-P", temp_file.name ]
            try:
                res = subprocess.run(cmd, check=True, capture_output=True)
                print(res.stdout.decode("utf-8"))
            except Exception as e:
                print(e)
                print(cmd)
                pathlib.Path("/tmp/latest_parameters.json").write_text(json.dumps(msg, indent=2))
                print("saved in /tmp/latest_parameters.json")
                sys.exit(1)
        try:
            print(json.loads(res.stdout.decode("utf-8")).get("body", {}).get("output", {}))
        except: 
            print(res.stdout.decode("utf-8"))
        return True
    except Exception as e:
        print("\nERROR:", str(e))
        print(cmd)
        if res:
            print(res.stdout)
            print(res.stderr)
        return False
   
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
    post_text(text, meta, collection, action, sep="\n")

PACKAGE="common"

import os
import requests
import traceback
import dotenv
import sys
import signal
from requests.auth import HTTPBasicAuth
from mcp.server.fastmcp import FastMCP
from typing import Dict


def signal_handler(sig, frame):
    """
    Handle system signals to gracefully shut down the server.
    """
    print("Shutting down server...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


# first load wskprops if ani
dotenv.load_dotenv(os.path.expanduser("~/.wskprops"))

# get info from the environment
AUTH = os.getenv("AUTH")
if AUTH is None:
    print("You are not logged in. Please run 'ops ide login' to login.")
    sys.exit(1)

APIHOST = os.getenv("APIHOST")
if APIHOST is None:
    print("please set APIHOST in your environment")
    sys.exit(1)
    
ops_auth = HTTPBasicAuth(AUTH.split(":")[0], AUTH.split(":")[1])

NAMESPACE =  None
try: 
    NAMESPACE = requests.get(f"{APIHOST}/api/v1/namespaces", auth=ops_auth).json()[0]
    #print("Connected to", NAMESPACE)
except: print("error retrieving namespace")

def invoke(package, func, args):
    if NAMESPACE is None:
        return {"error": "please provide credentials for openserverless"}
    url = f"{APIHOST}/api/v1/namespaces/{NAMESPACE}/actions/{package}/{func}?blocking=true"
    try:
        res = requests.post(url, auth=ops_auth, json=args)
        out = res.json().get("response", {}).get("result", {"error": "no response"})
        return out
    except Exception as e:
        traceback.print_exc()
        return { "error": str(e) }

mcp = FastMCP(name=PACKAGE)

@mcp.tool(description="Reverse the input text")
def reverse_local(input: str) -> Dict:
    """
    input is the string to reverse
    """
    return {
        "output": input[::-1]
    }

@mcp.resource("greet_local://{input}", description="return a greeting")
def greet_local(input: str) -> Dict:
    """
    input is the name to greet
    """
    output = input or "world"
    return f"Hello, {output}!"

@mcp.prompt(description="who you are")
def person_local(input: str) -> Dict:
    """
    input is the description of the person
    """
    output = input or "a nice person"
    return f"You are {output}!"

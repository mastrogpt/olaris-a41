import sys
import json
import os
import platform
import shutil
from pathlib import Path

os.chdir(os.getenv("OPS_PWD") or ".")

def list_mcp_packages(actions):
    """
    iterate all the actions and return a list of all the packages where there is at least one action with an annotation starting with mcp:
    """
    mcp_packages = set()
    for action in actions:
        for annotation in action.get("annotations", []):
            if isinstance(annotation, dict) and annotation.get("key", "").startswith("mcp:"):
                namespace = action["namespace"].split("/")[-1]
                #print(f"Found  {annotation} in", namespace, action['name'])
                mcp_packages.add(namespace)
                break
    return mcp_packages


def install_5ire(package, file, uninstall):
    """
    read the file as json, add an entry <package> under mcpServers with
    commnds: ops
    args: a41 mcp run <package>
    save the file
    """

    # Read existing config or create new one
    if Path(file).exists():
        config = json.loads(Path(file).read_text())
    else:
        config = {"servers": []}

    # iterate array config "servers" and remove the one with key == package
    config["servers"] = [s for s in config["servers"] if s.get("key") != package]

    if uninstall:
        print(f"Removing {package}")    
    else:
        print(f"Adding {package} in {file}")    
        config["servers"].append({
            "command": shutil.which("ops"),
            "key": package,
            "args": ["a41", "mcp", "run", package],
            "isActive": True
        })

    # Save updated config
    Path(file).write_text(json.dumps(config, indent=2))

def install_cursor(package, file, uninstall):
    """
    read the file as json, add an entry <package> under mcpServers with
    commnds: ops
    args: a41 mcp run <package>
    save the file
    """

    # Read existing config or create new one
    if Path(file).exists():
        config = json.loads(Path(file).read_text())
    else:
        config = {"mcpServers": {}}

    if uninstall:
        print(f"Uninstalling {package} from {file}")
        del config["mcpServers"][package]
    else:
        config["mcpServers"][package] = {
            "command": "ops",
            "name": package,
            "args": ["a41", "mcp", "run", package],
            "env": {
                "APIHOST": os.getenv("APIHOST") or os.getenv("OPSDEV_APIHOST") or "",
                "AUTH": os.getenv("AUTH") or ""
            }
        }

    # Save updated config
    Path(file).write_text(json.dumps(config, indent=2))


[package, uninstall, cursor, claude, fire, sse] = sys.argv[1:]


import openwhisk
actions = openwhisk.call("actions")
mcp_packages =  list_mcp_packages(actions)

if package == "":
    print("Available packages with MCP actions:")
    for package in sorted(mcp_packages):
        print(f"  {package}")
    sys.exit(0)

if not package in mcp_packages:
    print(f"Package {package} has not mcp action")
    sys.exit(0)

if cursor =="true":
    if not os.path.exists("packages"):
        print("No packages folder found - we expect to find it in the root of the project")
        sys.exit(1)
    config_path = ".cursor/mcp.json"
    print("Installing MCP with Cursor in ", config_path)
    os.makedirs(".cursor", exist_ok=True)
    install_cursor(package, config_path, uninstall=="true")
elif fire == "true":
    system = platform.system()
    if system == 'Windows':
        base_dir = os.getenv('APPDATA') or os.path.join(os.getenv('USERPROFILE') or "", 'AppData', 'Roaming')
        config_path = os.path.join(base_dir, '5ire', 'mcp.json')
    elif system == 'Darwin':  # macOS
        base_dir = os.path.expanduser('~/Library/Application Support/5ire')
        config_path = os.path.join(base_dir, 'mcp.json')
    elif system == 'Linux':
        base_dir = os.path.expanduser('~/.config/5ire')
        config_path = os.path.join(base_dir, 'mcp.json')
    else:
        raise RuntimeError(f'Unsupported OS: {system}')
    print("Installing MCP with 5ire in ", config_path)
    os.makedirs(base_dir, exist_ok=True)
    install_5ire(package, config_path, uninstall=="true")

elif claude == "true":
    print("TODO Installing MCP with Claude")

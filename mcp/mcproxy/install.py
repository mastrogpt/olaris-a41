import sys
import json
import os
from pathlib import Path

os.chdir(os.getenv("OPS_PWD"))

def install(package, file, uninstall):
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
            "args": ["a41", "mcp", "run", package]
        }

    # Save updated config
    Path(file).write_text(json.dumps(config, indent=2))

[package, uninstall, cursor, claude, five] = sys.argv[1:]

if cursor =="true":
    if not os.path.exists("packages"):
        print("No packages folder found - we expect to find it in the root of the project")
        sys.exit(1)
    print("Installing MCP with Cursor")
    os.makedirs(".cursor", exist_ok=True)
    install(package, ".cursor/mcp.json", uninstall=="true")
elif claude == "true":
    print("TODO Installing MCP with Claude")
elif five == "true":
    print("TODO Installing MCP with 5ire")

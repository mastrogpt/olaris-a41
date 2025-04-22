import sys, os
from pathlib import Path

def write_text_or_clean(file, clean, text):
    path = Path(file)
    if clean:
        if path.exists():
            print(f"Cleaning file {file}")
            path.unlink()
        return
    if path.exists():
        print(f"File {file} already exists.")
        return
    print(f"Creating file {file}")
    path.write_text(text)

def main(typ, package, name, description):
    print(f"Type: {typ}")
    print(f"Package: {package}")
    print(f"Name: {name}")
    print(f"Description: {description}")
    
    dir = os.getenv("OPS_PWD")
    if dir:
        os.chdir(dir)
    clean = typ == "clean"

    os.makedirs(f"packages/{package}/{name}", exist_ok=True)
    os.makedirs(f"tests/{package}", exist_ok=True)

    file = Path(f"packages/{package}/{name}/__main__.py")
    write_text_or_clean(file, clean, f"""#--kind python:default
#-a mcp:type {typ}
#-a mcp:desc "{description}"
#-a input:str "the user input (default='')"

import {name}
def main(args):
  return {name}.{name}(args)
""")

    file = f"packages/{package}/{name}/{name}.py"
    write_text_or_clean(file, clean, f"""def {name}(args):
  input = args.get("input", "")
  output = input
  return {{ "output": output }}
""")

    file = Path(f"tests/{package}/test_{name}.py")
    write_text_or_clean(file, clean, f"""import sys
sys.path.append("packages/{package}/{name}")
import {name} as m

def test_{name}():
    args = {{}}
    result = m.{name}(args)
    assert result["output"] == ""
    args = {{"input": "test input"}}
    result = m.{name}(args)
    assert result["output"] == "test input"
""")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: <type> <package> <name> <description>")
        sys.exit(0)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

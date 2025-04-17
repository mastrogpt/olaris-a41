import os, sys, requests
from pathlib import Path

from requests.auth import HTTPBasicAuth
    
APIHOST = os.getenv("OPSDEV_APIHOST")
NAMESPACE = os.getenv("OPSDEV_USERNAME")
AUTH = os.getenv("AUTH")
if AUTH is None:
    print("You are not logged in. Please run 'ops ide login' to login.")
    sys.exit(1) 

ops_auth = HTTPBasicAuth(AUTH.split(":")[0], AUTH.split(":")[1])


def call(cmd, args=None):
    url = f"{APIHOST}/api/v1/namespaces/{NAMESPACE}/{cmd}"
    try:
        if args:
            response = requests.post(url, auth=ops_auth, json=args)
        else:
            response = requests.get(url, auth=ops_auth)
        return response.json()
    except Exception as e:
        print(e)
        return None

def extract_types(actions, package):
    """
    Extract function annotations from actions matching the target namespace and having mcp:type.
    """
    # Initialize result map
    result = {}
    
    # Expected namespace for filtering
    target_namespace = f"{NAMESPACE}/{package}"
    
    # Process each action
    for action in actions:
        # Skip if not in target namespace
        if action['namespace'] != target_namespace:
            continue
            
        # Get annotations
        annotations = action.get('annotations', [])
        
        # Check if this action has mcp:type annotation
        has_mcp_type = any(ann.get('key') == 'mcp:type' for ann in annotations)
        if not has_mcp_type:
            continue
            
        # Get function name
        func_name = action['name']
        
        # Create annotation map for this function
        ann_map = {}
        for ann in annotations:
            key = ann.get('key', '')
            # Include annotations with ':' in the key, but exclude mcp:type
            if ':' in key:
                ann_map[key] = ann.get('value')
                
        # Add to result if we found any matching annotations
        if ann_map:
            result[func_name] = ann_map
    
    return result


COMMON = Path("common.py").read_text()


def generate(types, package):
    """
    Create a folder mcp if it does not exist and generate a file mcp/<package>.py.
    Write the common code to the file then iterate over the keys of the types.
    Look at the values, for each key consider <annotation> as:
    - @mcp.tool if the value is "tool"
    - @mcp.prompt if the value is "prompt" 
    - @mcp.resource(<value>) if the value is "resource" <value> is the value of mcp:resource
    Initialize <docs> with the value of mcp:desc
    Construct as array <args>, <docs>, <vars> by iterating <current> the values of the types[<key>] as follows:
    - exclude anything starting with "mcp:"
    - add to <args> the <current>
    - add to <vars> the <current> without what is after the ":"
    - add to <docs> the <current> " is " + value of <current>
    Then add a "def <key>(<args converted to a comma separated string>)" with the <annotation>
    Finally add <docs> as a docstring to the function, concatenating all the docs with a newline.
    The body should create a message dictionary, assign each of <vars> in a key with the name of the var, then execute a 'invoke(<func>, <message>)
    """
    # Create mcp folder if it doesn't exist
    os.makedirs('_svr', exist_ok=True)
    
    # Generate file path
    filepath = f'_svr/{package}.py'
    
    #f = open(filepath, 'w')
    with open(filepath, 'w') as f:
        # Write common code
        f.write(COMMON.replace("\"common\"", f"\"{package}\""))
        
        # Process each function
        items = list(types.items())
        for key, annotations in items:
            #(key, annotations) = items[0]
            # Get annotation type
            mcp_type = annotations.get('mcp:type')
            
            # Determine decorator
            if mcp_type == 'tool':
                decorator = '@mcp.tool('
            elif mcp_type == 'prompt':
                decorator = '@mcp.prompt('
            elif mcp_type == 'resource':
                resource_value = annotations.get('mcp:resource', '')
                decorator = f'@mcp.resource("{resource_value}",'
            else:
                continue

            description = annotations.get('mcp:desc', '')
                
            # Initialize docs with description
            docs = []
            
            # Build args, vars and docs arrays
            args = []
            vars = []
            for ann_key, ann_value in annotations.items():
                if not ann_key.startswith('mcp:'):
                    args.append(ann_key)
                    var = ann_key.split(':')[0]
                    vars.append(var)
                    docs.append(f"{var} is {ann_value}")
            
            # Write function
            f.write(f'{decorator} description="{description}")\n')
            f.write(f'def {key}({",".join(args)}) -> Dict:\n')
            f.write('    """\n')
            f.write('    ' + '\n    '.join(docs) + '\n')
            f.write('    """\n')
            f.write('    message = {}\n')
            for arg, var in zip(args, vars):
                f.write(f'    message["{var}"] = {var}\n')
            f.write(f'    return invoke(PACKAGE, "{key}", message)\n\n')
        #f.write(f'mcp.run()\n')


def main(package):
    # Get all actions
    
    types = extract_types(call("actions"), package)
    generate(types, package)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: generator.py <package>")
        package = "hello41"
        sys.exit(1)

    main(sys.argv[1])

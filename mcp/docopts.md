# Plugin ops a41 mcp

AI tasks to manage Agent41 MCP

## Synopsis

```text
Usage:
  mcp run <package> [--sse]
  mcp generate <package>
  mcp test <package> [--sample] [--norun]
  mcp install [<package>] [--cursor] [--claude] [--5ire] [--uninstall]
  mcp inspect <package>  [--sse] 
  mcp sse <package> [<hostname>] [--uninstall]
```

## Commands

```
  mcp run       run a package. If the--sse flag is set, an Sse mcp server is started
  mcp generate  generate mcp server code for a OpenServerless Package
  mcp test      test the generated mcp server with cli
  mcp install   install/uninstall local mcp server to cursor / claude / 5ire
  mcp inspect   start the MCP web inspector on http://127.0.0.1:6274
  mcp sse       install/uninstall sse mcp server to OpenServerless cluster  
```


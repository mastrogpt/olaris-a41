This is an example of an action:

```
[
      {
            'annotations': [
                  {
                        'key': 'web-export', 'value': True
                  },
                  {
                        'key': 'name:string', 'value': 'name of the person'
                  },
                  {
                        'key': 'raw-http', 'value': False
                  },
                  {
                        'key': 'mcp:type', 'value': 'prompt'
                  },
                  {
                        'key': 'final', 'value': True
                  },
                  {
                        'key': 'provide-api-key', 'value': False
                  },
                  {
                        'key': 'exec', 'value': 'python: 3'
                  }
            ],
            'exec': {
                  'binary': True
            },
            'limits': {
                  'concurrency': 1, 'logs': 10, 'memory': 256, 'timeout': 60000
            },
            'name': 'resource',
            'namespace': 'michele/hello41',
            'publish': False,
            'updated': 1744491147921,
            'version': '0.0.1'
      },
      {
            'annotations': [
                  {
                        'key': 'web-export', 'value': True
                  },
                  {
                        'key': 'raw-http', 'value': False
                  },
                  {
                        'key': 'final', 'value': True
                  },
                  {
                        'key': 'provide-api-key', 'value': False
                  },
                  {
                        'key': 'exec', 'value': 'python: 3'
                  }
            ],
            'exec': {
                  'binary': True
            },
            'limits': {
                  'concurrency': 1, 'logs': 10, 'memory': 256, 'timeout': 60000
            },
            'name': 'stateless',
            'namespace': 'michele/chat',
            'publish': False,
            'updated': 1744490637960,
            'version': '0.0.3'
      },
      {
            'annotations': [
                  {
                        'key': 'web-export', 'value': True
                  },
                  {
                        'key': 'raw-http', 'value': False
                  },
                  {
                        'key': 'final', 'value': True
                  },
                  {
                        'key': 'provide-api-key', 'value': False
                  },
                  {
                        'key': 'exec', 'value': 'python: 3'
                  }
            ],
            'exec': {
                  'binary': True
            },
            'limits': {
                  'concurrency': 1, 'logs': 10, 'memory': 256, 'timeout': 60000
            },
            'name': 'prompt',
            'namespace': 'michele/hello41',
            'publish': False,
            'updated': 1744490637474,
            'version': '0.0.1'
      },
      {
            'annotations': [
                  {
                        'key': 'web-export', 'value': True
                  },
                  {
                        'key': 'raw-http', 'value': False
                  },
                  {
                        'key': 'mcp:type', 'value': 'prompt'
                  },
                  {
                        'key': 'final', 'value': True
                  },
                  {
                        'key': 'provide-api-key', 'value': False
                  },
                  {
                        'key': 'exec', 'value': 'python: 3'
                  }
            ],
            'exec': {
                  'binary': True
            },
            'limits': {
                  'concurrency': 1, 'logs': 10, 'memory': 256, 'timeout': 60000
            },
            'name': 'resorce',
            'namespace': 'michele/hello41',
            'publish': False,
            'updated': 1744490637043,
            'version': '0.0.1'
      },
      {
            'annotations': [
                  {
                        'key': 'web-export', 'value': True
                  },
                  {
                        'key': 'raw-http', 'value': False
                  },
                  {
                        'key': 'final', 'value': True
                  },
                  {
                        'key': 'provide-api-key', 'value': False
                  },
                  {
                        'key': 'exec', 'value': 'python: 3'
                  }
            ],
            'exec': {
                  'binary': True
            },
            'limits': {
                  'concurrency': 1, 'logs': 10, 'memory': 256, 'timeout': 60000
            },
            'name': 'tool',
            'namespace': 'michele/hello41',
            'publish': False,
            'updated': 1744490636617,
            'version': '0.0.1'
      }
]
```

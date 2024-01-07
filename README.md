# Graph Traversal [![](https://github.com/nurlicht/Algorithms/actions/workflows/python-package.yml/badge.svg)](https://github.com/nurlicht/Algorithms/actions)

### Algorithm Features
- Single-pass
- Non-recursive
- Simple character-scan of xml-string
    - No use of find, indexOf ...

### Test Case
  - XML-parsing

### Execution
- Javascript: ```deno test -A```
- Python: ```python ./src/python/xml_parser_test.py```

### Application with other clients
Simply call the following static method (as in the demo-class):
```
XmlParser.parse(xmlString)
``` 

### Implementation
- Data Model
  - XmlTag: Name, indices, attributes ... of an XML-tag
  - XmlNode: Graph-based model for values, children ... of an XML-node
+ Logic
  1. Detect tags
  2. Scan tags
        - Generate new nodes with new start tags (<>)
        - Keep track of the previous tag/node
        - Associate a new node with its parent
        - Assign values to leaves upon detection of an end tag (</>)

Extraction of tags and creation of nodes may be done in parallel or serially (the flag ```extractAllTagsFirst```).

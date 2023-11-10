# Graph Traversal

### Algorithm Features
- Single-pass
- Non-recursive
- Simple character-scan of xml-string
    - No use of find, indexOf ...

### Test Case
  - XML-parsing

### Execution
```
node ./xml-parser.js
```

### Console Output (demo)
```
Input (xmlString):
    <Item_0>
      <Item_0_0 key1="value1" key2="value2">
        4
      </Item_0_0>
      <Item_0_1>
        <Item_0_1_0>
          Hello World!
        </Item_0_1_0>
      </Item_0_1>
    </Item_0>

(stringified) Output (xmlObject): {
  "name": "Item_0",
  "children": [
    {
      "name": "Item_0_0",
      "attributes": {
        "key1": "value1",
        "key2": "value2"
      },
      "value": "4"
    },
    {
      "name": "Item_0_1",
      "children": [
        {
          "name": "Item_0_1_0",
          "value": "Hello World!"
        }
      ]
    }
  ]
}
```

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

class Utilities {
  static hasValue(x) {
    return x !== null && x !== undefined;
  }

  static withDefault(x, xDefault) {
    return Utilities.hasValue(x) ? x : xDefault;
  }
}

class XmlTag {
  tagString;
  firstIndex;
  secondIndex;
  attributes;

  constructor(
    tagString,
    firstIndex,
    secondIndex
  ) {
    this.tagString = tagString;
    this.firstIndex = firstIndex;
    this.secondIndex = secondIndex;
    this.attributes = this.getAtributes();
  }
  
  static getNext(xmlString, searchStartIndex) {
    const xmlStringLength = xmlString.length;
    let firstIndex = -1;
    let secondIndex = -1;
    let index = searchStartIndex;
    while (secondIndex < 0 && index < xmlStringLength) {
      const c = xmlString.charAt(index);
      if (c === '<') {
        if (firstIndex > 0) {
          throw new Error('Unexpected < was encountered.');
        }
        firstIndex = index;
      } else if (c === '>') {
        if (firstIndex < 0) {
          throw new Error('Unexpected > was encountered.');
        }
        secondIndex = index;
      }
      ++index;
    }
    if (secondIndex < 0) {
      return null;
    }
    return new XmlTag(
      xmlString.substring(firstIndex, secondIndex + 1),
      firstIndex,
      secondIndex
    );
  }

  getAtributes() {
    const keyValues = {};
    this.getNameAndAtributes()
      .slice(1)
      .map((x) => x.trim().split('='))
      .forEach((x) => keyValues[x[0].trim()] = x[1].trim().replaceAll('"', ''))
    ;
    return keyValues;
  }

  getName() {
    return this.getNameAndAtributes()[0];
  }

  getNameAndAtributes() {
    if (!this.isValid()) {
      throw new Error('Invalid Tag was encountered.');
    }
    return this.tagString.substring(this.isEndTag() ? 2 : 1, this.tagString.length - 1).split(' ');
  }

  isEndTag() {
    if (!this.isValid()) {
      throw new Error('Invalid Tag was encountered.');
    }
    return this.tagString.startsWith('</');
  }

  isValid() {
    return (
      Utilities.hasValue(this.tagString) &&
      this.tagString.startsWith('<') &&
      this.tagString.charAt(this.tagString.length - 1) === '>' &&
      Number.isInteger(this.firstIndex) &&
      Number.isInteger(this.secondIndex)
    );
  }
}

class XmlNode {
  parent;
  name;
  attributes;
  children;
  value;

  constructor(parent, name, attributes, children, value) {
    this.parent = parent;
    this.name = name;
    this.attributes = attributes;
    this.children = Utilities.withDefault(children, []);
    this.value = value;
    if (Utilities.hasValue(parent)) {
      parent.children.push(this);
    }
  }
  
  static create(parent, name, attributes) {
    return new XmlNode(parent, name, attributes, [], null);
  }
  
  isLeaf() {
    return this.children.length === 0;
  }

  setValue(value) {
    const hasValue = Utilities.hasValue(value);
    if (hasValue && !this.isLeaf()) {
      throw new Error('Value cannot be assigned to a non-leaf node.');
    }
    this.value = hasValue ? value.toString().replaceAll('\\n', '').trim() : null;
  }

  static removeParentsAndNulls(node) {
    if (!Utilities.hasValue(node)) {
      return;
    }
    node.parent = undefined;
    for (const child of node.children) {
      XmlNode.removeParentsAndNulls(child);
    }
    if (node.children.length === 0) {
      node.children = undefined;
    }
    if (!Utilities.hasValue(node.value)) {
      node.value = undefined;
    }
    if (!Utilities.hasValue(node.attributes) || Object.keys(node.attributes).length === 0) {
      node.attributes = undefined;
    }
  }
}

export class XmlParser {
  static parse(xmlString, extractAllTagsFirst) {
    if (typeof xmlString !== 'string') {
      throw new Error('Invalid XML-string was encountered.');
    }
    const xmlNodeRoot = XmlNode.create(null, null);
    if (extractAllTagsFirst) {
      // Method 1: more readable, more separation of concerns, but with more space complexity
      const tags = XmlParser.getTags(xmlString);
      XmlParser.addNodes(xmlString, tags, xmlNodeRoot);
    } else {
      // Method 2: less readable, less separation of concerns, but with less space complexity
      XmlParser.extractTagsAndAddNodes(xmlString, xmlNodeRoot);
    }
    const root = xmlNodeRoot.children[0];
    return root;
  }

  static extractTagsAndAddNodes(xmlString, parent) {
    const xmlStringLength = xmlString.length;
    let index = 0;
    let lastNode = parent;
    let previousTag = null;
    while (index < xmlStringLength) {
      const tag = XmlTag.getNext(xmlString, index);
      if (!Utilities.hasValue(tag)) {
        return;
      } else {
        if (!tag.isEndTag()) { // <TAG>
          const parent = (
            Utilities.hasValue(previousTag) &&
            previousTag.isEndTag() &&
            Utilities.hasValue(lastNode)
            ) ? lastNode.parent : lastNode;
          lastNode = XmlNode.create(parent, tag.getName(), tag.getAtributes());
        } else { // </TAG>
          if (!Utilities.hasValue(previousTag)) {
            throw new Error('Unexpected </TAG> was encountered.');
          }
          if (!previousTag.isEndTag()) {
            if (previousTag.getName() === tag.getName()) {
              const value = xmlString.substring(
                previousTag.secondIndex + 1,
                tag.firstIndex
              );
              lastNode.setValue(value);
            } else {
              throw new Error('Unpaired tag names were encountered: ' +
              tag.getName() + ' vs. ' + previousTag.getName())
            }
          }
        }
        previousTag = tag;
        index = tag.secondIndex + 1;
      }
    }
  }

  static getTags(xmlString) {
    const xmlStringLength = xmlString.length;
    const tags = [];
    let index = 0;
    while (index < xmlStringLength) {
      const tag = XmlTag.getNext(xmlString, index);
      if (Utilities.hasValue(tag)) {
        tags.push(tag);
        index = tag.secondIndex + 1;
      } else {
        index = xmlStringLength;
      }
    }
    return tags;
  }

  static addNodes(xmlString, tags, parent) {
    let lastNode = parent;
    let previousTag = null;
    for (const tag of tags) {
      if (!tag.isEndTag()) { // <TAG>
        const parent = (
          Utilities.hasValue(previousTag) &&
          previousTag.isEndTag() &&
          Utilities.hasValue(lastNode)
          ) ? lastNode.parent : lastNode;
        lastNode = XmlNode.create(parent, tag.getName(), tag.getAtributes());
      } else { // </TAG>
        if (!Utilities.hasValue(previousTag)) {
          throw new Error('Unexpected </TAG> was encountered.');
        }
        if (!previousTag.isEndTag()) {
          if (previousTag.getName() === tag.getName()) {
            const value = xmlString.substring(
              previousTag.secondIndex + 1,
              tag.firstIndex
            );
            lastNode.setValue(value);
          } else {
            throw new Error('Unpaired tag names were encountered: ' +
            tag.getName() + ' vs. ' + previousTag.getName())
          }
        }
      }
      previousTag = tag;
    }
  }

  static removeParentsAndNulls(node) {
    return XmlNode.removeParentsAndNulls(node);
  }
}

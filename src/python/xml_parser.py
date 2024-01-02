class XmlTag:
  def __init__(self, tag_string, first_index, second_index):
    self.tag_string = tag_string
    self.first_index = first_index
    self.second_index = second_index
    self.attributes = self.get_attributes()
  
  @staticmethod
  def get_next(xml_string, search_string_index):
    xml_stringLength = len(xml_string)
    first_index = -1
    second_index = -1
    index = search_string_index
    while (second_index < 0 and index < xml_stringLength):
      c = xml_string[index]
      if (c == '<'):
        if (first_index > 0):
          raise Exception('Unexpected < was encountered.')
        first_index = index
      elif (c == '>'):
        if (first_index < 0):
          raise Exception('Unexpected > was encountered.')
        second_index = index
      index += 1
    if (second_index < 0):
      return None
    return XmlTag(
      xml_string[first_index : second_index + 1],
      first_index,
      second_index
    )

  def get_attributes(self):
    key_values = {}
    attributes = self.get_name_and_attributes()[1:]
    if (len(attributes) == 0):
      return None
    for attribute in attributes:
      key_value = attribute.strip().split('=')
      key_values[key_value[0].strip()] = key_value[1].strip().replace('"', '')
    return key_values

  def get_name(self):
    return self.get_name_and_attributes()[0]
 
  def get_name_and_attributes(self):
    if (not self.is_valid()):
      raise Exception('Invalid Tag was encountered.')
    return self.tag_string[2 if self.is_end_tag() else 1: len(self.tag_string) - 1].split(' ')
 
  def is_end_tag(self):
    if (not self.is_valid()):
      raise Exception('Invalid Tag was encountered.')
    return self.tag_string.startswith('</')

  def is_valid(self):
    return self.tag_string != None and self.tag_string.startswith('<') and self.tag_string[len(self.tag_string) - 1] == '>' and isinstance(self.first_index, int) and isinstance(self.second_index, int) 


class XmlNode:
  def __init__(self, parent, name, attributes, children, value):
    self.parent = parent
    self.name = name
    self.attributes = attributes
    self.children = children if children != None else []
    self.value = value
    if (parent != None):
      parent.children.append(self)
  
  @staticmethod
  def create(parent, name, attributes):
    return XmlNode(parent, name, attributes, [], None)
  
  def isLeaf(self):
    return len(self.children) == 0

  def set_value(self, value):
    if (value == None):
      self.value = None
    else:
      if (not self.isLeaf()):
        raise Exception('Value cannot be assigned to a non-leaf node.')
      self.value = value.replace('\\n', '').strip()


class XmlParser:
  
  @staticmethod
  def parse(xml_string, extractAllTagsFirst):
    if (not isinstance(xml_string, str)):
      raise Exception('Invalid XML-string was encountered.')
    xmlNodeRoot = XmlNode.create(None, None, None)
    if (extractAllTagsFirst):
      # Method 1: more readable, more separation of concerns, but with more space complexity
      tags = XmlParser.getTags(xml_string)
      XmlParser.addNodes(xml_string, tags, xmlNodeRoot)
    else:
      # Method 2: less readable, less separation of concerns, but with less space complexity
      XmlParser.extractTagsAndAddNodes(xml_string, xmlNodeRoot)
    root = xmlNodeRoot.children[0]
    return root

  @staticmethod
  def extractTagsAndAddNodes(xml_string, parent):
    xml_string_length = len(xml_string)
    index = 0
    last_node = parent
    previous_tag = None
    while (index < xml_string_length):
      tag = XmlTag.get_next(xml_string, index)
      if (tag == None):
        return
      else:
        if (not tag.is_end_tag()): # <TAG>
          last_node_is_parent = (
            previous_tag != None and
            previous_tag.is_end_tag() and
            last_node != None
            )
          parent = last_node.parent if last_node_is_parent else last_node
          last_node = XmlNode.create(parent, tag.get_name(), tag.get_attributes())
        else: # </TAG>
          if (previous_tag == None):
            raise Exception('Unexpected </TAG> was encountered.')
          isLeaf = (
            not previous_tag.is_end_tag() and
            previous_tag.get_name() == tag.get_name()
          )
          if (isLeaf):
            value = xml_string[previous_tag.second_index + 1 : tag.first_index]
            last_node.set_value(value)
        previous_tag = tag
        index = tag.second_index + 1

  @staticmethod
  def getTags(xml_string):
    xml_string_length = len(xml_string)
    tags = []
    index = 0
    while (index < xml_string_length):
      tag = XmlTag.get_next(xml_string, index)
      if (tag != None):
        tags.append(tag)
        index = tag.second_index + 1
      else:
        index = xml_string_length
    return tags

  @staticmethod
  def addNodes(xml_string, tags, parent):
    last_node = parent
    previous_tag = None
    for tag in tags:
      if (not tag.is_end_tag()): # <TAG>
        last_node_is_parent = (
          previous_tag != None and
          previous_tag.is_end_tag() and
          last_node != None
          )
        parent = last_node.parent if last_node_is_parent else last_node
        last_node = XmlNode.create(parent, tag.get_name(), tag.get_attributes())
      else: # </TAG>
        if (previous_tag == None):
          raise Exception('Unexpected </TAG> was encountered.')
        isLeaf = (
          not previous_tag.is_end_tag() and
          previous_tag.get_name() == tag.get_name()
        )
        if (isLeaf):
          value = xml_string[previous_tag.second_index + 1 : tag.first_index]
          last_node.set_value(value)
      previous_tag = tag

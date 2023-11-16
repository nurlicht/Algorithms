import unittest
from xml_parser import XmlTag, XmlNode, XmlParser

class XmlTest(unittest.TestCase):

  def test_xml_tag(self):
    tag_string = '> <tag key1=value1 key2=value2>'
    tag_object = XmlTag.get_next(tag_string, 1)
    self.assertIsNotNone(tag_object)
    self.assertEqual(tag_object.get_name(), 'tag', 'tag-name is incorrect')
    self.assertEqual(tag_object.first_index, 2)
    self.assertEqual(tag_object.second_index, 30)
    self.assertEqual(tag_object.attributes, {'key1': 'value1', 'key2': 'value2'})
    self.assertEqual(tag_object.tag_string, '<tag key1=value1 key2=value2>')
    self.assertFalse(tag_object.is_end_tag())
    self.assertTrue(tag_object.is_valid())

  def test_xml_node(self):
    root = XmlNode.create(None, 'root', {'key1': 'value1'})
    self.assertIsNotNone(root)
    self.assertIsNone(root.parent)
    self.assertEqual(root.name, 'root')
    self.assertEqual(root.attributes, {'key1': 'value1'})
    self.assertTrue(root.isLeaf())

    child = XmlNode.create(root, 'child', {'key2': 'value2'})
    self.assertFalse(root.isLeaf())
    self.assertIsNotNone(child)
    self.assertEqual(child.parent, root)
    self.assertEqual(child.name, 'child')
    self.assertEqual(child.attributes, {'key2': 'value2'})
    self.assertTrue(child.isLeaf())

  def test_xml_parser(self):
    # Initialize
    xml_string = (
      '<Item_0>'
        '<Item_0_0 key1="value1" key2="value2">'
          '4'
        '</Item_0_0>'
        '<Item_0_1>'
          '<Item_0_1_0>'
            'Hello World!'
          '</Item_0_1_0>'
        '</Item_0_1>'
      '</Item_0>'
    )

    # Run
    xml_object_1 = XmlParser.parse(xml_string, True)
    xml_object_2 = XmlParser.parse(xml_string, False)

    # Assert
    self.assertIsNotNone(xml_object_1)
    self.assertIsNotNone(xml_object_2)

    for xml_object in [xml_object_1, xml_object_2]:
      self.assertEqual(xml_object.children[0].value, '4')
      self.assertEqual(xml_object.children[0].attributes, {'key1': 'value1', 'key2': 'value2'})
      self.assertEqual(xml_object.children[1].children[0].value, 'Hello World!')


if __name__ == '__main__':
  unittest.main()
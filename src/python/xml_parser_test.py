from email.headerregistry import ParameterizedMIMEHeader
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

  def test_xml_parser_1(self):
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

  def test_xml_parser_2(self):
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
          '<Item_0_1_1 key3="value3" key4="value4">'
            '<Item_0_1_1_0 key5="value5" key6="value6">'
              '<Item_0_1_1_0_0 key7="value7" key8="value8">'
                'Merry Chrismas!'
              '</Item_0_1_1_0_0>'
            '</Item_0_1_1_0>'
          '</Item_0_1_1>'
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
      self.assertEqual(xml_object.children[1].children[1].attributes, {'key3': 'value3', 'key4': 'value4'})
      self.assertEqual(xml_object.children[1].children[1].children[0].attributes, {'key5': 'value5', 'key6': 'value6'})
      self.assertEqual(xml_object.children[1].children[1].children[0].children[0].attributes, {'key7': 'value7', 'key8': 'value8'})
      self.assertEqual(xml_object.children[1].children[1].children[0].children[0].value, 'Merry Chrismas!')

  def test_xml_tag_invalid_1(self):
    # Initialize
    param_list = [
      ('> <tag key1=value1 key2=value2>', 0),
      ('> <tag key1=value1 key2=value2>', 3),
    ]

    # Run/Assert
    for args in param_list:
      with self.subTest(args):
        self.assertRaisesRegex(
          Exception,
          'Unexpected > was encountered.',
          XmlTag.get_next,
          args[0],
          args[1]
        )

  def test_xml_tag_invalid_2(self):
    # Initialize
    param_list = [
      ('sw1< <tag key1=value1 key2=value2>', 0),
      ('sw1< <tag key1=value1 key2=value2>', 1),
      ('sw1< <tag key1=value1 key2=value2>', 3),
    ]

    # Run/Assert
    for args in param_list:
      with self.subTest(args):
        self.assertRaisesRegex(
          Exception,
          'Unexpected < was encountered.',
          XmlTag.get_next,
          args[0],
          args[1]
        )

  def test_parse_invalid_1(self):
    # Initialize
    param_list = [
      (1, True),
      (True, True),
      ({}, True),
      ([], True),
      (1, False),
      (True, False),
      ({}, False),
      ([], False)
    ]

    # Run/Assert
    for args in param_list:
      with self.subTest(args):
        self.assertRaisesRegex(
          Exception,
          'Invalid XML-string was encountered.',
          XmlParser.parse,
          args[0],
          args[1]
        )

  def test_parse_invalid_2(self):
    # Initialize
    param_list = [
      ('</b>', False),
      ('1 </b>', True),
    ]

    # Run/Assert
    for args in param_list:
      with self.subTest(args):
        self.assertRaisesRegex(
          Exception,
          'Unexpected </TAG> was encountered.',
          XmlParser.parse,
          args[0],
          args[1]
        )

  def test_parse_invalid_3(self):
    # Initialize
    param_list = [
      ('<b>1</a>', False)
    ]

    # Run/Assert
    for args in param_list:
      with self.subTest(args):
        self.assertRaisesRegex(
          Exception,
          'Unpaired tag names were encountered: a vs. b',
          XmlParser.parse,
          args[0],
          args[1]
        )

if __name__ == '__main__':
  unittest.main()
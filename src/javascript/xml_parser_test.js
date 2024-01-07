import { XmlParser } from './xml_parser.js';

import { assert, assertThrows } from "https://deno.land/std@0.211.0/assert/mod.ts";


Deno.test('Health-Check', async () => {
    assert((await new Promise((res, rej) => res(4))) === 4);
}, 1000);


[true, false].forEach((extractAllTagsFirst) => {
  Deno.test('XML can be parsed with extractAllTagsFirst=' + extractAllTagsFirst, () => {
    // Initialize
    const xmlString = `
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
    `;

    // Run
    const xmlObject = XmlParser.parse(xmlString, extractAllTagsFirst);
    XmlParser.removeParentsAndNulls(xmlObject); 

    // Assert
    assert(xmlObject.children[0].value, '4')
    assert(xmlObject.children[0].attributes, {'key1': 'value1', 'key2': 'value2'})
    assert(xmlObject.children[1].children[0].value, 'Hello World!')
    assert(xmlObject.children[1].children[1].attributes, {'key3': 'value3', 'key4': 'value4'})
    assert(xmlObject.children[1].children[1].children[0].attributes, {'key5': 'value5', 'key6': 'value6'})
    assert(xmlObject.children[1].children[1].children[0].children[0].attributes, {'key7': 'value7', 'key8': 'value8'})
    assert(xmlObject.children[1].children[1].children[0].children[0].value, 'Merry Chrismas!')
  }, 1000);
});


[true, false].forEach((extractAllTagsFirst) => {
  Deno.test('Invalid XML causes an exception with extractAllTagsFirst=' + extractAllTagsFirst, () => {
    // Initialize
    const xmlString = '<b>1</a>';

    // Run/Assert
    assertThrows(
      () => XmlParser.parse(xmlString, extractAllTagsFirst),
      Error,
      'Unpaired tag names were encountered: a vs. b'
    );
  }, 1000);
});



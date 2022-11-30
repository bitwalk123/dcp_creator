import json
from xml.dom import minidom

import dicttoxml

jsonname = 'C:/Users/212295/Downloads/Nagahata/dcp.json'


def prettify(xml_string: str):
    """Return a pretty-printed XML string for the Element.
    """
    dom = minidom.parseString(xml_string)
    # dom = minidom.parse(xml_fname)
    return dom.toprettyxml()


if __name__ == "__main__":
    with open(jsonname, 'r') as f:
        json_dict = json.load(f)
        print(json_dict)
        xml = dicttoxml.dicttoxml(json_dict)
        print(xml)
        print(prettify(xml))

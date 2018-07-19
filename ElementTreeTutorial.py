"""
https://docs.python.org/3/library/xml.etree.elementtree.html
"""

# Parsing XML
# We can import this data by reading from a file:
import xml.etree.ElementTree as ET
tree = ET.parse('country_data.xml')
root = tree.getroot()
# Or directly from a string:
root = ET.fromstring(country_data_as_string)
# As an Element, root has a tag and a dictionary of attributes:
print(root.tag, root.attrib)
# It also has children nodes over which we can iterate:
for child in root:
    print(child.tag, child.attrib)
# Children are nested, and we can access specific child nodes by index:
print(root[0][1].text)


# Pull API for non-blocking parsing
# parse XML incrementally, without blocking operations
parser = ET.XMLPullParser(['start', 'end'])
parser.feed('<mytag>sometext')
list(parser.read_events())
parser.feed(' more text</mytag>')
for event, elem in parser.read_events():
    print(event)
    print(elem.tag, 'text=', elem.text)


# Finding interesting elements
# iterate recursively over all the sub-tree below it (its children, their children, and so on)
for neighbor in root.iter('neighbor'):
    print(neighbor.attrib)
# finall() finds only elements with a tag which are direct children of the current element
# find() finds the first child with a particular tag
# text accesses the element’s text content
# get() accesses the element’s attributes
for country in root.findall('country'):
    rank = country.find('rank').text
    name = country.get('name')
    print(name, rank)


# Modifying an XML File






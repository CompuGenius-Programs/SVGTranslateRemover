import re
import xml.etree.ElementTree as ET


def apply_translation(match):
    command = match.group(1)
    points = match.group(2).split()
    translated_points = []
    for i in range(0, len(points), 2):
        x = float(points[i]) + translate_x
        y = float(points[i + 1]) + translate_y
        translated_points.append(f"{x} {y}")
    return f"{command}{' '.join(translated_points)}"


ET.register_namespace("", "http://www.w3.org/2000/svg")

tree = ET.parse('original.svg')
root = tree.getroot()

for path in root.findall('.//{http://www.w3.org/2000/svg}path'):
    d = path.get('d')
    translate = path.get('transform')

    translate_x, translate_y = map(float, re.match(r'translate\(([^,]+),([^)]+)\)', translate).groups())

    d = re.sub(r'([A-Za-z])([\d\s.-]+)', apply_translation, d)

    path.set('d', d)
    del path.attrib['transform']

tree.write('modified.svg')

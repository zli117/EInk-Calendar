import xml.etree.ElementTree as ET


class WeatherIconLookup:
    def __init__(self, value_path: str):
        self.map = {}
        root = ET.parse(value_path).getroot()
        for child in root:
            if child.tag == 'string' and 'name' in child.attrib:
                self.map[child.attrib['name']] = child.text

    def look_up_with_name(self, name: str):
        # Default N/A
        return self.map.get(name, '\uf07b')

    def look_up_with_owm_id(self, id: int):
        return self.look_up_with_name('wi_owm_%03d' % id)

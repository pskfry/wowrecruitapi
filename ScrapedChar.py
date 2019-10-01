import re
from dateutil.parser import parse

class ScrapedChar:
    def __init__(self, tds):
        for id, td in enumerate(tds):
            if id == 0:
                # parse name column
                p = re.compile(r'<td.*?a[^>]*character (?P<CLASS>[^"]*)')
                m = p.search(repr(td))
                self.char_class = m.group('CLASS')
                p = re.compile(r'<td.*?a[^>]*>(?P<NAME>[^<]*)')
                m = p.search(repr(td))
                self.char_name = m.group('NAME')
            if id == 1:
                # parse guild column
                p = re.compile(r'<td.*?a[^>]*&lt;(?P<GUILD>[A-z ]*)&')
                m = p.search(repr(td))
                if m:
                    self.guild = m.group('GUILD')
                else:
                    self.guild = ''
            if id == 3:
                # parse realm column
                p = re.compile(r'<td.*?a[^>]*>(?P<SERVER>[^<]*)')
                m = p.search(repr(td))
                if m:
                    self.realm_name = m.group('SERVER')
                else:
                    self.realm_name = ''

                    
            if id == 4:
                # parse ilvl column
                p = re.compile(r'<td[^>]*>(?P<ILVL>[^<]*)')
                m = p.search(repr(td))
                if m:
                    self.item_level = float(m.group('ILVL'))
                else:
                    self.item_level = ''
            if id == 5:
                # parse last updated column
                p = re.compile(
                    r'<td[^>].*?<span[^>]*label="(?P<LASTUPDATED>[^"]*)')
                m = p.search(repr(td))
                if m:
                    last_updated = m.group('LASTUPDATED')
                    last_updated_pydate = parse(last_updated)
                    self.last_updated = last_updated_pydate.strftime(
                        "%m-%d-%Y %H:%M:%S")
                else:
                    self.last_updated = ''
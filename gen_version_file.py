#!/usr/bin/env python
# coding: utf-8
import re

from app import DCPCreator

pattern_version = re.compile(r'^(.+)\.(.+)\.(.+)$')
info_version = """VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(%s, %s, %s, 0),
    prodvers=(%s, %s, %s, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u''),
        StringStruct(u'FileDescription', u'DCP Creator'),
        StringStruct(u'FileVersion', u'%s.%s.%s'),
        StringStruct(u'InternalName', u'dcp_creator'),
        StringStruct(u'LegalCopyright', u'\xa9 Keiichi Takahashi, All rights reserved.'),
        StringStruct(u'OriginalFilename', u'dcp_creator.exe'),
        StringStruct(u'ProductName', u'DCP Creator'),
        StringStruct(u'ProductVersion', u'%s.%s.%s.0')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)"""

if __name__ == "__main__":
    m = pattern_version.match(DCPCreator.__version__)
    if m:
        list_version_element = [m.group(i) for i in range(1, 4)]
    else:
        list_version_element = ['0', '0', '0']
    # write version information
    file_version = 'version.txt'
    with open(file_version, mode='w', encoding='UTF-8') as f:
        f.write(info_version % tuple(list_version_element * 4))
    print('> Complete generating version file!')

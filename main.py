#!/usr/local/bin/python
# coding: utf-8

import doc
import engine
import util

code = '600519'

if __name__ == '__main__':
    engine.start(code)
    doc.generate_doc(code)
    util.log('大功告成')

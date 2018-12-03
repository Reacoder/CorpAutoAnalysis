#!/usr/local/bin/python
# coding: utf-8

import doc
import engine
# import snow
import util

if __name__ == '__main__':
    engine.start()
    doc.generate_doc()
    # snow.start_write()
    util.log('大功告成')

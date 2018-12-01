#!/usr/local/bin/python
# coding: utf-8

import config
import doc
import engine
import util

if __name__ == '__main__':
    engine.start(config.CODE)
    doc.generate_doc(config.CODE)
    util.log('大功告成')

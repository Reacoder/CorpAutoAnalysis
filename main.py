#!/usr/local/bin/python
# coding: utf-8

import util


def make_doc():
    import doc
    import engine
    engine.start()
    doc.generate_doc()


def make_snow():
    import snow
    snow.start_write()


if __name__ == '__main__':
    # make_doc()
    make_snow()
    util.log('大功告成')

#!/usr/local/bin/python
# coding: utf-8

import errno
import json
import os
import pickle
from io import BytesIO

from PIL import Image

import config


def save_cookie(driver, path):
    with open(path, 'wb') as f:
        pickle.dump(driver.get_cookies(), f)


def load_cookie(driver, path):
    with open(path, 'rb') as f:
        cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)


def save_file(code, filename, text, mode='w'):
    path = get_file_path(code, filename)
    create_path(path)
    with open(path, mode) as f:
        log('保存文本到 %s' % path)
        f.write(text)


def read_file(code, filename):
    path = get_file_path(code, filename)
    if not os.path.isfile(path):
        return ''
    with open(path, 'r') as f:
        return f.read()


def load_json(code):
    path = get_file_path(code, 'json')
    create_path(path)
    with open(path, 'r') as f:
        saved_data = json.load(f)
        log('从 %s 取出 %s ' % (path, str(saved_data)))
        return saved_data


def save_json(code, key, value):
    path = get_file_path(code, 'json')
    create_path(path)
    saved_data = {}
    if os.path.isfile(path):
        saved_data = load_json(code)
    saved_data[key] = value
    with open(path, 'w') as f:
        log('保存 { %s : %s } 到 %s ' % (key, value, path))
        json.dump(saved_data, f)


def get_img_path(code, filename):
    path = os.path.join('private/' + code, filename + r".png")
    return path


def get_file_path(code, filename):
    path = os.path.join('private/' + code, filename + r".txt")
    return path


def create_path(path):
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as e:  # Guard against race condition
            if e.errno != errno.EEXIST:
                raise


def get_code_type(code):
    code_type = 'sh'
    if code[0] == '0':
        code_type = 'sz'
    return code_type


def log(content):
    print('========>> %s ' % content)


def save_rect_element(png, left, top, right, bottom, code, filename):
    left = config.FACTOR * left
    top = config.FACTOR * top
    right = config.FACTOR * right
    bottom = config.FACTOR * bottom
    im = Image.open(BytesIO(png))  # uses PIL library to open image in memory
    im = im.crop((left, top, right, bottom))  # defines crop points
    path = get_img_path(code, filename)
    log('保存图片到 %s' % path)
    create_path(path)
    im.save(path)  # saves new cropped image

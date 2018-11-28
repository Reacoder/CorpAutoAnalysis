#!/usr/local/bin/python
# coding: utf-8

import base64
import errno
import os
import time
from io import BytesIO

from PIL import Image
from selenium import webdriver

from private.account import LXR

brower = webdriver.Chrome()
lxr = LXR()


def save_image(canvas, code, filename):
    canvas_base64 = brower.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)
    # decode
    canvas_png = base64.b64decode(canvas_base64)
    # save to a file
    path = get_path(code, filename)
    create_path(path)
    with open(path, 'wb') as f:
        log('保存图片到 %s' % path)
        f.write(canvas_png)


def get_path(code, filename):
    path = os.path.join('private/' + code, filename + r".png")
    return path


def create_path(path):
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as e:  # Guard against race condition
            if e.errno != errno.EEXIST:
                raise


def grab_lxr_data(code):
    url = 'https://www.lixinger.com/analytics/company/%s/%s/detail/fundamental/value/primary' % (
        get_code_type(code), code)
    brower.get(url)
    brower.implicitly_wait(30)  # 隐性等待，最长等30秒
    goto_login_btn = brower.find_element_by_css_selector('.btn.btn-success.ng-binding')
    goto_login_btn.click()
    log('点击去登陆按钮')
    brower.implicitly_wait(10)
    username_input = brower.find_element_by_name('uniqueName')
    password_input = brower.find_element_by_name('password')
    username_input.send_keys(lxr.username)
    password_input.send_keys(lxr.password)
    login_btn = brower.find_element_by_css_selector('.btn.btn-primary.text-capitalize.pull-right.ng-isolate-scope')
    login_btn.click()
    log('点击登陆按钮')

    grab_lxr_guzhi(code)
    grab_lxr_yingli(code)


def grab_lxr_guzhi(code):
    log('获取估值分析')
    url = 'https://www.lixinger.com/analytics/company/%s/%s/detail/fundamental/value/primary' % (
        get_code_type(code), code)
    brower.get(url)
    brower.implicitly_wait(30)
    key = ".chart.chart-line.ng-isolate-scope.chartjs-render-monitor"
    canvas_list = brower.find_elements_by_css_selector(key)
    i = 0
    prefix = 'lxr_gz_'
    name_list = ['pe'
        , 'pb'
        , 'ps'
        , 'guxi']
    for canvas in canvas_list:
        save_image(canvas, code, prefix + name_list[i])
        i = i + 1


def grab_lxr_yingli(code):
    log('获取盈利分析')
    url = 'https://www.lixinger.com/analytics/company/%s/%s/detail/fundamental/profit' % (
        get_code_type(code), code)
    brower.get(url)
    brower.implicitly_wait(30)
    key = ".chart.chart-line.ng-scope.ng-isolate-scope.chartjs-render-monitor"
    canvas_list = brower.find_elements_by_css_selector(key)
    prefix = 'lxr_yl_'
    name_list = ['roe_jiaquan'
        , 'roe_guimu'
        , ''
        , 'ganggan'
        , ''
        , 'zhouzhuan'
        , 'jinglirunlv'
        , ''
        , '']
    i = 0
    for canvas in canvas_list:
        if len(name_list[i]) > 0:
            save_image(canvas, code, prefix + name_list[i])
        i = i + 1


def grab_ths_zst(code):
    log('获取走势图')
    url = 'http://data.10jqka.com.cn/market/lhbgg/code/%s/' % code
    brower.get(url)
    brower.implicitly_wait(30)

    brower.switch_to.frame(1)
    key = ".draw-type.klView"
    btn_list = brower.find_elements_by_css_selector(key)
    prefix = 'ths_zst_'
    name_list = ['day', 'week', 'month']
    i = 0
    for btn in btn_list:
        btn.click()
        time.sleep(1)
        canvas = brower.find_element_by_id('tcanvas')
        save_image(canvas, code, prefix + name_list[i])
        i = i + 1


def get_code_type(code):
    type = 'sh'
    if code[0] == '0':
        type = 'sz'
    return type


def log(content):
    print('========>> %s ' % content)


def save_element_image(png, element, code, filename):
    log('从元素获取图片')
    location = element.location
    size = element.size

    im = Image.open(BytesIO(png))  # uses PIL library to open image in memory
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    im = im.crop((left, top, right, bottom))  # defines crop points
    path = get_path(code, filename)
    create_path(path)
    im.save(path)  # saves new cropped image


def save_rect_element(png, left, top, right, bottom, code, filename):
    log('从元素获取图片')
    im = Image.open(BytesIO(png))  # uses PIL library to open image in memory
    im = im.crop((left, top, right, bottom))  # defines crop points
    path = get_path(code, filename)
    create_path(path)
    im.save(path)  # saves new cropped image


def grab_ths_brief(code):
    log('获取公司概要')
    url = 'http://basic.10jqka.com.cn/%s/' % code
    brower.get(url)
    brower.implicitly_wait(30)
    key = ".bd"
    element_list = brower.find_elements_by_css_selector(key)
    element = element_list[1]
    png = brower.get_screenshot_as_png()
    save_element_image(png, element, code, 'ths_brief')


def grab_ths_operate(code):
    log('主营构成分析')
    url = 'http://basic.10jqka.com.cn/%s/operate.html' % code
    brower.get(url)
    brower.implicitly_wait(30)
    parent = brower.find_element_by_id('analysis')
    key = "clearfix"
    element = parent.find_element_by_class_name(key)
    brower.execute_script("arguments[0].scrollIntoView();", element)

    head = brower.find_element_by_class_name('header')
    brower.execute_script('$(arguments[0]).fadeOut()', head)
    search = brower.find_element_by_css_selector('.iwc_searchbar.clearfix.float_box')
    brower.execute_script('$(arguments[0]).fadeOut()', search)
    time.sleep(1)

    left = element.location['x']
    top = 0

    width = element.size['width']
    height = 0.3 * width

    right = left + width
    bottom = top + height

    png = brower.get_screenshot_as_png()
    save_rect_element(png, left, top, right, bottom, code, 'ths_product')


if __name__ == '__main__':
    code = '002050'
    # grab_lxr_data(code)
    # grab_ths_zst(code)
    # grab_ths_brief(code)
    grab_ths_operate(code)
    log('大功告成')

'''
#将页面滚动条拖到底部
js = "document.documentElement.scrollTop=400"
brower.execute_script(js)
time.sleep(1)



'''

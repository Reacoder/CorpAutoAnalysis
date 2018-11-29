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

driver = webdriver.Chrome()
lxr = LXR()
FACTOR = 2  # 分辨率高的为2，低的为1


def save_image(canvas, code, filename):
    canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)
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
    driver.get(url)
    driver.implicitly_wait(30)  # 隐性等待，最长等30秒
    goto_login_btn = driver.find_element_by_css_selector('.btn.btn-success.ng-binding')
    goto_login_btn.click()
    log('点击去登陆按钮')
    driver.implicitly_wait(10)
    username_input = driver.find_element_by_name('uniqueName')
    password_input = driver.find_element_by_name('password')
    username_input.send_keys(lxr.username)
    password_input.send_keys(lxr.password)
    login_btn = driver.find_element_by_css_selector('.btn.btn-primary.text-capitalize.pull-right.ng-isolate-scope')
    login_btn.click()
    log('点击登陆按钮')

    grab_lxr_valuation(code)
    grab_lxr_profit(code)


def grab_lxr_valuation(code):
    log('获取估值分析')
    url = 'https://www.lixinger.com/analytics/company/%s/%s/detail/fundamental/value/primary' % (
        get_code_type(code), code)
    driver.get(url)
    driver.implicitly_wait(30)
    key = ".chart.chart-line.ng-isolate-scope.chartjs-render-monitor"
    canvas_list = driver.find_elements_by_css_selector(key)
    i = 0
    prefix = 'img_valuation_'
    name_list = ['pe'
        , 'pb'
        , 'ps'
        , 'dividend']
    for canvas in canvas_list:
        save_image(canvas, code, prefix + name_list[i])
        i = i + 1


def grab_lxr_profit(code):
    log('获取盈利分析')
    url = 'https://www.lixinger.com/analytics/company/%s/%s/detail/fundamental/profit' % (
        get_code_type(code), code)
    driver.get(url)
    driver.implicitly_wait(30)
    key = ".chart.chart-line.ng-scope.ng-isolate-scope.chartjs-render-monitor"
    canvas_list = driver.find_elements_by_css_selector(key)
    prefix = 'img_profit_'
    name_list = ['roe_weight'
        , 'roe'
        , ''
        , 'leverage'
        , ''
        , 'turnover'
        , 'profit_rate'
        , ''
        , '']
    i = 0
    for canvas in canvas_list:
        if len(name_list[i]) > 0:
            save_image(canvas, code, prefix + name_list[i])
        i = i + 1


def grab_ths_trend(code):
    log('获取走势图')
    url = 'http://data.10jqka.com.cn/market/lhbgg/code/%s/' % code
    driver.get(url)
    driver.implicitly_wait(30)

    driver.switch_to.frame(1)
    key = ".draw-type.klView"
    btn_list = driver.find_elements_by_css_selector(key)
    prefix = 'img_trend_'
    name_list = ['day', 'week', 'month']
    i = 0
    for btn in btn_list:
        btn.click()
        time.sleep(1)
        canvas = driver.find_element_by_id('tcanvas')
        save_image(canvas, code, prefix + name_list[i])
        i = i + 1


def get_code_type(code):
    type = 'sh'
    if code[0] == '0':
        type = 'sz'
    return type


def log(content):
    print('========>> %s ' % content)


def save_rect_element(png, left, top, right, bottom, code, filename):
    left = FACTOR * left
    top = FACTOR * top
    right = FACTOR * right
    bottom = FACTOR * bottom
    im = Image.open(BytesIO(png))  # uses PIL library to open image in memory
    im = im.crop((left, top, right, bottom))  # defines crop points
    path = get_path(code, filename)
    log('保存图片到 %s' % path)
    create_path(path)
    im.save(path)  # saves new cropped image


def grab_ths_brief(code):
    log('公司概要')
    url = 'http://basic.10jqka.com.cn/%s/' % code
    driver.get(url)
    driver.implicitly_wait(30)
    element_list = driver.find_elements_by_css_selector(".bd")
    element = element_list[1]
    scroll_to_element(element)
    hide_float_search()
    save_element(element, code, 'img_brief')


def grab_ths_operate(code):
    log('经营分析')
    url = 'http://basic.10jqka.com.cn/%s/operate.html' % code
    driver.get(url)
    driver.implicitly_wait(30)
    element_list = driver.find_elements_by_css_selector(".bd.pt5")
    # 公司产品
    element = element_list[2]
    scroll_to_element(element)
    hide_float_search()
    save_element(element, code, 'img_product_category')
    # 上下游
    element = element_list[3]
    scroll_to_element(element)
    save_element(element, code, 'img_partner')


def save_element(element, code, filename):
    left = element.location['x']
    top = 0
    width = element.size['width']
    height = element.size['height']
    right = left + width
    bottom = top + height
    png = driver.get_screenshot_as_png()
    save_rect_element(png, left, top, right, bottom, code, filename)


def scroll_to_element(element):
    driver.execute_script("arguments[0].scrollIntoView();", element)


def hide_float_search():
    head = driver.find_element_by_class_name('header')
    driver.execute_script('$(arguments[0]).fadeOut()', head)
    search = driver.find_element_by_css_selector('.iwc_searchbar.clearfix.float_box')
    driver.execute_script('$(arguments[0]).fadeOut()', search)
    time.sleep(1)


if __name__ == '__main__':
    code = '002050'
    grab_lxr_data(code)
    grab_ths_trend(code)
    grab_ths_brief(code)
    grab_ths_operate(code)
    log('大功告成')

#!/usr/local/bin/python
# coding: utf-8

import base64
import errno
import os

from selenium import webdriver

from private.account import LXR

brower = webdriver.Chrome()
lxr = LXR()


def save_image(canvas, code, filename):
    canvas_base64 = brower.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)
    # decode
    canvas_png = base64.b64decode(canvas_base64)
    # save to a file
    path = os.path.join('private/' + code, filename + r".png")
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as e:  # Guard against race condition
            if e.errno != errno.EEXIST:
                raise
    with open(path, 'wb') as f:
        f.write(canvas_png)


def grab_data_from_lxr(code):
    type = 'sh'
    if code[0] == '0':
        type = 'sz'
    url = 'https://www.lixinger.com/analytics/company/%s/%s/detail/fundamental/value/primary' % (type, code)
    brower.get(url)
    brower.implicitly_wait(30)  # 隐性等待，最长等30秒
    goto_login_btn = brower.find_element_by_css_selector('.btn.btn-success.ng-binding')
    goto_login_btn.click()
    brower.implicitly_wait(10)
    username_input = brower.find_element_by_name('uniqueName')
    password_input = brower.find_element_by_name('password')
    username_input.send_keys(lxr.username)
    password_input.send_keys(lxr.password)
    login_btn = brower.find_element_by_css_selector('.btn.btn-primary.text-capitalize.pull-right.ng-isolate-scope')
    login_btn.click()
    brower.implicitly_wait(30)
    canvas_list = brower.find_elements_by_css_selector(".chart.chart-line.ng-isolate-scope.chartjs-render-monitor")
    i = 1
    for canvas in canvas_list:
        save_image(canvas, code, str(i))
        i = i + 1


if __name__ == '__main__':
    grab_data_from_lxr('002050')

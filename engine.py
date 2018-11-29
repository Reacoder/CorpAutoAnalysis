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
FACTOR = 1  # 分辨率高的为2，低的为1


def save_image(canvas, code, filename):
    canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)
    # decode
    canvas_png = base64.b64decode(canvas_base64)
    # save to a file
    path = get_img_path(code, filename)
    create_path(path)
    with open(path, 'wb') as f:
        log('保存图片到 %s' % path)
        f.write(canvas_png)


def save_file(code, filename, text):
    path = get_file_path(code, filename)
    create_path(path)
    with open(path, 'a') as f:
        log('保存文本到 %s' % path)
        f.write(text)


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
    path = get_img_path(code, filename)
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
    # 题材要点
    element = driver.find_element_by_css_selector(".gntc")
    save_file(code, 'file_concept', element.text)


def grab_ths_operate(code):
    log('经营分析')
    url = 'http://basic.10jqka.com.cn/%s/operate.html' % code
    driver.get(url)
    driver.implicitly_wait(30)
    element_list = driver.find_elements_by_css_selector(".bd.pt5")
    # 公司产品
    # element = element_list[2]
    # scroll_to_element(element)
    # hide_float_search()
    # save_element(element, code, 'img_operate_product')

    elements = driver.find_elements_by_css_selector(".m_table.m_hl")
    element = elements[2]
    scroll_to_element(element)
    hide_float_search()
    save_element(element, code, 'img_operate_product')
    element = elements[3]
    scroll_to_element(element)
    save_element(element, code, 'img_operate_product2')

    # 上下游
    element = element_list[3]
    scroll_to_element(element)
    save_element(element, code, 'img_operate_partner')
    # 董事会经营评述
    driver.find_elements_by_css_selector(".more.fr")[0].click()
    driver.implicitly_wait(10)
    element = driver.find_elements_by_css_selector(".f14.none.clearfix.pr")[0]
    save_file(code, 'file_operate', element.text)


def grab_ths_holder(code):
    log('股东研究')
    url = 'http://basic.10jqka.com.cn/%s/holder.html' % code
    driver.get(url)
    driver.implicitly_wait(30)
    element_list = driver.find_elements_by_css_selector(".bd.pt5")
    # 股东人数
    element = element_list[0]
    scroll_to_element(element)
    hide_float_search()
    save_element(element, code, 'img_holder_count')
    # 十大流通股东
    element = element_list[1]
    scroll_to_element(element)
    save_element(element, code, 'img_holder_ten_circulation')
    # 十大股东
    element = element_list[2]
    scroll_to_element(element)
    save_element(element, code, 'img_holder_ten')
    # 控股层级关系
    element = element_list[3]
    scroll_to_element(element)
    log(element.location['y'])
    # 公司
    # save_element(element, code, 'img_controller', y=element.size['width'] * 0.35)
    # 家里
    save_element(element, code, 'img_controller', y=element.size['width'] * 0.25)


def grab_ths_worth(code):
    log('盈利预测')
    url = 'http://basic.10jqka.com.cn/%s/worth.html' % code
    driver.get(url)
    driver.implicitly_wait(30)
    element_list = driver.find_elements_by_css_selector(".bd")
    # 业绩预测
    element = element_list[1]
    scroll_to_element(element)
    hide_float_search()
    save_element(element, code, 'img_worth_forecast')
    # driver.execute_script("document.body.style.zoom='80%'")
    # 业绩预测详表
    # element = element_list[2]
    # scroll_to_element(element)
    # save_element(element, code, 'img_worth_forecast_table')
    element = driver.find_elements_by_css_selector(".m_table.m_hl.posi_table")[0]
    scroll_to_element(element)
    save_element(element, code, 'img_worth_forecast_table')
    element = driver.find_elements_by_css_selector(".m_table.m_hl.ggintro.ggintro_1.organData")[0]
    scroll_to_element(element)
    save_element(element, code, 'img_worth_forecast_table2')


def grab_ths_news(code):
    log('新闻公告')
    url = 'http://basic.10jqka.com.cn/%s/news.html' % code
    driver.get(url)
    driver.implicitly_wait(30)
    element = driver.find_element_by_css_selector(".bd.m_dlbox")
    scroll_to_element(element)
    # 研报评级
    tr_list = driver.find_elements_by_css_selector(".organ_item")

    for tr in tr_list:
        link = tr.find_element_by_css_selector(".client.pagescroll")
        td_list = tr.find_elements_by_tag_name('td')
        title = td_list[1].text + "\n" + td_list[2].text + "\n" + td_list[3].text + "\n"
        title = title + "-" * 50 + "\n"
        save_file(code, 'file_worth', title)

        window_before = driver.window_handles[0]
        link.click()
        driver.implicitly_wait(10)
        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after)
        element = driver.find_element_by_css_selector(".YBText")
        save_file(code, 'file_worth', element.text + "\n\n" + "=" * 50 + "\n\n")
        driver.switch_to.window(window_before)
        driver.implicitly_wait(10)


# def grab_ths_concept(code):
#     log('概念题材')
#     url = 'http://basic.10jqka.com.cn/%s/concept.html' % code
#     driver.get(url)
#     driver.implicitly_wait(30)
#     driver.find_elements_by_css_selector(".conAllBtn")[2].click()
#     driver.implicitly_wait(3)
#     element = driver.find_element_by_id("material")
#     save_file(code, 'file_concept', element.text)


def grab_ths_position(code):
    log('主力持仓')
    url = 'http://basic.10jqka.com.cn/%s/position.html' % code
    driver.get(url)
    driver.implicitly_wait(30)
    element_list = driver.find_elements_by_css_selector(".bd.pt5.pr")
    element = element_list[0]
    scroll_to_element(element)
    hide_float_search()
    save_element(element, code, 'img_position')


def grab_ths_bonus(code):
    log('分红融资')
    url = 'http://basic.10jqka.com.cn/%s/bonus.html' % code
    driver.get(url)
    driver.implicitly_wait(30)
    element = driver.find_element_by_id("bonus_table")
    scroll_to_element(element)
    hide_float_search()
    save_element(element, code, 'img_bonus')
    element = driver.find_element_by_id("additionprofile_bd")
    scroll_to_element(element)
    save_element(element, code, 'img_addition_profile')


def grab_ths_event(code):
    log('公司大事')
    url = 'http://basic.10jqka.com.cn/%s/event.html' % code
    driver.get(url)
    driver.implicitly_wait(30)
    element = driver.find_element_by_id("manager")
    scroll_to_element(element)
    hide_float_search()
    save_element(element, code, 'img_event_manager')
    element = driver.find_element_by_id("holder")
    scroll_to_element(element)
    save_element(element, code, 'img_event_holder')


def save_element(element, code, filename, y=0):
    left = element.location['x']
    top = y
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
    code = '600373'
    # driver.execute_script("document.body.style.zoom='80%'")
    # driver.maximize_window()
    # grab_lxr_data(code)
    # grab_ths_trend(code)
    grab_ths_brief(code)
    grab_ths_operate(code)
    grab_ths_holder(code)
    grab_ths_worth(code)
    grab_ths_news(code)
    grab_ths_position(code)
    grab_ths_bonus(code)
    grab_ths_event(code)
    log('大功告成')

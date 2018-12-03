#!/usr/local/bin/python
# coding: utf-8

import base64
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import config
import util
from private.account import LXR

driver = webdriver.Chrome()
driver.set_window_position(-2000, 0)
lxr = LXR()
cookie_path = 'private/cookie_lxr.txt'


def grab_lxr_data(code):
    util.log('获取理杏仁数据')
    util.create_path(cookie_path)
    url = 'https://www.lixinger.com'
    driver.get(url)
    time.sleep(1)
    try:
        util.load_cookie(driver, cookie_path)
    except FileNotFoundError:
        url = 'https://www.lixinger.com/analytics/company/%s/%s/detail/fundamental/value/primary' % (
            util.get_code_type(code), code)
        driver.get(url)
        driver.implicitly_wait(30)  # 隐性等待，最长等30秒
        goto_login_btn = driver.find_element_by_css_selector('.btn.btn-success.ng-binding')
        goto_login_btn.click()
        util.log('点击去登陆按钮')
        driver.implicitly_wait(10)
        username_input = driver.find_element_by_name('uniqueName')
        password_input = driver.find_element_by_name('password')
        username_input.send_keys(lxr.username)
        password_input.send_keys(lxr.password)
        login_btn = driver.find_element_by_css_selector('.btn.btn-primary.text-capitalize.pull-right.ng-isolate-scope')
        login_btn.click()
        util.log('点击登陆按钮')
        time.sleep(2)
        util.save_cookie(driver, cookie_path)
        util.log('登陆成功')
    # 开始获取数据
    grab_lxr_valuation(code)
    grab_lxr_profit(code)
    grab_lxr_growth(code)
    try:
        driver.find_element_by_link_text('成本分析')
        grab_lxr_costs(code)
        grab_lxr_asset(code)
        grab_lxr_debt(code)
    except NoSuchElementException:
        util.log('没有成本分析')
        util.log('没有资产分析')
        util.log('没有负债分析')


def grab_lxr_valuation(code):
    util.log('获取估值分析')
    url = 'https://www.lixinger.com/analytics/company/%s/%s/detail/fundamental/value/primary' % (
        util.get_code_type(code), code)
    driver.get(url)
    driver.implicitly_wait(30)
    key = ".chart.chart-line.ng-isolate-scope.chartjs-render-monitor"
    canvas_list = driver.find_elements_by_css_selector(key)
    text_list = driver.find_elements_by_css_selector('.list-unstyled.metric-info')
    i = 0
    prefix = 'img_valuation_'
    name_list = ['pe'
        , 'pb'
        , 'ps'
        , 'dividend']
    for canvas in canvas_list:
        save_image(canvas, code, prefix + name_list[i])
        util.save_json(code, name_list[i], text_list[i].text)
        i = i + 1


def grab_lxr_profit(code):
    util.log('获取盈利分析')
    url = 'https://www.lixinger.com/analytics/company/%s/%s/detail/fundamental/profit' % (
        util.get_code_type(code), code)
    driver.get(url)
    driver.implicitly_wait(30)
    key = ".chart.chart-line.ng-scope.ng-isolate-scope.chartjs-render-monitor"
    canvas_list = driver.find_elements_by_css_selector(key)
    text_list = driver.find_elements_by_css_selector('.list-unstyled.metric-info')
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
            util.save_json(code, name_list[i], text_list[i].text)
        i = i + 1


def grab_lxr_growth(code):
    util.log('获取成长分析')
    url = 'https://www.lixinger.com/analytics/company/%s/%s/detail/fundamental/growth' % (
        util.get_code_type(code), code)
    driver.get(url)
    driver.implicitly_wait(30)
    key = ".chart.chart-bar.ng-scope.ng-isolate-scope.chartjs-render-monitor"
    canvas_list = driver.find_elements_by_css_selector(key)
    text_list = driver.find_elements_by_css_selector('.list-unstyled.metric-info')
    prefix = 'img_growth_'
    name_list = ['total_income'
        , 'profit'
        , 'profit_exclude'
        , 'cash_flow'
        , '']
    i = 0
    for canvas in canvas_list:
        if len(name_list[i]) > 0:
            save_image(canvas, code, prefix + name_list[i])
            util.save_json(code, name_list[i], text_list[i].text)
        i = i + 1


def grab_lxr_costs(code):
    util.log('获取成本分析')
    url = 'https://www.lixinger.com/analytics/company/%s/%s/detail/fundamental/costs' % (
        util.get_code_type(code), code)
    driver.get(url)
    driver.implicitly_wait(30)
    key = ".chart.chart-line.ng-scope.ng-isolate-scope.chartjs-render-monitor"
    canvas_list = driver.find_elements_by_css_selector(key)
    text_list = driver.find_elements_by_css_selector('.list-unstyled.metric-info')
    prefix = 'img_costs_'
    name_list = ['gross_profit_rate'
        , 'three_fee_rate'
        , 'sale_fee_rate'
        , 'manage_fee_rate'
        , 'finance_fee_rate'
        , ''
        , '']
    i = 0
    for canvas in canvas_list:
        if len(name_list[i]) > 0:
            save_image(canvas, code, prefix + name_list[i])
            util.save_json(code, name_list[i], text_list[i].text)
        i = i + 1


def grab_lxr_asset(code):
    util.log('资产结构分析')
    url = 'https://www.lixinger.com/analytics/company/%s/%s/detail/fundamental/asset' % (
        util.get_code_type(code), code)
    driver.get(url)
    driver.implicitly_wait(30)
    key = ".chart.chart-line.ng-isolate-scope.chartjs-render-monitor"
    canvas = driver.find_element_by_css_selector(key)
    name = 'img_asset'
    time.sleep(1)
    save_image(canvas, code, name)
    # 保存详情
    element = driver.find_element_by_css_selector('.chart-pie-cta')
    scroll_to_element(element)
    driver.execute_script('document.getElementsByClassName("btn-cta")[0].style.display = "none";')
    time.sleep(1)
    save_element(element, code, 'img_asset_detail', y=config.FACTOR * 40)


def grab_lxr_debt(code):
    util.log('负债结构分析')
    url = 'https://www.lixinger.com/analytics/company/%s/%s/detail/fundamental/debt' % (
        util.get_code_type(code), code)
    driver.get(url)
    driver.implicitly_wait(30)
    key = ".chart.chart-line.ng-isolate-scope.chartjs-render-monitor"
    canvas = driver.find_element_by_css_selector(key)
    name = 'img_debt'
    time.sleep(1)
    save_image(canvas, code, name)
    # 保存详情
    element = driver.find_element_by_css_selector('.chart-pie-cta')
    scroll_to_element(element)
    driver.execute_script('document.getElementsByClassName("btn-cta")[0].style.display = "none";')
    time.sleep(1)
    save_element(element, code, 'img_debt_detail', y=config.FACTOR * 40)


def grab_ths_trend(code):
    util.log('获取走势图')
    url = 'http://data.10jqka.com.cn/market/lhbgg/code/%s/' % code
    driver.get(url)
    time.sleep(1)
    driver.get(url)
    time.sleep(2)
    title_element = driver.find_element_by_class_name('fz24')
    util.save_json(code, 'code_name', title_element.text)
    driver.switch_to.frame(1)
    time.sleep(1)
    key = ".draw-type.klView"
    btn_list = driver.find_elements_by_css_selector(key)
    prefix = 'img_trend_'
    name_list = ['day', 'week', 'month']
    i = 0
    for btn in btn_list:
        btn.click()
        time.sleep(1)
        element = driver.find_element_by_id('canvasPanel')
        scroll_to_element(element)
        time.sleep(1)
        save_element(element, code, prefix + name_list[i])
        # canvas = driver.find_element_by_id('tcanvas')
        # save_image(canvas, code, prefix + name_list[i])
        i = i + 1


def grab_ths_brief(code):
    util.log('公司概要')
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
    util.save_file(code, 'file_concept', element.text)


def grab_ths_operate(code):
    util.log('经营分析')
    url = 'http://basic.10jqka.com.cn/%s/operate.html' % code
    driver.get(url)
    driver.implicitly_wait(30)
    # element_list = driver.find_elements_by_css_selector(".bd.pt5")
    # 公司产品
    # element = element_list[2]
    # scroll_to_element(element)
    # hide_float_search()
    # save_element(element, code, 'img_operate_product')

    # elements = driver.find_elements_by_css_selector(".m_table.m_hl")
    # element = elements[2]
    # scroll_to_element(element)
    # hide_float_search()
    # save_element(element, code, 'img_operate_product')
    # element = elements[3]
    # scroll_to_element(element)
    # save_element(element, code, 'img_operate_product2')
    # < !-- 主营构成分析 -->
    analysis = driver.find_element_by_id('analysis')
    element = analysis.find_element_by_css_selector('.bd.pt5')
    scroll_to_element(element)
    hide_float_search()
    save_element(element, code, 'img_operate_product')
    # <!-- 主要客户及供应商 -->
    try:
        provider = driver.find_element_by_id('provider')
        element = provider.find_element_by_css_selector('.bd.pt5')
        scroll_to_element(element)
        save_element(element, code, 'img_operate_partner')
    except NoSuchElementException:
        pass

    # # 上下游
    # element = element_list[3]
    # scroll_to_element(element)
    # save_element(element, code, 'img_operate_partner')
    # 董事会经营评述
    driver.find_elements_by_css_selector(".more.fr")[0].click()
    driver.implicitly_wait(10)
    element = driver.find_elements_by_css_selector(".f14.none.clearfix.pr")[0]
    util.save_file(code, 'file_operate', element.text)


def grab_ths_holder(code):
    util.log('股东研究')
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
    top = get_bottom_element_top(element)
    if top > 0:  # 到底了
        save_element(element, code, 'img_controller', y=top)
    else:
        save_element(element, code, 'img_controller', )
    # window_height = driver.get_window_size()['height']
    # top = element.size['width']*0.6 - element.size['height']
    # top = window_height - element.size['height'] * 2.25
    # save_element(element, code, 'img_controller', y=top)


def get_bottom_element_top(element):
    # 开始计算
    window_height = driver.get_window_size().get('height')
    doc_height = driver.find_element_by_tag_name('html').size['height']
    element_y = element.location['y']
    bottom_distance = doc_height - element_y
    dy = 120  # 补差值
    top = window_height - bottom_distance - dy
    util.log('window_height %f' % window_height)
    util.log('doc_height %f' % doc_height)
    util.log('element_y %f' % element_y)
    util.log('bottom_distance %f' % bottom_distance)
    util.log('top %f ' % top)
    return top


def grab_ths_worth(code):
    util.log('盈利预测')
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
    element_list = driver.find_elements_by_css_selector(".m_table.m_hl.posi_table")
    if len(element_list) > 0:
        element = element_list[0]
        scroll_to_element(element)
        save_element(element, code, 'img_worth_forecast_table')
        element = driver.find_elements_by_css_selector(".m_table.m_hl.ggintro.ggintro_1.organData")[0]
        scroll_to_element(element)
        save_element(element, code, 'img_worth_forecast_table2')


def grab_ths_news(code):
    util.log('新闻公告')
    url = 'http://basic.10jqka.com.cn/%s/news.html' % code
    driver.get(url)
    driver.implicitly_wait(30)
    try:
        element = driver.find_element_by_css_selector(".bd.m_dlbox")
        scroll_to_element(element)
        # 研报评级
        tr_list = driver.find_elements_by_css_selector(".organ_item")

        i = 1
        for tr in tr_list:
            link = tr.find_element_by_css_selector(".client.pagescroll")
            td_list = tr.find_elements_by_tag_name('td')
            title = td_list[1].text + "\n" + td_list[2].text + "\n" + td_list[3].text + "\n"
            title = title + "-" * 50 + "\n"
            util.save_file(code, 'file_worth', title, mode='a')

            window_before = driver.window_handles[0]
            link.click()
            driver.implicitly_wait(10)
            window_after = driver.window_handles[1]
            driver.switch_to.window(window_after)
            try:
                element = driver.find_element_by_css_selector(".YBText")
            except NoSuchElementException:
                element = driver.find_element_by_id('news_content')
            util.save_file(code, 'file_worth', element.text + "\n" * 4, mode='a')
            driver.switch_to.window(window_before)
            driver.implicitly_wait(10)
            if i == config.WORTH_COUNT:
                break
            i = i + 1
    except NoSuchElementException:
        pass


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
    util.log('主力持仓')
    url = 'http://basic.10jqka.com.cn/%s/position.html' % code
    driver.get(url)
    driver.implicitly_wait(30)
    element_list = driver.find_elements_by_css_selector(".bd.pt5.pr")
    element = element_list[0]
    scroll_to_element(element)
    hide_float_search()
    save_element(element, code, 'img_position')


def grab_ths_bonus(code):
    util.log('分红融资')
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
    util.log('公司大事')
    url = 'http://basic.10jqka.com.cn/%s/event.html' % code
    driver.get(url)
    driver.implicitly_wait(30)
    # 高管持股变动
    try:
        parent = driver.find_element_by_id("manager")
        element = parent.find_element_by_css_selector('.m_table_data.pagination')
        scroll_to_element(element)
        hide_float_search()
        save_element(element, code, 'img_event_manager')
    except NoSuchElementException:
        head = driver.find_element_by_class_name('header')
        driver.execute_script('$(arguments[0]).fadeOut()', head)
    # 股东持股变动
    try:
        parent = driver.find_element_by_id("holder")
        element = parent.find_element_by_css_selector('.m_table_data.pagination')
        scroll_to_element(element)
        top = get_bottom_element_top(element)
        if top > 0:  # 到底了
            save_element(element, code, 'img_event_holder', y=top)
        else:
            save_element(element, code, 'img_event_holder', )
    except NoSuchElementException:
        pass


def scroll_to_element(element):
    driver.execute_script("arguments[0].scrollIntoView();", element)


def hide_float_search():
    head = driver.find_element_by_class_name('header')
    driver.execute_script('$(arguments[0]).fadeOut()', head)
    try:
        search = driver.find_element_by_css_selector('.iwc_searchbar.clearfix.float_box')
        driver.execute_script('$(arguments[0]).fadeOut()', search)
    except NoSuchElementException:
        pass
    time.sleep(1)


def save_element(element, code, filename, y=0):
    left = element.location['x']
    top = y
    width = element.size['width']
    height = element.size['height']
    right = left + width
    bottom = top + height
    png = driver.get_screenshot_as_png()
    util.save_rect_element(png, left, top, right, bottom, code, filename)


def save_image(canvas, code, filename):
    canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", canvas)
    # decode
    canvas_png = base64.b64decode(canvas_base64)
    # save to a file
    path = util.get_img_path(code, filename)
    util.create_path(path)
    with open(path, 'wb') as f:
        util.log('保存图片到 %s' % path)
        f.write(canvas_png)


def start():
    code = config.CODE
    grab_lxr_data(code)
    grab_ths_trend(code)
    grab_ths_brief(code)
    grab_ths_operate(code)
    grab_ths_holder(code)
    grab_ths_worth(code)
    grab_ths_news(code)
    grab_ths_position(code)
    grab_ths_bonus(code)
    grab_ths_event(code)
    util.log('引擎运行完毕')


if __name__ == '__main__':
    code = config.CODE
    # driver.execute_script("document.body.style.zoom='80%'")
    # driver.maximize_window()
    # grab_lxr_data(code)
    # grab_ths_trend(code)
    # grab_ths_brief(code)
    # grab_ths_operate(code)
    # grab_ths_holder(code)
    # grab_ths_worth(config.CODE)
    grab_ths_news(code)
    # grab_ths_position(code)
    # grab_ths_bonus(code)
    # grab_ths_event(code)
    util.log('引擎运行完毕')

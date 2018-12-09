#!/usr/local/bin/python
# coding: utf-8


import os
import time

from selenium import webdriver

import config
import util
from private.account import LXR

driver = webdriver.Chrome()
if config.HIDE:
    driver.set_window_position(-2000, 0)
lxr = LXR()
cookie_path = 'private/cookie_snow.txt'


def login_snow():
    util.create_path(cookie_path)
    url = 'https://xueqiu.com/'
    driver.get(url)
    sleep()
    try:
        util.load_cookie(driver, cookie_path)
    except FileNotFoundError:
        driver.get(url)
        driver.implicitly_wait(30)  # 隐性等待，最长等30秒
        goto_login_btn = driver.find_element_by_css_selector('.nav__login__btn')
        goto_login_btn.click()
        util.log('点击去登陆按钮')
        driver.implicitly_wait(10)
        username_input = driver.find_element_by_name('username')
        password_input = driver.find_element_by_name('password')
        username_input.send_keys(lxr.username)
        sleep()
        password_input.send_keys(lxr.password)
        login_btn = driver.find_element_by_css_selector('.modal__login__btn')
        login_btn.click()
        util.log('点击登陆按钮')
        time.sleep(30)
        util.save_cookie(driver, cookie_path)
        util.log('登陆成功')


def get_res_dir(code):
    return config.LOCAL_DIR + 'private/' + code + '/'


def write_article(code):
    my_dir = get_res_dir(code)
    my_dict = util.load_json(code)
    url = 'https://xueqiu.com/write'
    driver.get(url)
    sleep()
    element_title = driver.find_element_by_css_selector('.long-text__title')
    element_content = driver.find_element_by_css_selector(
        '.sb-editor__container.editor--progress.medium-editor-element')
    parent = driver.find_element_by_css_selector('.sb-editor__upload')
    element_file = parent.find_element_by_name('file')
    # 标题
    util.log('标题')
    element_title.send_keys(my_dict['code_name'])
    # 走势图
    util.log('走势图')
    element_content.send_keys('\n' + '走势图' + '\n')
    element_content.send_keys('1.周k线' + '\n')
    element_file.send_keys(my_dir + 'img_trend_week.png')
    sleep()
    element_content.send_keys('2.日k线' + '\n')
    element_file.send_keys(my_dir + 'img_trend_day.png')
    sleep()
    # 插播广告
    util.log('插播广告')
    element_content.send_keys('\n' + '***** 如果你需要个股的这种文档，请加我徽信：Reacoder​ 或者关注 美旺新高 公众号 *****' + '\n')
    # 一.公司概要
    util.log('一.公司概要')
    element_content.send_keys('一.公司概要' + '\n')
    element_file.send_keys(my_dir + 'img_brief.png')
    sleep()
    # 二.业务构成
    util.log('二.业务构成')
    element_content.send_keys('二.业务构成' + '\n')
    element_file.send_keys(my_dir + 'img_operate_product.png')
    sleep()
    if os.path.isfile(my_dir + 'img_costs_gross_profit_rate.png'):
        element_content.send_keys('1.毛利率' + '\n')
        element_content.send_keys(my_dict['gross_profit_rate'].replace('\n', ' ' * 3) + '\n')
        element_file.send_keys(my_dir + 'img_costs_gross_profit_rate.png')
        sleep()
        element_content.send_keys('2.三项费用率' + '\n')
        element_content.send_keys(my_dict['three_fee_rate'].replace('\n', ' ' * 3) + '\n')
        element_file.send_keys(my_dir + 'img_costs_three_fee_rate.png')
        sleep()
        element_content.send_keys('3.销售费用率' + '\n')
        element_content.send_keys(my_dict['sale_fee_rate'].replace('\n', ' ' * 3) + '\n')
        element_file.send_keys(my_dir + 'img_costs_sale_fee_rate.png')
        sleep()
        element_content.send_keys('4.管理费用率' + '\n')
        element_content.send_keys(my_dict['manage_fee_rate'].replace('\n', ' ' * 3) + '\n')
        element_file.send_keys(my_dir + 'img_costs_manage_fee_rate.png')
        sleep()
        element_content.send_keys('5.财务费用率' + '\n')
        element_content.send_keys(my_dict['finance_fee_rate'].replace('\n', ' ' * 3) + '\n')
        element_file.send_keys(my_dir + 'img_costs_finance_fee_rate.png')
        sleep()
    # 三.股东占比情况
    util.log('三.股东占比情况')
    element_content.send_keys('三.股东占比情况' + '\n')
    element_content.send_keys('1.股东人数' + '\n')
    element_file.send_keys(my_dir + 'img_holder_count.png')
    sleep()
    element_content.send_keys('2.十大流通股东' + '\n')
    element_file.send_keys(my_dir + 'img_holder_ten_circulation.png')
    sleep()
    element_content.send_keys('3.十大股东' + '\n')
    element_file.send_keys(my_dir + 'img_holder_ten.png')
    sleep()
    element_content.send_keys('4.控制层级关系' + '\n')
    element_file.send_keys(my_dir + 'img_controller.png')
    sleep()
    element_content.send_keys('5.机构持股汇总' + '\n')
    element_file.send_keys(my_dir + 'img_position.png')
    sleep()
    element_content.send_keys('6.高管持股变动' + '\n')
    if os.path.isfile(my_dir + 'img_event_manager.png'):
        element_file.send_keys(my_dir + 'img_event_manager.png')
        sleep()
    else:
        element_content.send_keys('无高管持股变动' + '\n')
    if os.path.isfile(my_dir + 'img_event_holder.png'):
        element_content.send_keys('7.股东持股变动' + '\n')
        element_file.send_keys(my_dir + 'img_event_holder.png')
        sleep()
    element_content.send_keys('8.分红情况' + '\n')
    element_file.send_keys(my_dir + 'img_bonus.png')
    sleep()
    # 四.生意特征
    util.log('四.生意特征')
    element_content.send_keys('四.生意特征' + '\n')
    element_content.send_keys('1.主要客户及供应商' + '\n')
    if os.path.isfile(my_dir + 'img_operate_partner.png'):
        element_file.send_keys(my_dir + 'img_operate_partner.png')
        sleep()
    else:
        element_content.send_keys('无主要客户及供应商' + '\n')
    element_content.send_keys('2.加权ROE' + '\n')
    element_content.send_keys(my_dict['roe_weight'].replace('\n', ' ' * 3) + '\n')
    element_file.send_keys(my_dir + 'img_profit_roe_weight.png')
    sleep()
    element_content.send_keys('3.归属于母公司股东的ROE' + '\n')
    element_content.send_keys(my_dict['roe'].replace('\n', ' ' * 3) + '\n')
    element_file.send_keys(my_dir + 'img_profit_roe.png')
    sleep()
    element_content.send_keys('4.杠杆倍数' + '\n')
    element_content.send_keys(my_dict['leverage'].replace('\n', ' ' * 3) + '\n')
    element_file.send_keys(my_dir + 'img_profit_leverage.png')
    sleep()
    element_content.send_keys('5.资产周转率' + '\n')
    element_content.send_keys(my_dict['turnover'].replace('\n', ' ' * 3) + '\n')
    element_file.send_keys(my_dir + 'img_profit_turnover.png')
    sleep()
    element_content.send_keys('6.净利润率' + '\n')
    element_content.send_keys(my_dict['profit_rate'].replace('\n', ' ' * 3) + '\n')
    element_file.send_keys(my_dir + 'img_profit_profit_rate.png')
    sleep()
    # 五.成长性评估
    util.log('五.成长性评估')
    element_content.send_keys('五.成长性评估' + '\n')
    element_content.send_keys('1.业绩预测' + '\n')
    element_file.send_keys(my_dir + 'img_worth_forecast.png')
    sleep()
    if os.path.isfile(my_dir + 'img_worth_forecast_table.png'):
        element_content.send_keys('2.业绩预测详表' + '\n')
        element_file.send_keys(my_dir + 'img_worth_forecast_table.png')
        sleep()
        element_file.send_keys(my_dir + 'img_worth_forecast_table2.png')
        sleep()
    # 插播广告
    util.log('插播广告')
    element_content.send_keys('\n' + '***** 如果你需要个股的这种文档，请加我徽信：Reacoder​ 或者关注 美旺新高 公众号 *****' + '\n')
    element_file.send_keys(config.LOCAL_DIR + 'qr_code.jpg')
    sleep()
    # 六.估值分析
    util.log('六.估值分析')
    element_content.send_keys('六.估值分析' + '\n')
    element_content.send_keys('1.PE-TTM (扣非)' + '\n')
    element_content.send_keys(my_dict['pe'].replace('\n', ' ' * 3) + '\n')
    element_file.send_keys(my_dir + 'img_valuation_pe.png')
    sleep()
    element_content.send_keys('2.PB (不含商誉)' + '\n')
    element_content.send_keys(my_dict['pb'].replace('\n', ' ' * 3) + '\n')
    element_file.send_keys(my_dir + 'img_valuation_pb.png')
    sleep()
    element_content.send_keys('3.PS-TTM' + '\n')
    element_content.send_keys(my_dict['ps'].replace('\n', ' ' * 3) + '\n')
    element_file.send_keys(my_dir + 'img_valuation_ps.png')
    sleep()
    # 七.收入，利润，现金流分析
    util.log('七.收入，利润，现金流分析')
    element_content.send_keys('七.收入，利润，现金流分析' + '\n')
    element_content.send_keys('1.营业总收入' + '\n')
    element_content.send_keys(my_dict['total_income'].replace('\n', ' ' * 3) + '\n')
    element_file.send_keys(my_dir + 'img_growth_total_income.png')
    sleep()
    element_content.send_keys('2.营业利润' + '\n')
    element_content.send_keys(my_dict['profit'].replace('\n', ' ' * 3) + '\n')
    element_file.send_keys(my_dir + 'img_growth_profit.png')
    sleep()
    element_content.send_keys('3.归属于母公司股东的扣非净利润' + '\n')
    element_content.send_keys(my_dict['profit_exclude'].replace('\n', ' ' * 3) + '\n')
    element_file.send_keys(my_dir + 'img_growth_profit_exclude.png')
    sleep()
    element_content.send_keys('4.经营活动产生的现金流量净额' + '\n')
    element_content.send_keys(my_dict['cash_flow'].replace('\n', ' ' * 3) + '\n')
    element_file.send_keys(my_dir + 'img_growth_cash_flow.png')
    sleep()
    # 八.资产负债分析
    util.log('八.资产负债分析')
    element_content.send_keys('八.资产负债分析' + '\n')
    if os.path.isfile(my_dir + 'img_asset.png') and os.path.isfile(my_dir + 'img_debt.png'):
        element_content.send_keys('1.资产分析' + '\n')
        element_file.send_keys(my_dir + 'img_asset.png')
        sleep()
        element_content.send_keys('2.负债分析' + '\n')
        element_file.send_keys(my_dir + 'img_debt.png')
        sleep()
    else:
        element_content.send_keys('特殊行业无资产负债分析' + '\n')
    # 九.券商分析
    util.log('九.券商分析')
    element_content.send_keys('九.券商分析' + '\n')
    element_content.send_keys(util.read_file(code, 'file_worth') + '\n')
    # 十.题材要点
    util.log('十.题材要点')
    element_content.send_keys('十.题材要点' + '\n')
    element_content.send_keys(util.read_file(code, 'file_concept') + '\n')
    # 十一.董事会经营评述
    util.log('十一.董事会经营评述')
    element_content.send_keys('十一.董事会经营评述' + '\n')
    element_content.send_keys(util.read_file(code, 'file_operate') + '\n')


def sleep():
    time.sleep(2)


def start_write():
    login_snow()
    write_article(config.CODE)


if __name__ == '__main__':
    login_snow()
    write_article(config.CODE)

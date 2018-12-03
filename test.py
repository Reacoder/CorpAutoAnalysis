#!/usr/local/bin/python
# coding: utf-8


from selenium import webdriver

import util

driver = webdriver.Chrome()
driver.set_window_position(-2000, 0)
url = 'https://wenku.baidu.com/view/96ef3824192e45361066f5ca.html?rec_flag=default&sxts=1542964211853'


def parse():
    driver.get(url)
    driver.implicitly_wait(30)  # 隐性等待，最长等30秒
    ele_title = driver.find_element_by_id('doc-tittle-0')
    util.log(ele_title.text)
    page_ele = driver.find_element_by_id('pageNo-1')
    util.save_file('wenku', 'test', page_ele.text)


if __name__ == '__main__':
    parse()

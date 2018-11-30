from docx import Document
from docx.shared import Inches

import util
import engine

document = Document()


def generate_doc(code):
    engine.start(code)
    my_dir = 'private/' + code + '/'
    my_dict = util.load_json(code)
    pic_width = Inches(7)

    document.add_heading(my_dict['code_name'], 0)

    document.add_heading('走势图', level=1)
    document.add_picture(my_dir + 'img_trend_day.png', width=pic_width)

    document.add_heading('一.公司概要', level=1)
    document.add_picture(my_dir + 'img_brief.png', width=pic_width)

    document.add_heading('二.业务构成', level=1)
    document.add_picture(my_dir + 'img_operate_product.png', width=pic_width)
    document.add_heading('1.毛利率', level=2)
    document.add_picture(my_dir + 'img_costs_gross_profit_rate.png', width=pic_width)
    document.add_heading('2.三项费用率', level=2)
    document.add_picture(my_dir + 'img_costs_three_fee_rate.png', width=pic_width)
    document.add_heading('3.销售费用率', level=2)
    document.add_picture(my_dir + 'img_costs_sale_fee_rate.png', width=pic_width)
    document.add_heading('4.管理费用率', level=2)
    document.add_picture(my_dir + 'img_costs_manage_fee_rate.png', width=pic_width)
    document.add_heading('5.财务费用率', level=2)
    document.add_picture(my_dir + 'img_costs_finance_fee_rate.png', width=pic_width)

    document.save('private/' + code + '/' + 'demo.docx')


if __name__ == '__main__':
    code = '600519'
    generate_doc(code)

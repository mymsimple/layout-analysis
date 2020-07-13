#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Title   : OCR 相关枚举类型
@File    :   ocr_enum.py    
@Author  : vincent
@Time    : 2020/7/8 4:56 下午
@Version : 1.0 
'''
from enum import Enum


class BizType(Enum):
    # 银行流水
    bank_flow = "01"
    # 征信报告
    credit_report = "02"
    # 住房公积金
    housing_provident_fund = "03"

# -*- coding: utf-8 -*-

{
    'name': 'Gap Analysis Quotations',
    'version': '0.1',
    'author': 'Carlos Paredes',
    'website': 'https://github.com/anex',
    'category': 'Gap Analysis',
    'depends': [
        'base',
        'gap_analysis'
    ],
    'description': """
Adds feature to generate a Order Quotation from a Gap Analysis

Instructions
==============

Before try generate a Order Quotation from a Gap Analysis must be add a product on:

Configuration -> Configuration -> Gap Analysis -> Quotation Product.

This product will be use like product template for convert the Gap Analysis Functionalities in Sale Order Lines.
""",
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'views/gap_analysis_quotation.xml',
        'wizard/wizard_gap_analysis_quotation_view.xml',
    ],
    'active': True,
}

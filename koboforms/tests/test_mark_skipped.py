#_*_ coding: utf-8 _*_

from unittest import TestCase
from mark_skipped import FormDef, Survey
import os


class TestFormDef(TestCase):

    def setUp(self):
        self.form = FormDef('data/DOB_F3.xls')
        print('')

    def test_read_skipconditions(self):
        ret = self.form.read_skipconditions()
        print(ret)
        
    def test__check_colnames(self):
        conds = self.form.form.loc[:,('name', 'relevant')]
        with self.assertLogs(level='WARN'):
            self.form._check_colnames(conds)
        #print(conds)
        



# formname = '../data/DOB_F3.xls'
# sname = '../data/DOB_F3_2017_03_01_compact.csv'
# f = FormDef(formname)
# s = Survey(sname)



         
        
        
#   p[0] = 'check_selected(' + p[3] + ', ' + p[5] + ')'
#    'get_column(\'' + p[1][2:-1] + '\')'

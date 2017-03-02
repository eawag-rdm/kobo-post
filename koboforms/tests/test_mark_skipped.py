#_*_ coding: utf-8 _*_

from unittest import TestCase
from mark_skipped import FormDef, Survey

class TestFormDef(TestCase):

    def setUp(self):
        self.form = FormDef('../data/DOB_F3.xls')

    def test_mk_skip_conditions(self):
        conds = self.form.mk_skipconditions()
        print(conds)
        #self.assertEqual(conds, ())



# formname = '../data/DOB_F3.xls'
# sname = '../data/DOB_F3_2017_03_01_compact.csv'
# f = FormDef(formname)
# s = Survey(sname)



         
        
        
#   p[0] = 'check_selected(' + p[3] + ', ' + p[5] + ')'
#    'get_column(\'' + p[1][2:-1] + '\')'

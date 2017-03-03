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
        self.assertEqual(
            list(ret.loc[105]),
            ['Appearance_of_pond_systems_e_',
             ("check_selected(get_column('What_are_the_primary_secondar'), "
              "'free_water_surface_constructed') or check_selected(get_column("
              "'What_are_the_primary_secondar'), 'wsp___anaerobic_pond') or ch"
              "eck_selected(get_column('What_are_the_primary_secondar'), 'wsp_"
              "__facultative_pond') or check_selected(get_column('What_are_the"
              "_primary_secondar'), 'wsp___maturation_pond') or check_selected"
              "(get_column('What_are_the_primary_secondar'), 'aerated_pond') or "
              "check_selected(get_column('What_are_the_primary_secondar'), 'pol"
              "ishing_pond')")])
        
    def test__check_colnames(self):
        conds = self.form.form.loc[:,('name', 'relevant')]
        with self.assertLogs(level='WARN'):
            conds = self.form._check_colnames(conds)
        self.assertNotIn(15, conds)
        self.assertEqual(len(conds), 248)

        
class TestSurvey(TestCase):
    
    def setUp(self):
        self.form = FormDef('data/DOB_F3.xls')
        self.surv = Survey('data/DOB_F3_2017_03_01_compact.csv',
                           'data/DOB_F3.xls' )
        print('')

    def test__get_column(self):
        res = self.surv._get_column('Names_of_interviewers')
        self.assertEqual(res[19], ['rohan'])
        self.assertEqual(res[17], ['rohan', 'other'])
        self.assertEqual(len(res), 132)

    def test__check_selected(self):
        column = self.surv._get_column('Names_of_interviewers')
        self.assertTrue(self.surv._check_selected(column[17], 'other'))
        self.assertFalse(self.surv._check_selected(column[19], 'other'))
        print(type(column))
        
        

# formname = '../data/DOB_F3.xls'
# sname = '../data/DOB_F3_2017_03_01_compact.csv'
# f = FormDef(formname)
# s = Survey(sname)



         
        
        
#   p[0] = 'check_selected(' + p[3] + ', ' + p[5] + ')'
#    'get_column(\'' + p[1][2:-1] + '\')'

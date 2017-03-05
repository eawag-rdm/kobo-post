#_*_ coding: utf-8 _*_

from unittest import TestCase
from mark_skipped import FormDef, Survey
import os
import pandas as pd


class TestFormDef(TestCase):

    def setUp(self):
        self.form = FormDef('data/DOB_F3.xls')
        print('')

    def test_read_skipconditions(self):
        ret = self.form.read_skipconditions()
        desid = ['Appearance_of_pond_systems_e_',
                 ("logical_or(logical_or(logical_or(logical_or(logical_or(chec"
                  "k_selected(get_column('What_are_the_primary_secondar'), 'fr"
                  "ee_water_surface_constructed'), check_selected(get_column('"
                  "What_are_the_primary_secondar'), 'wsp___anaerobic_pond')), "
                  "check_selected(get_column('What_are_the_primary_secondar'), "
                  "'wsp___facultative_pond')), check_selected(get_column('What"
                  "_are_the_primary_secondar'), 'wsp___maturation_pond')), che"
                  "ck_selected(get_column('What_are_the_primary_secondar'), 'a"
                  "erated_pond')), check_selected(get_column('What_are_the_pri"
                  "mary_secondar'), 'polishing_pond'))")]
        self.assertEqual(list(ret.loc[105]), desid)
     
    def test__check_colnames(self):
        conds = self.form.form.loc[:,('name', 'relevant')]
        with self.assertLogs(level='WARN'):
            conds = self.form._check_colnames(conds)
        self.assertNotIn(15, conds)
        self.assertEqual(len(conds), 248)

    def test__mk_loopgrouping(self):
        print('')
        self.form._mk_loopgrouping()

        
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
        isselected = self.surv._check_selected(column, 'other')
        self.assertEqual(list(isselected[8:20]),
                         [True, True, True, True, False,
                          False, False, True, False, True, False, False])
        
    def test_eval_skiprules(self):
        res = self.surv.eval_skiprules()

    # def test__expand_skiprules(self):
    #     self.surv._expand_groups()
        
    
        
            


            

            
# s = Survey(sname)



         
        
        
#   p[0] = 'check_selected(' + p[3] + ', ' + p[5] + ')'
#    'get_column(\'' + p[1][2:-1] + '\')'

#_*_ coding: utf-8 _*_

from unittest import TestCase
from mark_skipped import FormDef, Survey
import os
import pandas as pd
import numpy as np


pd.options.display.max_colwidth = 200


class TestFormDef(TestCase):

    def setUp(self):
        self.form = FormDef('data/DOB_F3.xls')
        self.surv = Survey('data/DOB_F3_2017_03_01_compact.csv',
                           'data/DOB_F3.xls' )
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

    def test_mk_loopgrouping(self):
        self.form = FormDef('data/Test_Formdef_Loops.xls')
        self.surv = Survey('data/Test_Loops_DOB_F3_compact.csv',
                           'data/Test_Formdef_Loops.xls' )
        self.form.mk_loopgrouping(self.surv)
        l = self.form.form.loc[[5,12], ['name', 'relevant']].values
        expect = np.array([['group_vq7sw37[1]/Others_003',
                             "${group_vq7sw37[1]/What_pre_treatment_stages_are} = 'kitchen_grease' or ${group_vq7sw37[1]/What_pre_treatment_stages_are} = 'oil_skimmer' or ${group_vq7sw37[1]/What_pre_treatment_stages_are} = 'screen_with_ma' or ${group_vq7sw37[1]/What_pre_treatment_stages_are} = 'screen_with_me' or ${group_vq7sw37[1]/What_pre_treatment_stages_are} = 'grit_removal' or ${group_vq7sw37[1]/What_pre_treatment_stages_are} = 'grease_trap_at' or ${group_vq7sw37[1]/What_pre_treatment_stages_are} = 'integrated_gri' or ${group_vq7sw37[1]/What_pre_treatment_stages_are} = 'other'"],
                            ['group_vq7sw37[2]/Others_003',
                             "${group_vq7sw37[2]/What_pre_treatment_stages_are} = 'kitchen_grease' or ${group_vq7sw37[2]/What_pre_treatment_stages_are} = 'oil_skimmer' or ${group_vq7sw37[2]/What_pre_treatment_stages_are} = 'screen_with_ma' or ${group_vq7sw37[2]/What_pre_treatment_stages_are} = 'screen_with_me' or ${group_vq7sw37[2]/What_pre_treatment_stages_are} = 'grit_removal' or ${group_vq7sw37[2]/What_pre_treatment_stages_are} = 'grease_trap_at' or ${group_vq7sw37[2]/What_pre_treatment_stages_are} = 'integrated_gri' or ${group_vq7sw37[2]/What_pre_treatment_stages_are} = 'other'"],
                            ['group_vq7sw37[3]/Others_003',
                             "${group_vq7sw37[3]/What_pre_treatment_stages_are} = 'kitchen_grease' or ${group_vq7sw37[3]/What_pre_treatment_stages_are} = 'oil_skimmer' or ${group_vq7sw37[3]/What_pre_treatment_stages_are} = 'screen_with_ma' or ${group_vq7sw37[3]/What_pre_treatment_stages_are} = 'screen_with_me' or ${group_vq7sw37[3]/What_pre_treatment_stages_are} = 'grit_removal' or ${group_vq7sw37[3]/What_pre_treatment_stages_are} = 'grease_trap_at' or ${group_vq7sw37[3]/What_pre_treatment_stages_are} = 'integrated_gri' or ${group_vq7sw37[3]/What_pre_treatment_stages_are} = 'other'"],
                            ['group_a1b1c1[3]/TestColumnB',
                             "${group_a1b1c1[3]/TestColumnA} = '' and ${group_a1b1c1[3]/TestColumnC} >= 'hahaha' or ${Project_code} !=  'huhu'"],
                            ['group_a1b1c1[5]/TestColumnB',
                             "${group_a1b1c1[5]/TestColumnA} = '' and ${group_a1b1c1[5]/TestColumnC} >= 'hahaha' or ${Project_code} !=  'huhu'"]])
        self.assertTrue(np.all(l == expect))

        
class TestSurvey(TestCase):
    
    def setUp(self):
        self.form = FormDef('data/DOB_F3.xls')
        self.surv = Survey('data/DOB_F3_2017_03_01_compact.csv',
                           'data/DOB_F3.xls' )
        print('')

    def test__get_column(self):
        res = self.surv._get_column('Names_of_interviewers')
        self.assertEqual(res[19], 'rohan')
        self.assertEqual(res[17], 'rohan other')
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

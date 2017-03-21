#_*_ coding: utf-8 _*_

from unittest import TestCase
from kobopost.mark_skipped import FormDef, Survey
import os
import sys
import pandas as pd
import numpy as np


pd.options.display.max_colwidth = 200

modpath = os.path.split(os.path.dirname(sys.modules[__name__].__file__))[0]
datapath = os.path.join(os.path.split(modpath)[0], 'data')

class TestFormDef(TestCase):

    def setUp(self):
        self.form = FormDef(os.path.join(datapath, 'DOB_F3.xls'))
        self.surv = Survey(os.path.join(datapath, 'DOB_F3_2017_03_07_08_14_30.xlsx'),
                           os.path.join(datapath, 'DOB_F3.xls'))
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
        with self.assertLogs(level='WARNING'):
            conds = self.form._check_colnames(conds)
        self.assertNotIn(15, conds)
        self.assertEqual(len(conds), 248)

    def test__elim_condition_loops(self):
        self.form = FormDef(os.path.join(datapath, 'Test_Formdef_Loops_Cond.xls'))
        self.form._elim_condition_loops()
        self.assertEqual(self.form.form.loc[73, 'relevant'], '')
        self.assertEqual(self.form.form.loc[74, 'relevant'],
                         "${Is_the_sludge_that_is_removed_} = 'yes'")
        lastcond = self.form.form.loc[75, 'relevant'].split(' and ')[-1]
        self.assertEqual(lastcond, "${Is_the_sludge_that_is_removed_} = 'yes'")
        
    def test_mk_loopgrouping(self):
        self.form = FormDef(os.path.join(datapath, 'Test_Formdef_Loops.xls'))
        self.surv = Survey(os.path.join(datapath, 'DOB_F3_2017_03_07_08_14_30.xlsx'),
                           os.path.join(datapath, 'Test_Formdef_Loops.xls'))
        self.form.mk_loopgrouping(self.surv)
        l = self.form.form.loc[5, ['name', 'relevant']].values
        expect = np.array([['group_vq7sw37[1]/Others_003',
                            ("${group_vq7sw37[1]/What_pre_treatment_stages_are} = 'kitchen_grease' or ${group_vq7sw37[1]/What_pre_treatment_stages_are} = 'oil_skimmer' or ${group_vq7sw37[1]/What_pre_treatment_sta"
                             "ges_are} = 'screen_with_ma' or ${group_vq7sw37[1]/What_pre_treatment_stages_are} = 'screen_with_me' or ${group_vq7sw37[1]/What_pre_treatment_stages_are} = 'grit_removal' or ${group_vq7s"
                             "w37[1]/What_pre_treatment_stages_are} = 'grease_trap_at' or ${group_vq7sw37[1]/What_pre_treatment_stages_are} = 'integrated_gri' or ${group_vq7sw37[1]/What_pre_treatment_stages_are} = '"
                             "other'")],
                           ['group_vq7sw37[2]/Others_003',
                            ("${group_vq7sw37[2]/What_pre_treatment_stages_are} = 'kitchen_grease' or ${group_vq7sw37[2]/What_pre_treatment_stages_are} = 'oil_skimmer' or ${group_vq7sw37[2]/What_pre_treatment_sta"
                             "ges_are} = 'screen_with_ma' or ${group_vq7sw37[2]/What_pre_treatment_stages_are} = 'screen_with_me' or ${group_vq7sw37[2]/What_pre_treatment_stages_are} = 'grit_removal' or ${group_vq7s"
                             "w37[2]/What_pre_treatment_stages_are} = 'grease_trap_at' or ${group_vq7sw37[2]/What_pre_treatment_stages_are} = 'integrated_gri' or ${group_vq7sw37[2]/What_pre_treatment_stages_are} = '"
                             "other'")],
                           ['group_vq7sw37[3]/Others_003',
                            ("${group_vq7sw37[3]/What_pre_treatment_stages_are} = 'kitchen_grease' or ${group_vq7sw37[3]/What_pre_treatment_stages_are} = 'oil_skimmer' or ${group_vq7sw37[3]/What_pre_treatment_sta"
                             "ges_are} = 'screen_with_ma' or ${group_vq7sw37[3]/What_pre_treatment_stages_are} = 'screen_with_me' or ${group_vq7sw37[3]/What_pre_treatment_stages_are} = 'grit_removal' or ${group_vq7s"
                             "w37[3]/What_pre_treatment_stages_are} = 'grease_trap_at' or ${group_vq7sw37[3]/What_pre_treatment_stages_are} = 'integrated_gri' or ${group_vq7sw37[3]/What_pre_treatment_stages_are} = '"
                             "other'")],
                           ['group_vq7sw37[4]/Others_003',
                            ("${group_vq7sw37[4]/What_pre_treatment_stages_are} = 'kitchen_grease' or ${group_vq7sw37[4]/What_pre_treatment_stages_are} = 'oil_skimmer' or ${group_vq7sw37[4]/What_pre_treatment_sta"
                             "ges_are} = 'screen_with_ma' or ${group_vq7sw37[4]/What_pre_treatment_stages_are} = 'screen_with_me' or ${group_vq7sw37[4]/What_pre_treatment_stages_are} = 'grit_removal' or ${group_vq7s"
                             "w37[4]/What_pre_treatment_stages_are} = 'grease_trap_at' or ${group_vq7sw37[4]/What_pre_treatment_stages_are} = 'integrated_gri' or ${group_vq7sw37[4]/What_pre_treatment_stages_are} = '"
                             "other'")]])

        self.assertTrue(np.all(l == expect))

        
class TestSurvey(TestCase):
    
    def setUp(self):
        self.form = FormDef(os.path.join(datapath, 'DOB_F3.xls'))
        self.surv = Survey(os.path.join(datapath, 'DOB_F3_2017_03_07_08_14_30.xlsx'),
                           os.path.join(datapath, 'DOB_F3.xls'))
        print('')

    def test_read_workbook(self):
        res = self.surv._read_workbook()
        self.assertEqual(set([d.shape for d in res[0].values()]),
                         set([(132, 257), (114, 10)]))
        self.assertEqual(res[1], ['uploaded_form_dkhgoz', 'group_vq7sw37'])

    def test__massage_group_tables(self):
        res = self.surv._massage_group_tables()
        self.assertEqual(list(res.keys()), ['group_vq7sw37'])
        self.assertEqual(res['group_vq7sw37']
                         .loc[126, ['group_vq7sw37[1]/What_pre_treatment_stages_are',
	                            'group_vq7sw37[2]/What_pre_treatment_stages_are',
	                            'group_vq7sw37[3]/What_pre_treatment_stages_are',
	                            'group_vq7sw37[4]/What_pre_treatment_stages_are',
	                            'group_vq7sw37[1]/Others_003',
                                    'group_vq7sw37[2]/Others_003',
                                    'group_vq7sw37[3]/Others_003',
                                    'group_vq7sw37[4]/Others_003']].tolist(),
	                 ['screen_with_ma', 'grit_removal', 'grease_trap_at',
                          'none', 'Ready made steel screen fixed',
                          'Civil constructed', 'Civil constructed', ''])

    def test_join_main_and_groups(self):
        res = self.surv.quest
        self.assertEqual(res.shape, (132, 265))
        self.assertTrue(all([c in res.columns for c in [
            'group_vq7sw37[1]/What_pre_treatment_stages_are',
            'group_vq7sw37[2]/What_pre_treatment_stages_are',
            'group_vq7sw37[3]/What_pre_treatment_stages_are',
            'group_vq7sw37[4]/What_pre_treatment_stages_are',
            'group_vq7sw37[1]/Others_003', 'group_vq7sw37[2]/Others_003',
            'group_vq7sw37[3]/Others_003', 'group_vq7sw37[4]/Others_003']]))
        
    def test__get_column(self):
        res = self.surv._get_column('Names_of_interviewers')
        self.assertEqual(res[20], 'rohan')
        self.assertEqual(res[18], 'rohan other')
        self.assertEqual(len(res), 132)

    def test__check_selected(self):
        column = self.surv._get_column('Names_of_interviewers')
        isselected = self.surv._check_selected(column, 'other')
        self.assertEqual(list(isselected[8:20]),
                         [True, True, True, True, False,
                          False, False, True, False, True, False, False])
        
    def test_eval_skiprules(self):
        skip = self.surv.eval_skiprules()
        col = 'Others_003_001_001'
        self.assertEqual(skip[col][skip[col]].index.tolist(),
                         [3, 63, 70, 71, 99])
    
    def test_write_new_questionaire(self):
        self.surv.write_new_questionaire('DOB_F3_result.csv', 'NA', False)

    def test__insert_question_row(self):
        form = self.surv._mk_final_table('NA')
        res = self.surv._insert_question_row(form)
        qf = list(self.form.form['label'])
        self.assertTrue(all([q in qf for q in res.loc[0,:] if q != '']))


    

#!/bin/env python3
# _*_ coding: utf-8 _*_

import pandas as pd
import numpy as np
import re
import logging
from parser import XLSFormParser
from parser import XLSFormLexer

logger = logging.getLogger(__name__)

class FormDef(object):
    """Represents a KoBoToolbox - form definition"""

    def __init__(self, formname):
        self.form = pd.read_excel(formname)
        self.P = XLSFormParser()
        self.L = XLSFormLexer()

    def _check_colnames(self, conds):
        "check for non-strings in 'name' - column"
        wrong = conds[[not isinstance(n, str) for n in conds.name]]
        if not wrong.empty:
            logger.warn('bad columnname in "name":\n{}\n--> dropping'.format(wrong))
            conds.drop(wrong.index, inplace=True)
        return conds
    
    def read_skipconditions(self):
        conds = self.form.loc[:,('name', 'relevant')]
        conds = self._check_colnames(conds)
        conds = conds[(pd.notnull(conds.relevant))]
        conds.relevant = conds.relevant.map(self.P.parse)
        return conds

       
class Survey(object):
    """Represents a KoBoToolbox Questionaire.

    We assume that it was downloaded using
    "Download" -> "CSV" -> "Advanced Export", with
    "DON'T split select multiple choice answers into separate columns" checked.

    """

    def __init__(self, surveyname, formname):
        self.quest = pd.read_csv(surveyname)
        self.F = FormDef(formname)
        self.skiprules = self.F.read_skipconditions()

    def _get_column(self, colname):
        "returns series of lists for cells in colname"
        column = self.quest.loc[:, colname].map(lambda x: x.split())
        return(column.reset_index(drop=True))

    def _check_selected(self, column, val):
        "check whether val in values"
        return column.map(lambda x: val in x).reset_index(drop=True)

    def _expand_groups(self):
        "expands skiprules table for prefixed 'groups'"
        print(self.quest.columns)
        print(self.quest.columns.map(
            lambda x: re.match('(group_.+\[\d+\])/(.+)', x)))
        


        
    
    def eval_skiprules(self):
        '''Returns a DataFrame with relevant columns
        that contain boolean indicator whether cell
        was skipped or not.

        ''' 
        get_column = self._get_column
        check_selected = self._check_selected
        logical_or = np.logical_or
        logical_and = np.logical_and
        logical_not = np.logical_not
        skip = pd.DataFrame()
        return(self.skiprules)
        # for i, row in self.skiprules.iterrows():
        #     print(eval(row['relevant']))
        #  self.skiprules['rule'] = self.skiprules.apply(
        #     lambda row: eval(row['relevant']), axis=1)
        # print(self.skiprules)
            #skip[col] = eval(rule)

        # case1 = self.skiprules.iloc[0,:]
        # colname, rule = case1
        # result = eval(rule)
        # print(colname)
        # print(rule)
        # print(result)
        
        



        def check_selected(self, values, val):

            pass
        
        

    






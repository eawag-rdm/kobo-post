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

    ## continue here
    def eval_skiprules(self):
        def get_column(colname):
            "returns list of list of values for cells in colname"
            pass

        def check_selected(self, values, val):
            "check whether val in values"
            pass
        
        

    






#!/bin/env python3
# _*_ coding: utf-8 _*_

import pandas as pd
import numpy as np
import re

class FormDef(object):
    """Represents a KoBoToolbox - form definition"""

    def __init__(self, filename):
        self.form = pd.read_excel(filename)
        #self._mkpatterns()
        # self.relpat, self.selectpat = self._mkpatterns()

    # def _mkpatterns(self):
    #     colpat = r'\$\{(?P<colname>.+?)\}'
    #     reloppat = r' *(?P<relop>=|!=|>|<|<=|>=) *'
    #     valpat = r'(?P<val>.+)'
    #     relpat = r'(?P<relation>' + colpat + reloppat + valpat + ')'
    #     selectpat = r'(?P<selection>' + r'selected\(' + colpat + r' *, *' \
    #                 + valpat + r'\))'
    #     termpat = r'(' + relpat + r'|' + selectpat + r')'
        ## unfinished ##

    def getconditions(self):
        return self.form['relevant']
    

       
class Survey(object):
    """Represents a KoBoToolbox Questionaire.

    We assume that it was downloaded using
    "Download" -> "CSV" -> "Advanced Export", with
    "DON'T split select multiple choice answers into separate columns" checked.

    """

    def __init__(self, filename):
        self.quest = pd.read_csv(filename)





formname = '../data/DOB_F3.xls'
sname = '../data/DOB_F3_2017_03_01_compact.csv'
f = FormDef(formname)
s = Survey(sname)



         
        
        

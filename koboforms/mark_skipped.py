#!/bin/env python3
# _*_ coding: utf-8 _*_

import pandas as pd
import numpy as np
import re

class FormDef(object):
    """Represents a KoBoToolbox - form definition"""

    def __init__(self, filename):
        self.form = pd.read_excel(filename)
  
    def mk_skipconditions(self):
        self.form
    

       
class Survey(object):
    """Represents a KoBoToolbox Questionaire.

    We assume that it was downloaded using
    "Download" -> "CSV" -> "Advanced Export", with
    "DON'T split select multiple choice answers into separate columns" checked.

    """

    def __init__(self, filename):
        self.quest = pd.read_csv(filename)

    






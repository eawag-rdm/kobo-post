#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
"""mark_skipped.py

Usage:
  mark_skipped.py <questionaire> <form_definition>

""" 

from docopt import docopt
import pandas as pd
import numpy as np
import re
import os
import logging
from parser import XLSFormParser
from parser import XLSFormLexer

logger = logging.getLogger(__name__)

class FormDef(object):
    """Represents a KoBoToolbox - form definition"""

    def __init__(self, formname):
        self.form = pd.read_excel(formname, na_values=None, keep_default_na=[]).applymap(lambda x: str(x))
        self.P = XLSFormParser()
        self.L = XLSFormLexer()
        self.prefixpat = r'(group_\S+\[\d+\]/)'

    def _check_colnames(self, conds):
        "check for empty strings in 'name' - column"
        wrong = conds[conds.name == '']
        if not wrong.empty:
            logger.warn('bad columnname in "name":\n{}\n--> dropping'.format(wrong))
            conds.drop(wrong.index, inplace=True)
        return conds

    def mk_loopgrouping(self, survey):
        """Modifies the form description to explicitly define
        columns defines in loops over groups and the respective conditions.
        
        """ 
        def get_replacement_rules(groupname, oldrule, colnam, prefixes):
            """Create a sub-dataframe that contains the group specific
            replacement definition/conditions.

            """
            repdf = pd.DataFrame()
            # create new columnname / condition pairs
            for p in prefixes:
                newrule = oldrule.copy(deep=True)
                newrule.set_value('name', p + colnam)
                newcondition = newrule['relevant']
                # find and replace prefixed columns in condition
                for cn in loopdict[groupname]['colnames']:
                    newcondition = newcondition.replace(cn, p + cn)
                repdf = repdf.append(newrule.set_value('relevant', newcondition))
            return(repdf)

        def collect_loop_info():
            """Gather info about columnames defined in repeat-loops"""
            idxstart = self.form.loc[self.form['type'] == 'begin repeat',:].index
            idxend = self.form.loc[self.form['type'] == 'end repeat',:].index
            indexranges = [range(a+1, b) for a, b in zip(idxstart, idxend)] 
            groups = [self.form.loc[i, 'name'] for i in idxstart]
            colnamegroups = [self.form.loc[a+1:b-1, 'name']
                             for a, b in zip(idxstart, idxend)]
            assert(len(idxstart) == len(idxend) == len(groups))

            loopdict = {groups[i]: {'indices': list(indexranges[i]),
                                    'colnames': list(colnamegroups[i])}
                        for i in range(0, len(groups))}
            indexdict = {idx: grp
                         for i, grp in enumerate(groups)
                         for idx in indexranges[i]}
            return (loopdict, indexdict)

        def get_rules_in_loops_by_idx(indexdict):
            "find conditional rows in repeat-loops"
            idx_relevant = self.form.loc[pd.notnull(self.form.relevant)].index
            idx_relevant = [i for i in idx_relevant if i in indexdict]
            return idx_relevant
        
        def expand_form(idx, indexdict):
            "expands one rule at idx in a loop"
            groupname = indexdict[idx]
            oldrule = self.form.loc[idx,:]
            colnam = oldrule['name']
            prefixes = []
            for mat in [re.match(self.prefixpat + colnam, c)
                        for c in survey.get_columnnames()]:
                if mat:
                    prefixes.append(mat.group(1))
            repdf = get_replacement_rules(groupname, oldrule, colnam, prefixes)
            # replace the old rule - line with new ones
            self.form = self.form.drop(idx)
            self.form =self.form.append(repdf)

        loopdict, indexdict = collect_loop_info()
        idx_relevant = get_rules_in_loops_by_idx(indexdict)
        for idx in idx_relevant:
            expand_form(idx, indexdict)
        
    def read_skipconditions(self):
        conds = self.form.loc[:,('name', 'relevant')]
        conds = self._check_colnames(conds)
        conds = conds[conds.relevant != '']
        conds.relevant = conds.relevant.map(self.P.parse)
        return conds

       
class Survey(object):
    """Represents a KoBoToolbox Questionaire.

    We assume that it was downloaded using
    "Download" -> "CSV" -> "Advanced Export", with
    "DON'T split select multiple choice answers into separate columns" checked.

    """

    def __init__(self, surveyname, formname):
        ftyp = os.path.splitext(surveyname)[1].upper()
        if ftyp == '.CSV':
            self.quest = pd.read_csv(surveyname)
        elif ftyp in ['.XLS', '.XLSX']:
            self.quest = pd.read_excel(surveyname, na_values=[], keep_default_na=False).applymap(lambda x: str(x))
        else:
            raise(Exception('No valid file extension for {}'.format(surveyname)))
        self.F = FormDef(formname)
        self._repl_na()

    def _repl_na(self):
        "replace n/a with empty string"
        self.quest.replace(to_replace='n/a', value='', inplace=True)
        
    def _get_column(self, colname):
        "returns series of lists for cells in colname"
        column = self.quest.loc[:, colname]
        return column

    def _check_selected(self, column, val):
        "check whether val in values"
        return column.map(lambda x: val in x.split()).reset_index(drop=True)

    def get_columnnames(self):
        return self.quest.columns
    
    def eval_skiprules(self):
        '''Returns a DataFrame with relevant columns
        that contain boolean indicator whether cell
        was skipped or not.

        '''
        # fix loops in FormDef object
        self.F.mk_loopgrouping(self)
        # get skiprules
        self.skiprules = self.F.read_skipconditions()
        # define functionnames for evaluation of skiprules
        get_column = self._get_column
        check_selected = self._check_selected
        logical_or = np.logical_or
        logical_and = np.logical_and
        logical_not = np.logical_not

        skip = pd.DataFrame()
        for i, row in self.skiprules.iterrows():
            skip[row['name']] = eval(row['relevant']).apply(lambda x: not x)
        return(skip)

    def write_new_questionaire(self, outpath):
        skip = self.eval_skiprules()
        # same axis-0 count?
        assert(skip.shape[0] == self.quest.shape[0])
        # same index?
        assert(all(skip.index == self.quest.index))
        # all columns in skip also in original quest?
        missingcols = list(set(skip.columns) - set(self.quest.columns))
        if len(missingcols) > 0:
            logger.warn('Columns in form definition '
                        'that do not appear in survey:\n{}'
                        .format(missingcols))
        # indices are the same?
        assert(all(skip.index == self.quest.index))
        # apply the skipped - marker
        newform = self.quest.copy(deep = True)
        for colname in skip.columns:
            newform[colname] = newform.where(np.logical_not(skip[colname]),
                                             other='_SKIPPED_')
        # check skipped values where 'n/a' or ''
        isempty = np.logical_or(self.quest == '', self.quest == 'n/a')
        isskipped = newform == '_SKIPPED_'
        assert(all(isskipped == isempty))
        # convert '' to 'NA'
        newform.replace(to_replace='', value='NA', inplace=True)
        with open(outpath, 'w') as f:
            newform.to_csv(f, index=False, line_terminator='\r\n')

def main():
    arguments = docopt(__doc__, help=True)
    surv = Survey(arguments['<questionaire>'], arguments['<form_definition>'])
    base, ext = os.path.splitext(arguments['<questionaire>'])
    outpath = base + '_SKIP' + '.csv'
    surv.write_new_questionaire(outpath)

if __name__ == '__main__':
    main()
        

        

        

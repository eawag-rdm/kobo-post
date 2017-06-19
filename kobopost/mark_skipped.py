# _*_ coding: utf-8 _*_

"""Usage:
mark_skipped [options] <questionaire> <form_definition> <outpath>
mark_skipped (-h | --help)

Processes <questionaire>, an xlsx-file, based on <form_definition>, an xls file,
and writes the output to an apropriately named file in <outpath>

Options:
-h --help                 This help.
--na=<na_marker>          The string empty cells are replaced with [default: NA].
--format=<output_format>  Recognized formats are "XLSX" and "CSV" [default: CSV].
--fullquestions           Write a second header row that contains the full questions ("labels").
--keepnotes               Do not delete columns that represent "notes" instead of questions.

""" 
from docopt import docopt
import pandas as pd
import numpy as np
import re
import os
import sys
import logging
from .parser import XLSFormParser
from .parser import XLSFormLexer

logger = logging.getLogger(__name__)

class FormDef(object):
    """Represents a KoBoToolbox - form definition"""

    def __init__(self, formname):
        self.form = pd.read_excel(formname, na_values=None,
                                  keep_default_na=[]).applymap(lambda x: str(x))
        self.P = XLSFormParser()
        self.L = XLSFormLexer()
        self.prefixpat = r'(\S+(?:\[\d+\])?/)'

    def get_form(self):
        """returns the current formdef dataframe"""
        return self.form

    def _check_colnames(self, conds):
        "check for empty strings in 'name' - column"
        wrong = conds[conds.name == '']
        if not wrong.empty:
            logger.warning('bad columnname in "name":\n{}\n--> dropping'
                        .format(wrong))
            conds.drop(wrong.index, inplace=True)
        return conds

    def _elim_condition_loops(self):
        """Puts conditions that are set for loops inside the loop"""
        idxstart = self.form.loc[self.form['type'] == 'begin repeat', :].index
        idxend = self.form.loc[self.form['type'] == 'end repeat',:].index
        # find condition loops
        condloopsstart = []
        for i, startidx in enumerate(idxstart):
            if self.form.loc[startidx, 'relevant'] != '':
                condloopsstart.append(i)
        indexranges = [range(a, b) for a, b in zip(idxstart[condloopsstart],
                                                   idxend[condloopsstart])]
        for ran in indexranges:
            condition = self.form.loc[ran[0], 'relevant']
            self.form.loc[ran[0], 'relevant'] = ''
            for i in range(ran[0]+1, ran[-1]+1):
                oldcond = self.form.loc[i, 'relevant']
                joinlist = [c for c in [oldcond, condition] if c != '']
                self.form.loc[i, 'relevant'] = ' and '.join(joinlist)

    def collect_loop_info(self):
        """Gather info about columnames defined in repeat-loops"""
        repeatstack = []
        groupstack = []
        groups = []
        for i, l in self.form.iterrows():
            print(i)
            if re.match('\s*begin\s+repeat', l.type):
                repeatstack.append({'start': i, 'type': 'repeat',
                              'name': l['name']})
            elif re.match('\s*begin\s+group', l.type):
                groupstack.append({'start': i, 'type': 'group',
                              'name': l['name']})
            elif re.match('\s*end\s+repeat', l.type):
                groups.append(repeatstack.pop())
                

                              groups.append(stack.pop())
                    groups[-1]['depth'] = len(stack)
                    groups[-1]['stop'] = i
        # idxstart = self.form.loc[self.form['type'] == 'begin repeat',:].index
        # idxend = self.form.loc[self.form['type'] == 'end repeat',:].index
        # indexranges = [range(a+1, b) for a, b in zip(idxstart, idxend)] 
        # groups = [self.form.loc[i, 'name'] for i in idxstart]
        # colnamegroups = [self.form.loc[a+1:b-1, 'name']
        #                  for a, b in zip(idxstart, idxend)]
        # assert(len(idxstart) == len(idxend) == len(groups))
        
        # loopdict = {groups[i]: {'indices': list(indexranges[i]),
        #                         'colnames': list(colnamegroups[i])}
        #             for i in range(0, len(groups))}
        # indexdict = {idx: grp
        #              for i, grp in enumerate(groups)
        #              for idx in indexranges[i]}
        # return (loopdict, indexdict)
        
    
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
        self._elim_condition_loops()
        loopdict, indexdict = self.collect_loop_info()
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

    def __init__(self, arguments):
        self.arguments = arguments
        self.surveyname = arguments['<questionaire>']
        self.data, self.sheetnames = self._read_workbook()
        self.quest = self.join_main_and_groups()
        self.F = FormDef(arguments['<form_definition>'])
        self.orig_formdef = self.F.get_form()

        self._repl_na()

    def _read_workbook(self):
        """reads all worksheets of an Excel file.
        first sheet is interpreted as 'main', others as
        partial results from groups.

        """
        data = {}
        with pd.ExcelFile(self.surveyname) as xls:
            sheets = xls.sheet_names
            data['main'] = pd.read_excel(
                xls, sheets[0], na_values=[],
                keep_default_na=False,
                index_col='_index').applymap(lambda x: str(x))
            for s in sheets[1:]:
                data[s] = pd.read_excel(
                    xls, s, na_values=[],
                    keep_default_na=False).applymap(lambda x: str(x))
                data[s]['_parent_index'] = pd.to_numeric(data[s]['_parent_index'])
        return([data, sheets])

    def _massage_group_tables(self):
        """parses group-tables into tables suited for joining
        with main table.

        """
        data = {key: self.data[key] for key in self.sheetnames[1:]}
        grouptables = {}
        for d in data:
            # get maximum number of group elements
            par_idxs = [int(i) for i in data[d]._parent_index.tolist()]
            nmax = max([par_idxs.count(x) for x in set(par_idxs)])
            newindices = list(set(par_idxs))
            # add groupcolumns
            groupcols = [c for c in data[d].columns if c[0] != '_']
            gcpairs = [c.split('/') for c in groupcols]
            newcols =  [d + '[' + str(i) + ']' + '/' + gc[1]
                        for gc in gcpairs for i in range(1, nmax + 1)]
            # new DataFrame
            newdf = pd.DataFrame(index=newindices, columns=newcols)
            # populate new df
            idxcount = {}
            for i, row in newdf.iterrows():
                newdict = {}
                gcount = 0
                partrows = data[d].loc[data[d]._parent_index == i, groupcols]
                for _, oldrow in partrows.iterrows():
                    ocpairs = [c.split('/') for c in oldrow[oldrow != ''].index]
                    gcount += 1
                    newdict.update({c[0]+'['+str(gcount)+']/'+c[1]:
                                    oldrow[c[0]+'/'+c[1]] for c in ocpairs})
    
                newdf.loc[i] = pd.Series(newdict)
            newdf = newdf.fillna('')
            grouptables[d] = newdf
        return(grouptables)

    def join_main_and_groups(self):
        grouptables = self._massage_group_tables()
        for gname, gtable in grouptables.items():
            self.data['main'] = pd.merge(
                self.data['main'],
                gtable,
                left_index=True,
                right_index=True,
                how='outer')
        return(self.data['main'])
            
    def _repl_na(self):
        "replace n/a with empty string"
        self.quest.replace(to_replace=['n/a', np.nan],
                           value=['', ''], inplace=True)
        
    def _get_column(self, colname):
        "returns series of lists for cells in colname"
        column = self.quest.loc[:, colname]
        return column

    def _check_selected(self, column, val):
        "check whether val in values"
        return column.map(lambda x: val in x.split())#.reset_index(drop=True)

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

    def _insert_question_row(self, form):
        """Inserts a second header row that contains the
        full questions ("labels")

        """
        mapdict = {i[1]['name']: i[1]['label']
               for i in self.F.form.loc[:,['name','label']].iterrows()}
        newrow = list(form.columns)
        newrow = [mapdict.get(x, '') for x in newrow]
        form.loc[0] = newrow
        form.sort_index(inplace=True)
        return form

    def _handle_notes(self, form):
        newform = form.copy(deep=True)
        # Column names that are "notes"
        notenames = self.F.form.loc[self.F.form['type'] == 'note', 'name']
        # check whether empty
        assert((self.quest.loc[:, notenames].values == '').all())
        if self.arguments['--keepnotes']:
            newform.loc[:, notenames] = '_NOTE_'
        else:
            newform.drop(notenames, axis=1, inplace=True)
        return newform

    def _mk_final_table(self):
        """Creates final table"""
        na_marker = self.arguments['--na']
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
            repcol = newform[colname].where(np.logical_not(skip[colname]),
                                            other='_SKIPPED_')
            newform[colname] = newform[colname].where(
                np.logical_not(skip[colname]), other='_SKIPPED_')
        # check skipped values where 'n/a' or ''
        isempty = self.quest == ''
        isskipped = newform == '_SKIPPED_'
        assert(all(isskipped == isempty))
        # Handle columns representing "notes"
        newform = self._handle_notes(newform)
        # convert '' to 'NA'
        newform.replace(to_replace='', value=na_marker, inplace=True)
        newform.fillna(value=na_marker, inplace=True)
        return newform

    def _re_sort_columns(self, form):
        """Puts "group"-columns into the position they appear in the form
        definition.
        
        """
        newform = form.copy(deep=True)
        formdefnames = self.orig_formdef.loc[:, 'name'] #names in form definition
        survcols = form.columns #columns names in survey
        grouppat = r'(?P<is_group>(?P<group_id>group_\w+)\[\d+\]/)?(?P<question>[\w/]+)'
        
        def fullmatchdict(mo):
            md = mo.groupdict()
            md.update({'match': mo.group(0)})
            return md
        
        survcolgroupmatch = [[pos, fullmatchdict(re.match(grouppat, c))]
                             for pos, c in enumerate(survcols)]
        
        def _move_group(survmatch, pos):
            # create hole in survcol - positions
            grouplen = len(survmatch)
            for s in survcolgroupmatch:
                s[0] = s[0] + grouplen if s[0] > pos else s[0]
            # move group questions
            survmatch.sort(key=lambda x: x[0])
            for gcol in survmatch:
                index = survcolgroupmatch.index(gcol)
                survcolgroupmatch[index][0] = pos+1
                pos += 1
            return pos

        pos = 0
        for nam in formdefnames:
            survmatch = [s for s in survcolgroupmatch if s[1]['question'] == nam]
            if len(survmatch) == 0:
                continue
            elif (not survmatch[0][1]['is_group']) and len(survmatch) == 1:
                pos = survmatch[0][0]
            elif survmatch[0][1]['is_group']:
                pos = _move_group(survmatch, pos)
            else:
                raise Exception('ERROR: Found multiple instances of {}'.format(nam))
        # new list of columnnames
        survcolgroupmatch.sort(key=lambda x: x[0])
        newcols = [x[1]['match'] for x in survcolgroupmatch]
        assert(set(list(survcols)) == set(newcols))
        # re-ordered form
        newform = newform[newcols]
        return newform
        
    def write_new_questionaire(self):
        base = os.path.splitext(self.arguments['<questionaire>'])[0]
        basename = os.path.basename(base)
        extension = self.arguments['--format'].lower()
        outpath = os.path.join(self.arguments['<outpath>'], basename + '.' + extension)

        newform = self._mk_final_table()
        if self.arguments['--fullquestions']:
            newform = self._insert_question_row(newform)
        newform = self._re_sort_columns(newform)
        ext = os.path.splitext(outpath)[1]
        if ext == '.csv':
            with open(outpath, 'w') as f:
                newform.to_csv(f, index=True, index_label='INDEX',
                               line_terminator='\r\n')
            
        elif ext == '.xlsx':
            newform.to_excel(outpath, index=True, sheet_name="Sheet1",
                             index_label='INDEX')
        else:
            raise NotImplementedError('Output format "{}" not recognized.'
                                      .format(ext[1:].upper()))
                

def main():
    arguments = docopt(__doc__, help=True) 
    surv = Survey(arguments)
    surv.write_new_questionaire()

if __name__ == '__main__':
    main()


       

        

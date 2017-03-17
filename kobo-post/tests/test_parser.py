# _*_ coding: utf-8 _*_

from unittest import TestCase
from ply.lex import LexError
from ply.yacc import GrammarError
from parser import XLSFormLexer, XLSFormParser

class TestParser(TestCase):

    def setUp(self):
        self.L = XLSFormLexer()
        self.P = XLSFormParser()
        self.tconds = ["${Is_the_system_operational} = 'yes'",
                       "${Extensive_plant_growth_in_disc} = 'no_plant_growth' " + \
                       "or ${Extensive_plant_growth_in_disc}= 'yes__but_normal' " + \
                       "or ( ${Extensive_plant_growth_in_dis} = 'yes__remarkable_p" + \
                       "lant_growth' and 'hullu' = 'hullu')",
                       "selected(${ What_could_be_the_reason_Any_ }, 'other_reason')",
                       "illegal = 'yes'",
                       "'leftside' = [holla]"]
        self.perrors = ["'yes' 'no'", "and 'yes'"]
        self.partest = ["'one' = '1' and 'two' > '0' or 'three' <= '9'",
                        "'one' = '1' and ('two' > '0' or 'three' <= '9')",
                        "'one' = '1' and not 'two' > '0' or 'three' <= '9'",
                        "'one' = '1' and not ('two' > '0' or 'three' <= '9')"]
        
        self.partestres = [("logical_or(logical_and(('one' == '1'), ('two' > "
                            "'0')), ('three' <= '9'))"),
                           ("logical_and(('one' == '1'), logical_or(('two' > '"
                            "0'), ('three' <= '9')))"),
                           ("logical_or(logical_and(('one' == '1'), logical_not"
                            "(('two' > '0'))), ('three' <= '9'))"),
                           ("logical_and(('one' == '1'), logical_not(logical_or"
                            "(('two' > '0'), ('three' <= '9'))))")]

        self.lexres = [[('COLUMN','${Is_the_system_operational}',1,0),
                        ('EQUAL','==',1,29),
                        ('STRINGLIT',"'yes'",1,31)],
                       [('COLUMN','${Extensive_plant_growth_in_disc}',1,0),
                        ('EQUAL','==',1,34),
                        ('STRINGLIT',"'no_plant_growth'",1,36),
                        ('OR','or',1,54),
                        ('COLUMN','${Extensive_plant_growth_in_disc}',1,57),
                        ('EQUAL','==',1,90),
                        ('STRINGLIT',"'yes__but_normal'",1,92),
                        ('OR','or',1,110),
                        ('LPAREN','(',1,113),
                        ('COLUMN','${Extensive_plant_growth_in_dis}',1,115),
                        ('EQUAL','==',1,148),
                        ('STRINGLIT',"'yes__remarkable_plant_growth'",1,150),
                        ('AND','and',1,181),
                        ('STRINGLIT',"'hullu'",1,185),
                        ('EQUAL','==',1,193),
                        ('STRINGLIT',"'hullu'",1,195),
                        ('RPAREN',')',1,202)],
                       [('SELECTED','selected',1,0),
                        ('LPAREN','(',1,8),
                        ('COLUMN','${ What_could_be_the_reason_Any_ }',1,9),
                        (',',',',1,43),
                        ('STRINGLIT',"'other_reason'",1,45),
                        ('RPAREN',')',1,59)]]

    def test_lexer(self):
        for i, ts in enumerate(self.tconds[0:3]):
            self.L.input(ts)
            for n, tok in enumerate(self.L):
                self.assertEqual(
                    (tok.type, tok.value, tok.lineno,tok.lexpos),
                    self.lexres[i][n])
        self.L.input(self.tconds[3])
        with self.assertRaises(LexError):
            for tok in self.L:
                pass
        self.L.input(self.tconds[4])
        with self.assertRaises(LexError):
            for tok in self.L:
                pass
         

    def test_parser(self):
        for i, ts in enumerate(self.partest):
            self.assertEqual(self.P.parse(ts), self.partestres[i])
        for pe in self.perrors[0:2]:
            with self.assertRaises(GrammarError):
                self.P.parse(pe)

# _*_ coding: utf-8 _*_

from unittest import TestCase
from lexer import XLSFormLexer, XLSFormParser

class TestLexer(TestCase):

    def setUp(self):
        self.L = XLSFormLexer()
        self.P = XLSFormParser()
        self.tconds = ["${Is_the_system_operational} = 'yes'",
                       "${Extensive_plant_growth_in_disc} = 'no_plant_growth' " + \
                       "or ${Extensive_plant_growth_in_disc} = 'yes__but_normal' " + \
                       "or (${Extensive_plant_growth_in_disc} = 'yes__remarkable_p" + \
                       "lant_growth' and 'hullu' = 'hullu')",
                       "selected(${What_could_be_the_reason_Any_}, 'other_reason')"]

    def test_lexer(self):
 
        for ts in self.tconds:
            print('')
            print("TESTSTRING:")
            print(ts)
            print('')
            self.L.input(ts)
            while True:
                tok = self.L.token()
                if not tok:
                    break
                print(tok)

    def test_parser(self):
        for ts in self.tconds:
            print('')
            print("TESTSTRING:")
            print(ts)
            print('')
            res = self.P.parse(ts)
            print(res)
        
        

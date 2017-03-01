# _*_ coding: utf-8 _*_

import ply.lex as lex
import ply.yacc as yacc

tokens0 = [
    'ID',
    'STRINGLIT',
    'LPAREN',
    'RPAREN',
    'COLUMN',
    'EQUAL',
    'NOTEQUAL',
    'LT',
    'LTEQ',
    'GT',
    'GTEQ'
]
    
reserved = {
    'selected': 'SELECTED',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT'
}
        
tokens = tokens0 + list(reserved.values())

def XLSFormLexer():
    
    t_STRINGLIT = r"'(?P<string>[^']*)'"
    t_COLUMN = r'\$\{.+?\}'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_NOTEQUAL = r'!='
    t_LT = r'<'
    t_GT = r'>'
    t_LTEQ = r'<='
    t_GTEQ = r'>='
    t_ignore = ' \t'
    
    literals = [',']

    def t_EQUAL(t):
        r'='
        t.value = '=='
        return t
    
    def t_ID(t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = reserved.get(t.value, 'ID')
        return t
    
    def t_error(t):
        print("Illegal character '{}'".format(t.value))
        t.lexer.skip(1)

    return lex.lex()
 
####### Parser

def XLSFormParser():
    def p_boolex_andor(p):
        '''boolex : boolex AND boolex
                  | boolex OR boolex'''
        p[0] = ' '.join([p[1], p[2], p[3]])

    def p_boolex_not(p):
        '''boolex : NOT boolex'''
        p[0] = ' '.join(['not', p[2]])

    def p_boolex_par(p):
        '''boolex : LPAREN boolex RPAREN'''
        p[0] = ' '.join([p[1], p[2], p[3]])

    def p_boolex_term(p):
        '''boolex : term EQUAL term
                  | term NOTEQUAL term
                  | term GT term
                  | term GTEQ term
                  | term LT term
                  | term LTEQ term''' 
        p[0] = ' '.join([p[1], p[2], p[3]])

    def p_term_stringlit(p):
        '''term : STRINGLIT'''
        p[0] = p[1]


    def p_term_column(p):
        'term : COLUMN'
        p[0] = 'get_column(\'' + p[1][2:-1] + '\')'

    def p_boolex_select(p):
        '''boolex : SELECTED LPAREN term ',' term RPAREN'''
        p[0] = 'check_selected(' + p[3] + ', ' + p[5] + ')'

    return yacc.yacc(debug=False, write_tables=False)

    

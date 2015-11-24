__author__ = 'koo'

import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'ALPHABET', 'PLUS', 'TIMES',
    'LPAREN', 'RPAREN',
    )

t_PLUS = r'\+'
t_TIMES = r'\*'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ALPHABET = r'a|b|c|d|epsilon'

# Ignored characters
t_ignore = " \t"

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

precedence = (
    ('left','PLUS'),
    ('left', 'TIMES'),
    )

def p_expression_alphabet(t):
    'expression : ALPHABET'
    t[0] = (t[1])

def p_expression_plus(t):
    'expression : expression PLUS expression'
    t[0] = ('+', t[1], t[3])

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = (t[2])

def p_expression_concat(t):
    'expression : expression expression'
    t[0] = ('.', t[1], t[2])

def p_expression_closure(t):
    'expression : expression TIMES'
    t[0] = ('*', t[1])


def p_error(t):
    print("Syntax error at '%s'" % t.value)

parser = yacc.yacc()

while True:
    try:
        s = raw_input('re > ')   # Use raw_input on Python 2
    except EOFError:
        break
    result = parser.parse(s)
    print result

def parse_re():
    s = raw_input('re > ')   # Use raw_input on Python 2
    result = parser.parse(s)
    print result
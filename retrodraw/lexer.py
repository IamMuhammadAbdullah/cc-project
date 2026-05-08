import re
from typing import List, NamedTuple

class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int

class LexerError(Exception):
    pass

class Lexer:
    TOKEN_SPECIFICATION = [
        ('HEX_COLOR', r'#[0-9a-fA-F]{6}'),         
        ('NUMBER',    r'\d+'),                     
        ('KEYWORD',   r'\b(MOVE|TURN|COLOR|REPEAT)\b'), 
        ('OP',        r'[+\-*/]'),                 
        ('LBRACKET',  r'\['),                      
        ('RBRACKET',  r'\]'),                      
        ('LPAREN',    r'\('),                      
        ('RPAREN',    r'\)'),                      
        ('WS',        r'[ \t]+'),                  
        ('NEWLINE',   r'\n'),                      
        ('MISMATCH',  r'.'),                       
    ]

    def __init__(self, code: str):
        self.code = code
        self.tokens = []

    def tokenize(self) -> List[Token]:
        tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in self.TOKEN_SPECIFICATION)
        line_num = 1
        line_start = 0
        
        for mo in re.finditer(tok_regex, self.code):
            kind = mo.lastgroup
            value = mo.group()
            column = mo.start() - line_start + 1
            
            if kind == 'NUMBER':
                self.tokens.append(Token(kind, value, line_num, column))
            elif kind == 'HEX_COLOR':
                self.tokens.append(Token(kind, value, line_num, column))
            elif kind == 'KEYWORD':
                self.tokens.append(Token(value, value, line_num, column))
            elif kind == 'OP':
                op_map = {'+': 'PLUS', '-': 'MINUS', '*': 'MUL', '/': 'DIV'}
                self.tokens.append(Token(op_map[value], value, line_num, column))
            elif kind in ('LBRACKET', 'RBRACKET', 'LPAREN', 'RPAREN'):
                self.tokens.append(Token(kind, value, line_num, column))
            elif kind == 'NEWLINE':
                line_start = mo.end()
                line_num += 1
            elif kind == 'WS':
                pass 
            elif kind == 'MISMATCH':
                raise LexerError(f"Unexpected character '{value}' at line {line_num}, column {column}")
                
        self.tokens.append(Token('EOF', '', line_num, len(self.code) - line_start + 1))
        return self.tokens

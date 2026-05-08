import sys
import re
import argparse
from typing import List, NamedTuple

class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int

class LexerError(Exception):
    pass

class Lexer:
    # Token specification using regex
    TOKEN_SPECIFICATION = [
        ('HEX_COLOR', r'#[0-9a-fA-F]{6}'),         # e.g., #FF00FF
        ('NUMBER',    r'\d+'),                     # Integer numbers
        ('KEYWORD',   r'\b(MOVE|TURN|COLOR|REPEAT)\b'), # Keywords
        ('OP',        r'[+\-*/]'),                 # Arithmetic operators
        ('LBRACKET',  r'\['),                      # Loop start
        ('RBRACKET',  r'\]'),                      # Loop end
        ('WS',        r'[ \t]+'),                  # Match spaces and tabs
        ('NEWLINE',   r'\n'),                      # Line endings
        ('MISMATCH',  r'.'),                       # Any other character
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
                # The keyword is the token type itself (MOVE, TURN, etc.)
                self.tokens.append(Token(value, value, line_num, column))
            elif kind == 'OP':
                op_map = {'+': 'PLUS', '-': 'MINUS', '*': 'MUL', '/': 'DIV'}
                self.tokens.append(Token(op_map[value], value, line_num, column))
            elif kind == 'LBRACKET':
                self.tokens.append(Token(kind, value, line_num, column))
            elif kind == 'RBRACKET':
                self.tokens.append(Token(kind, value, line_num, column))
            elif kind == 'NEWLINE':
                line_start = mo.end()
                line_num += 1
            elif kind == 'WS':
                pass # Completely ignore whitespace
            elif kind == 'MISMATCH':
                # Robust Error Reporting with exact location
                raise LexerError(f"Unexpected character '{value}' at line {line_num}, column {column}")
                
        self.tokens.append(Token('EOF', '', line_num, len(self.code) - line_start + 1))
        return self.tokens

def setup_cli():
    # Setup robust CLI arguments as per requirements
    parser = argparse.ArgumentParser(description="RetroDraw Compiler - Translates .logo to executable Python Code.")
    parser.add_argument("input_file", help="Input .logo source code file to compile")
    parser.add_argument("-o", "--output", help="Output file for generated turtle code", default="output.py")
    parser.add_argument("--debug", action="store_true", help="Print debug outputs like Tokens stream and AST")
    return parser.parse_args()

def main():
    args = setup_cli()
    print(f"[+] Compiling RetroDraw source: '{args.input_file}' to '{args.output}'")
    
    try:
        with open(args.input_file, 'r') as f:
            code = f.read()
            
        # --- PHASE 1: LEXER ---
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        if args.debug:
            print("=== LEXER DEBUG: TOKEN STREAM ===")
            for tok in tokens:
                print(f"  {tok.type:10} | {tok.value:10} | Line {tok.line:3}: Col {tok.column:3}")
            print("=================================\n")
                
        # --- PHASE 2: PARSER (Pending) ---
        print("[*] Lexical analysis completed successfully.")
        
    except FileNotFoundError:
        print(f"Error: Source file '{args.input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except LexerError as e:
        print(f"Lexical Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

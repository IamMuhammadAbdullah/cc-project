from typing import List
from .lexer import Token

class ASTNode: pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class MoveC(ASTNode):
    def __init__(self, expr):
        self.expr = expr

class TurnC(ASTNode):
    def __init__(self, expr):
        self.expr = expr

class ColorC(ASTNode):
    def __init__(self, color_hex):
        self.color_hex = color_hex

class RepeatL(ASTNode):
    def __init__(self, count_expr, body):
        self.count_expr = count_expr
        self.body = body

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Number(ASTNode):
    def __init__(self, value, line, col):
        self.value = value
        self.line = line
        self.col = col

class HexColor(ASTNode):
    def __init__(self, value, line, col):
        self.value = value
        self.line = line
        self.col = col

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current_token(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]

    def consume(self, expected_type=None) -> Token:
        curr = self.current_token()
        if expected_type and curr.type != expected_type:
            raise ParserError(f"Expected token {expected_type} but got {curr.type} at line {curr.line}, col {curr.column}")
        self.pos += 1
        return curr

    def parse(self) -> Program:
        statements = []
        while self.current_token().type != 'EOF':
            statements.append(self.parse_statement())
        return Program(statements)

    def parse_statement(self) -> ASTNode:
        curr = self.current_token()
        if curr.type in ('MOVE', 'TURN', 'COLOR'):
            return self.parse_command()
        elif curr.type == 'REPEAT':
            return self.parse_loop()
        else:
            raise ParserError(f"Unexpected token {curr.type} ('{curr.value}') at line {curr.line}, col {curr.column}")

    def parse_command(self) -> ASTNode:
        cmd = self.consume()
        if cmd.type == 'MOVE':
            return MoveC(self.parse_expression())
        elif cmd.type == 'TURN':
            return TurnC(self.parse_expression())
        elif cmd.type == 'COLOR':
            color_tok = self.consume('HEX_COLOR')
            return ColorC(HexColor(color_tok.value, color_tok.line, color_tok.column))

    def parse_loop(self) -> RepeatL:
        self.consume('REPEAT')
        count_expr = self.parse_expression()
        self.consume('LBRACKET')
        body = []
        while self.current_token().type != 'RBRACKET':
            if self.current_token().type == 'EOF':
                raise ParserError("Unexpected EOF while parsing REPEAT loop. Missing ']'")
            body.append(self.parse_statement())
        self.consume('RBRACKET')
        return RepeatL(count_expr, body)

    def parse_expression(self) -> ASTNode:
        node = self.parse_term()
        while self.current_token().type in ('PLUS', 'MINUS'):
            tok = self.consume()
            node = BinOp(left=node, op=tok.type, right=self.parse_term())
        return node

    def parse_term(self) -> ASTNode:
        node = self.parse_factor()
        while self.current_token().type in ('MUL', 'DIV'):
            tok = self.consume()
            node = BinOp(left=node, op=tok.type, right=self.parse_factor())
        return node

    def parse_factor(self) -> ASTNode:
        tok = self.current_token()
        if tok.type == 'NUMBER':
            self.consume('NUMBER')
            return Number(int(tok.value), tok.line, tok.column)
        elif tok.type == 'LPAREN':
            self.consume('LPAREN')
            node = self.parse_expression()
            self.consume('RPAREN')
            return node
        elif tok.type in ('PLUS', 'MINUS'):
            # Allow unary minus/plus
            sign_tok = self.consume()
            factor = self.parse_factor()
            # Wrap as 0 +/- factor
            return BinOp(Number(0, sign_tok.line, sign_tok.column), sign_tok.type, factor)
            
        raise ParserError(f"Expected NUMBER or '(', got {tok.type} at line {tok.line}, col {tok.column}")

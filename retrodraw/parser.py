from typing import List
from .lexer import Token

class ASTNode: pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Program({self.statements})"

class MoveC(ASTNode):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f"Move({self.expr})"

class TurnC(ASTNode):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f"Turn({self.expr})"

class SetPosC(ASTNode):
    def __init__(self, x_expr, y_expr):
        self.x_expr = x_expr
        self.y_expr = y_expr

    def __repr__(self):
        return f"SetPos({self.x_expr}, {self.y_expr})"

class ColorC(ASTNode):
    def __init__(self, color):
        self.color = color

    def __repr__(self):
        return f"Color({self.color})"

class RectC(ASTNode):
    def __init__(self, x1_expr, y1_expr, x2_expr, y2_expr):
        self.x1_expr = x1_expr
        self.y1_expr = y1_expr
        self.x2_expr = x2_expr
        self.y2_expr = y2_expr

    def __repr__(self):
        return f"Rect({self.x1_expr}, {self.y1_expr}, {self.x2_expr}, {self.y2_expr})"

class RepeatL(ASTNode):
    def __init__(self, count_expr, body):
        self.count_expr = count_expr
        self.body = body

    def __repr__(self):
        return f"Repeat({self.count_expr}, {self.body})"

class IfOnColor(ASTNode):
    def __init__(self, color, body):
        self.color = color
        self.body = body

    def __repr__(self):
        return f"IfOnColor({self.color}, {self.body})"

class LetC(ASTNode):
    def __init__(self, name, expr, line, col):
        self.name = name
        self.expr = expr
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Let({self.name}, {self.expr})"

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinOp({self.left}, {self.op}, {self.right})"

class Number(ASTNode):
    def __init__(self, value, line, col):
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Number({self.value})"

class ColorLiteral(ASTNode):
    def __init__(self, value, line, col):
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return f"ColorLiteral({self.value})"

class Identifier(ASTNode):
    def __init__(self, name, line, col):
        self.name = name
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Identifier({self.name})"

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
        if curr.type in ('MOVE', 'TURN', 'SET_POS', 'COLOR', 'RECT', 'LET'):
            return self.parse_command()
        elif curr.type == 'REPEAT':
            return self.parse_loop()
        elif curr.type == 'IF':
            return self.parse_if()
        else:
            raise ParserError(f"Unexpected token {curr.type} ('{curr.value}') at line {curr.line}, col {curr.column}")

    def parse_command(self) -> ASTNode:
        cmd = self.consume()
        if cmd.type == 'MOVE':
            return MoveC(self.parse_expression())
        elif cmd.type == 'TURN':
            return TurnC(self.parse_expression())
        elif cmd.type == 'SET_POS':
            self.consume('LPAREN')
            x_expr = self.parse_expression()
            self.consume('COMMA')
            y_expr = self.parse_expression()
            self.consume('RPAREN')
            return SetPosC(x_expr, y_expr)
        elif cmd.type == 'COLOR':
            return ColorC(self.parse_color())
        elif cmd.type == 'RECT':
            self.consume('LPAREN')
            x1_expr = self.parse_expression()
            self.consume('COMMA')
            y1_expr = self.parse_expression()
            self.consume('RPAREN')
            self.consume('LPAREN')
            x2_expr = self.parse_expression()
            self.consume('COMMA')
            y2_expr = self.parse_expression()
            self.consume('RPAREN')
            return RectC(x1_expr, y1_expr, x2_expr, y2_expr)
        elif cmd.type == 'LET':
            name_tok = self.consume('IDENT')
            self.consume('ASSIGN')
            return LetC(name_tok.value, self.parse_expression(), name_tok.line, name_tok.column)

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

    def parse_if(self) -> IfOnColor:
        self.consume('IF')
        self.consume('ON_COLOR')
        color = self.parse_color()
        self.consume('LBRACKET')
        body = []
        while self.current_token().type != 'RBRACKET':
            if self.current_token().type == 'EOF':
                raise ParserError("Unexpected EOF while parsing IF ON_COLOR block. Missing ']'")
            body.append(self.parse_statement())
        self.consume('RBRACKET')
        return IfOnColor(color, body)

    def parse_color(self) -> ColorLiteral:
        tok = self.current_token()
        if tok.type == 'HEX_COLOR':
            self.consume('HEX_COLOR')
            return ColorLiteral(tok.value, tok.line, tok.column)
        if tok.type == 'IDENT':
            self.consume('IDENT')
            return ColorLiteral(tok.value, tok.line, tok.column)
        raise ParserError(f"Expected color literal, got {tok.type} at line {tok.line}, col {tok.column}")

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
            return Number(tok.value, tok.line, tok.column)
        elif tok.type == 'IDENT':
            self.consume('IDENT')
            return Identifier(tok.value, tok.line, tok.column)
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
            
        raise ParserError(f"Expected NUMBER, identifier, or '(', got {tok.type} at line {tok.line}, col {tok.column}")

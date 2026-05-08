from .parser import *

class SemanticError(Exception):
    pass

class SemanticAnalyzer:
    VALID_COLORS = {
        'RED', 'GREEN', 'BLUE', 'BLACK', 'WHITE',
        'YELLOW', 'CYAN', 'MAGENTA', 'GRAY', 'ORANGE',
        'PURPLE', 'PINK',
    }

    def __init__(self):
        self.symbol_table = {}
        self.turtle_state = {
            'position': (0, 0),
            'heading': 0,
            'pen_color': 'BLACK',
        }

    def analyze(self, node: ASTNode):
        if isinstance(node, Program):
            for stmt in node.statements:
                self.analyze(stmt)
        elif isinstance(node, RepeatL):
            self.analyze(node.count_expr)
            value = self.constant_value(node.count_expr)
            if value is not None and (value < 0 or int(value) != value):
                raise SemanticError("REPEAT count must be a non-negative integer")
            for stmt in node.body:
                self.analyze(stmt)
        elif isinstance(node, IfOnColor):
            self.analyze(node.color)
            for stmt in node.body:
                self.analyze(stmt)
        elif isinstance(node, MoveC) or isinstance(node, TurnC):
            self.analyze(node.expr)
        elif isinstance(node, SetPosC):
            self.analyze(node.x_expr)
            self.analyze(node.y_expr)
        elif isinstance(node, ColorC):
            self.analyze(node.color)
            self.turtle_state['pen_color'] = node.color.value
        elif isinstance(node, RectC):
            self.analyze(node.x1_expr)
            self.analyze(node.y1_expr)
            self.analyze(node.x2_expr)
            self.analyze(node.y2_expr)
        elif isinstance(node, LetC):
            self.analyze(node.expr)
            self.symbol_table[node.name] = node.expr
        elif isinstance(node, BinOp):
            self.analyze(node.left)
            self.analyze(node.right)
            right_value = self.constant_value(node.right)
            if node.op == 'DIV' and right_value == 0:
                raise SemanticError("Division by zero in constant expression")
        elif isinstance(node, Identifier):
            if node.name not in self.symbol_table:
                raise SemanticError(f"Undefined variable '{node.name}' at line {node.line}, col {node.col}")
        elif isinstance(node, Number):
            pass
        elif isinstance(node, ColorLiteral):
            if node.value.startswith('#'):
                if len(node.value) != 7:
                    raise SemanticError(f"Invalid hex color {node.value} at line {node.line}")
            elif node.value not in self.VALID_COLORS:
                raise SemanticError(f"Unknown color '{node.value}' at line {node.line}, col {node.col}")

    def constant_value(self, node: ASTNode):
        if isinstance(node, Number):
            return node.value
        if isinstance(node, Identifier) and node.name in self.symbol_table:
            return self.constant_value(self.symbol_table[node.name])
        if isinstance(node, BinOp):
            left = self.constant_value(node.left)
            right = self.constant_value(node.right)
            if left is None or right is None:
                return None
            if node.op == 'PLUS':
                return left + right
            if node.op == 'MINUS':
                return left - right
            if node.op == 'MUL':
                return left * right
            if node.op == 'DIV':
                if right == 0:
                    return None
                return left / right
        return None

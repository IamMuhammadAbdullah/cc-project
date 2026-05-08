from .parser import *

class SemanticError(Exception):
    pass

class SemanticAnalyzer:
    def analyze(self, node: ASTNode):
        if isinstance(node, Program):
            for stmt in node.statements:
                self.analyze(stmt)
        elif isinstance(node, RepeatL):
            self.analyze(node.count_expr)
            for stmt in node.body:
                self.analyze(stmt)
        elif isinstance(node, MoveC) or isinstance(node, TurnC):
            self.analyze(node.expr)
        elif isinstance(node, ColorC):
            if not len(node.color_hex.value) == 7:
                raise SemanticError(f"Invalid Hex color length {node.color_hex.value} at line {node.color_hex.line}")
        elif isinstance(node, BinOp):
            self.analyze(node.left)
            self.analyze(node.right)
        elif isinstance(node, Number) or isinstance(node, HexColor):
            pass

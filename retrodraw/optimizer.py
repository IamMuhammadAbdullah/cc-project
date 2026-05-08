from .parser import *

class Optimizer:
    """Implement simple constant folding to pre-calculate arithmetic"""
    def __init__(self):
        self.constants = {}

    def optimize(self, node: ASTNode) -> ASTNode:
        return self.fold(node)

    def fold(self, node: ASTNode) -> ASTNode:
        if isinstance(node, Program):
            return Program([self.fold(stmt) for stmt in node.statements])
        elif isinstance(node, MoveC):
            return MoveC(self.fold(node.expr))
        elif isinstance(node, TurnC):
            return TurnC(self.fold(node.expr))
        elif isinstance(node, SetPosC):
            return SetPosC(self.fold(node.x_expr), self.fold(node.y_expr))
        elif isinstance(node, RepeatL):
            return RepeatL(self.fold(node.count_expr), [self.fold(stmt) for stmt in node.body])
        elif isinstance(node, IfOnColor):
            return IfOnColor(node.color, [self.fold(stmt) for stmt in node.body])
        elif isinstance(node, ColorC):
            return node
        elif isinstance(node, RectC):
            return RectC(
                self.fold(node.x1_expr),
                self.fold(node.y1_expr),
                self.fold(node.x2_expr),
                self.fold(node.y2_expr),
            )
        elif isinstance(node, LetC):
            expr = self.fold(node.expr)
            if isinstance(expr, Number):
                self.constants[node.name] = expr
            return LetC(node.name, expr, node.line, node.col)
        elif isinstance(node, Identifier):
            return self.constants.get(node.name, node)
        elif isinstance(node, BinOp):
            left = self.fold(node.left)
            right = self.fold(node.right)
            
            # Perform constant folding if both children are numbers!
            if isinstance(left, Number) and isinstance(right, Number):
                new_value = 0
                if node.op == 'PLUS': new_value = left.value + right.value
                elif node.op == 'MINUS': new_value = left.value - right.value
                elif node.op == 'MUL': new_value = left.value * right.value
                elif node.op == 'DIV': 
                    if right.value == 0:
                        return BinOp(left, node.op, right)
                    else:
                        new_value = left.value / right.value 
                return Number(new_value, left.line, left.col)
                
            return BinOp(left, node.op, right)
        return node

from .parser import *

class Optimizer:
    """Implement simple constant folding to pre-calculate arithmetic"""
    def fold(self, node: ASTNode) -> ASTNode:
        if isinstance(node, Program):
            return Program([self.fold(stmt) for stmt in node.statements])
        elif isinstance(node, MoveC):
            return MoveC(self.fold(node.expr))
        elif isinstance(node, TurnC):
            return TurnC(self.fold(node.expr))
        elif isinstance(node, RepeatL):
            return RepeatL(self.fold(node.count_expr), [self.fold(stmt) for stmt in node.body])
        elif isinstance(node, ColorC):
            return node
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
                        new_value = 0 # Safe fallback for div by zero during opt
                    else:
                        new_value = left.value // right.value 
                return Number(new_value, left.line, left.col)
                
            return BinOp(left, node.op, right)
        return node

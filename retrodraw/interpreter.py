from .parser import *
import turtle

class Interpreter:
    def __init__(self, t: turtle.RawTurtle):
        self.t = t

    def evaluate_expr(self, node: ASTNode) -> int:
        if isinstance(node, Number):
            return node.value
        elif isinstance(node, BinOp):
            left = self.evaluate_expr(node.left)
            right = self.evaluate_expr(node.right)
            if node.op == 'PLUS': return left + right
            elif node.op == 'MINUS': return left - right
            elif node.op == 'MUL': return left * right
            elif node.op == 'DIV': return left // right if right != 0 else 0
        return 0

    def execute(self, node: ASTNode):
        if isinstance(node, Program):
            for stmt in node.statements:
                self.execute(stmt)
        elif isinstance(node, MoveC):
            dist = self.evaluate_expr(node.expr)
            self.t.forward(dist)
        elif isinstance(node, TurnC):
            angle = self.evaluate_expr(node.expr)
            self.t.right(angle)
        elif isinstance(node, ColorC):
            self.t.pencolor(node.color_hex.value)
        elif isinstance(node, RepeatL):
            count = self.evaluate_expr(node.count_expr)
            for _ in range(count):
                for stmt in node.body:
                    self.execute(stmt)

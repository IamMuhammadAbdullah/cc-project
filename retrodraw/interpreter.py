from .parser import *
import turtle

class Interpreter:
    COLOR_MAP = {
        'RED': '#FF0000',
        'GREEN': '#00FF00',
        'BLUE': '#0000FF',
        'BLACK': '#000000',
        'WHITE': '#FFFFFF',
        'YELLOW': '#FFFF00',
        'CYAN': '#00FFFF',
        'MAGENTA': '#FF00FF',
        'GRAY': '#808080',
        'ORANGE': '#FFA500',
        'PURPLE': '#800080',
        'PINK': '#FFC0CB',
    }

    def __init__(self, t: turtle.RawTurtle):
        self.t = t
        self.symbol_table = {}
        self.turtle_state = {
            'position': self.t.position(),
            'heading': self.t.heading(),
            'pen_color': '#000000',
        }

    def evaluate_expr(self, node: ASTNode) -> float:
        if isinstance(node, Number):
            return node.value
        elif isinstance(node, Identifier):
            if node.name not in self.symbol_table:
                raise RuntimeError(f"Undefined variable '{node.name}'")
            return self.symbol_table[node.name]
        elif isinstance(node, BinOp):
            left = self.evaluate_expr(node.left)
            right = self.evaluate_expr(node.right)
            if node.op == 'PLUS': return left + right
            elif node.op == 'MINUS': return left - right
            elif node.op == 'MUL': return left * right
            elif node.op == 'DIV':
                if right == 0:
                    raise RuntimeError("Division by zero")
                return left / right
        return 0

    def execute(self, node: ASTNode):
        if isinstance(node, Program):
            for stmt in node.statements:
                self.execute(stmt)
        elif isinstance(node, MoveC):
            dist = self.evaluate_expr(node.expr)
            self.t.forward(dist)
            self._sync_state()
        elif isinstance(node, TurnC):
            angle = self.evaluate_expr(node.expr)
            self.t.right(angle)
            self._sync_state()
        elif isinstance(node, SetPosC):
            self.t.penup()
            self.t.setposition(self.evaluate_expr(node.x_expr), self.evaluate_expr(node.y_expr))
            self.t.pendown()
            self._sync_state()
        elif isinstance(node, ColorC):
            self.t.pencolor(self.resolve_color(node.color.value))
            self._sync_state()
        elif isinstance(node, RectC):
            self.draw_rect(
                self.evaluate_expr(node.x1_expr),
                self.evaluate_expr(node.y1_expr),
                self.evaluate_expr(node.x2_expr),
                self.evaluate_expr(node.y2_expr),
            )
        elif isinstance(node, RepeatL):
            count = int(self.evaluate_expr(node.count_expr))
            for _ in range(count):
                for stmt in node.body:
                    self.execute(stmt)
        elif isinstance(node, IfOnColor):
            if self.is_on_color(node.color.value):
                for stmt in node.body:
                    self.execute(stmt)
        elif isinstance(node, LetC):
            self.symbol_table[node.name] = self.evaluate_expr(node.expr)

    def resolve_color(self, value: str) -> str:
        return self.COLOR_MAP.get(value, value)

    def draw_rect(self, x1, y1, x2, y2):
        old_pos = self.t.position()
        old_heading = self.t.heading()
        was_down = self.t.isdown()

        self.t.penup()
        self.t.setposition(x1, y1)
        self.t.pendown()
        self.t.setposition(x2, y1)
        self.t.setposition(x2, y2)
        self.t.setposition(x1, y2)
        self.t.setposition(x1, y1)

        self.t.penup()
        self.t.setposition(old_pos)
        self.t.setheading(old_heading)
        if was_down:
            self.t.pendown()
        self._sync_state()

    def is_on_color(self, color_value: str) -> bool:
        target = self.resolve_color(color_value).lower()
        screen = self.t.getscreen()
        canvas = screen.cv
        x, y = self.t.position()

        canvas_x = x * screen.xscale
        canvas_y = -y * screen.yscale
        for item_id in canvas.find_overlapping(canvas_x - 2, canvas_y - 2, canvas_x + 2, canvas_y + 2):
            for option in ('fill', 'outline'):
                try:
                    item_color = canvas.itemcget(item_id, option)
                except Exception:
                    continue
                if item_color and item_color.lower() == target:
                    return True
        return False

    def _sync_state(self):
        self.turtle_state = {
            'position': self.t.position(),
            'heading': self.t.heading(),
            'pen_color': self.t.pencolor(),
        }

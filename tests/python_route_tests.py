import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from compiler import compile_source
from retrodraw.lexer import Lexer, LexerError
from retrodraw.parser import ParserError
from retrodraw.parser import MoveC, Number, Program, RepeatL
from retrodraw.interpreter import Interpreter
from retrodraw.semantic import SemanticError


def assert_raises(expected, fn):
    try:
        fn()
    except expected:
        return
    raise AssertionError(f"Expected {expected.__name__}")


def test_constant_folding_and_variables():
    ast = compile_source("LET STEP = 10 + 20 * 3\nMOVE STEP\n")
    assert isinstance(ast, Program)
    move = ast.statements[1]
    assert isinstance(move, MoveC)
    assert isinstance(move.expr, Number)
    assert move.expr.value == 70


def test_lexer_accepts_windows_newlines_and_comments():
    tokens = Lexer("COLOR RED\r\n// comment\r\nMOVE 10\r\n").tokenize()
    token_types = [token.type for token in tokens]

    assert token_types == ["COLOR", "IDENT", "MOVE", "NUMBER", "EOF"]


def test_proposal_constructs_parse_and_optimize():
    ast = compile_source(
        "COLOR RED\n"
        "RECT (-100,-100) (100,100)\n"
        "SET_POS (0,0)\n"
        "REPEAT 2 [ MOVE 5 IF ON_COLOR RED [ TURN 180 COLOR GREEN ] ]\n"
    )
    assert isinstance(ast.statements[3], RepeatL)


def test_on_color_samples_current_turtle_position():
    class FakeCanvas:
        def __init__(self):
            self.query = None

        def winfo_width(self):
            return 600

        def winfo_height(self):
            return 500

        def find_overlapping(self, x1, y1, x2, y2):
            self.query = (x1, y1, x2, y2)
            return [1]

        def itemcget(self, item_id, option):
            return "#FF0000" if option == "outline" else ""

    class FakeScreen:
        def __init__(self, canvas):
            self.cv = canvas
            self.xscale = 1
            self.yscale = 1

    class FakeTurtle:
        def __init__(self):
            self.canvas = FakeCanvas()

        def getscreen(self):
            return FakeScreen(self.canvas)

        def position(self):
            return (100, 0)

        def heading(self):
            return 0

    fake_turtle = FakeTurtle()
    interpreter = Interpreter(fake_turtle)

    assert interpreter.is_on_color("RED")
    assert fake_turtle.canvas.query == (98, -2, 102, 2)


def test_on_color_ignores_unsupported_canvas_color_options():
    class FakeCanvas:
        def winfo_width(self):
            return 600

        def winfo_height(self):
            return 500

        def find_overlapping(self, x1, y1, x2, y2):
            return [1]

        def itemcget(self, item_id, option):
            if option == "outline":
                raise RuntimeError("unknown option")
            return "#0000FF"

    class FakeScreen:
        def __init__(self, canvas):
            self.cv = canvas
            self.xscale = 1
            self.yscale = 1

    class FakeTurtle:
        def __init__(self):
            self.canvas = FakeCanvas()

        def getscreen(self):
            return FakeScreen(self.canvas)

        def position(self):
            return (100, 0)

        def heading(self):
            return 0

    assert not Interpreter(FakeTurtle()).is_on_color("RED")


def test_semantic_errors():
    assert_raises(SemanticError, lambda: compile_source("MOVE UNKNOWN\n"))
    assert_raises(SemanticError, lambda: compile_source("MOVE 10 / 0\n"))
    assert_raises(SemanticError, lambda: compile_source("COLOR BLURPLE\n"))
    assert_raises(SemanticError, lambda: compile_source("REPEAT -1 [ MOVE 10 ]\n"))
    assert_raises(SemanticError, lambda: compile_source("REPEAT 2.5 [ MOVE 10 ]\n"))


def test_lexer_and_parser_errors():
    assert_raises(LexerError, lambda: compile_source("MOVE @\n"))
    assert_raises(ParserError, lambda: compile_source("REPEAT 2 [ MOVE 10\n"))


def test_readme_snippets_compile():
    snippets = [
        "COLOR BLUE\nREPEAT 4 [ MOVE 100 TURN 90 ]",
        "COLOR MAGENTA\nLET STEP = 8\nREPEAT 40 [ MOVE STEP + 2 * 5 TURN 92 ]",
        "COLOR ORANGE\nREPEAT 12 [ REPEAT 4 [ MOVE 60 TURN 90 ] TURN 30 ]",
        (
            "COLOR GREEN\nSET_POS (-120,-80)\nRECT (-120,-80) (120,80)\n"
            "COLOR BLACK\nSET_POS (0,0)\nMOVE 100\nTURN 135\nMOVE 80"
        ),
        "COLOR CYAN\nMOVE 50 + 25 * 2\nTURN 90\nMOVE (100 + 20) / 2\nTURN 90\nMOVE 10 * (3 + 4)",
        "LET SIDE = 75\nLET ANGLE = 360 / 5\nCOLOR PURPLE\nREPEAT 5 [ MOVE SIDE TURN ANGLE ]",
        (
            "COLOR RED\nRECT (-100,-100) (100,100)\nCOLOR BLUE\nSET_POS (0,0)\n"
            "REPEAT 120 [ MOVE 5 IF ON_COLOR RED [ TURN 180 COLOR GREEN ] ]"
        ),
        "COLOR #FF0055\nREPEAT 36 [ MOVE 100 TURN 170 ]",
    ]
    for snippet in snippets:
        compile_source(snippet)


if __name__ == "__main__":
    test_constant_folding_and_variables()
    test_lexer_accepts_windows_newlines_and_comments()
    test_proposal_constructs_parse_and_optimize()
    test_on_color_samples_current_turtle_position()
    test_on_color_ignores_unsupported_canvas_color_options()
    test_semantic_errors()
    test_lexer_and_parser_errors()
    test_readme_snippets_compile()
    print("All compiler route tests passed.")

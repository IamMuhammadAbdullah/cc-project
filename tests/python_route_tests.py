import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from compiler import compile_source
from retrodraw.parser import MoveC, Number, Program, RepeatL
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


def test_proposal_constructs_parse_and_optimize():
    ast = compile_source(
        "COLOR RED\n"
        "RECT (-100,-100) (100,100)\n"
        "SET_POS (0,0)\n"
        "REPEAT 2 [ MOVE 5 IF ON_COLOR RED [ TURN 180 COLOR GREEN ] ]\n"
    )
    assert isinstance(ast.statements[3], RepeatL)


def test_semantic_errors():
    assert_raises(SemanticError, lambda: compile_source("MOVE UNKNOWN\n"))
    assert_raises(SemanticError, lambda: compile_source("MOVE 10 / 0\n"))
    assert_raises(SemanticError, lambda: compile_source("COLOR BLURPLE\n"))


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
    test_proposal_constructs_parse_and_optimize()
    test_semantic_errors()
    test_readme_snippets_compile()
    print("All compiler route tests passed.")

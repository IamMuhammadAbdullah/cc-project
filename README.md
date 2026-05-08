# SensiPath / RetroDraw Compiler

This project implements the proposal's sensory turtle-graphics DSL while keeping the existing Tkinter GUI.

## Compiler Pipeline

1. Lexical analysis: tokenizes movement, drawing, loop, conditional, color, expression, and variable syntax.
2. Syntax analysis: builds an AST for commands such as `MOVE`, `TURN`, `SET_POS`, `RECT`, `REPEAT`, and `IF ON_COLOR`.
3. Semantic analysis: validates colors, variable usage, repeat counts, and constant division by zero while maintaining a symbol table and turtle-state snapshot.
4. Optimization: performs constant folding across arithmetic expression trees.
5. Interpretation: walks the optimized AST and renders live turtle graphics on the GUI canvas.

## Supported DSL Example

```logo
// Draw a boundary
COLOR RED
RECT (-100,-100) (100,100)

COLOR BLUE
LET STEP = 5
REPEAT 100 [
  MOVE STEP
  IF ON_COLOR RED [
    TURN 180
    COLOR GREEN
  ]
]
```

## Testable Code Snippets

Paste any of these into `test.logo` or directly into the GUI editor.

### 1. Square

```logo
COLOR BLUE
REPEAT 4 [
  MOVE 100
  TURN 90
]
```

### 2. Spiral

```logo
COLOR MAGENTA
LET STEP = 8
REPEAT 40 [
  MOVE STEP + 2 * 5
  TURN 92
]
```

### 3. Nested Pattern

```logo
COLOR ORANGE
REPEAT 12 [
  REPEAT 4 [
    MOVE 60
    TURN 90
  ]
  TURN 30
]
```

### 4. Position And Rectangle

```logo
COLOR GREEN
SET_POS (-120,-80)
RECT (-120,-80) (120,80)

COLOR BLACK
SET_POS (0,0)
MOVE 100
TURN 135
MOVE 80
```

### 5. Constant Folding

```logo
COLOR CYAN
MOVE 50 + 25 * 2
TURN 90
MOVE (100 + 20) / 2
TURN 90
MOVE 10 * (3 + 4)
```

### 6. Variables

```logo
LET SIDE = 75
LET ANGLE = 360 / 5

COLOR PURPLE
REPEAT 5 [
  MOVE SIDE
  TURN ANGLE
]
```

### 7. Sensory Boundary Reaction

```logo
COLOR RED
RECT (-100,-100) (100,100)

COLOR BLUE
SET_POS (0,0)
REPEAT 120 [
  MOVE 5
  IF ON_COLOR RED [
    TURN 180
    COLOR GREEN
  ]
]
```

### 8. Hex Colors

```logo
COLOR #FF0055
REPEAT 36 [
  MOVE 100
  TURN 170
]
```

Run the GUI:

```powershell
python retrodraw_gui.py
```

Run the compiler checks from the CLI:

```powershell
python compiler.py test.logo --debug
```

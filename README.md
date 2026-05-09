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

### 9. Rotating Starburst

```logo
COLOR RED
REPEAT 40 [
  REPEAT 8 [
    MOVE 200
    TURN 135
  ]
  TURN 9
]
```

### 10. Cyan Square Bloom

```logo
COLOR #00FFFF
REPEAT 72 [
  REPEAT 4 [
    MOVE 90
    TURN 90
  ]
  TURN 5
  MOVE 3
]
```

### 11. Purple Pentagram Wheel

```logo
COLOR PURPLE
REPEAT 36 [
  REPEAT 5 [
    MOVE 100
    TURN 144
  ]
  TURN 10
]
```

### 12. Blue Dodecagon Rosette

```logo
COLOR BLUE
REPEAT 24 [
  REPEAT 12 [
    MOVE 45
    TURN 30
  ]
  TURN 15
]
```

### 13. Cyan Nested Triangles

```logo
COLOR CYAN
REPEAT 18 [
  REPEAT 3 [
    REPEAT 4 [
      MOVE 40
      TURN 60
      MOVE 40
      TURN 120
    ]
    TURN 120
  ]
  TURN 20
]
```

### 14. Magenta Hexagon Mandala

```logo
COLOR MAGENTA
REPEAT 36 [
  REPEAT 6 [
    MOVE 80
    TURN 60
  ]
  TURN 10
]
```

### 15. Blue Triangle Wheel

```logo
COLOR BLUE
REPEAT 60 [
  REPEAT 3 [
    MOVE 100
    TURN 120
  ]
  TURN 6
]
```

### 16. Hot Pink Spirograph

```logo
COLOR #FF0055
REPEAT 72 [
  MOVE 140
  TURN 170
]
```

### 17. Purple Pentagon Ring

```logo
COLOR PURPLE
REPEAT 36 [
  REPEAT 5 [
    MOVE 80
    TURN 72
  ]
  TURN 10
]
```

### 18. Orange Phyllotaxis Spiral

```logo
COLOR ORANGE
REPEAT 140 [
  MOVE 160
  TURN 137
]
```

### 19. Growing Cyan Squares

```logo
COLOR CYAN
LET SIDE = 100
REPEAT 45 [
  REPEAT 4 [
    MOVE SIDE
    TURN 90
  ]
  TURN 12
  LET SIDE = SIDE + 20
]
```

### 20. Growing Magenta Spiral

```logo
COLOR MAGENTA
LET STEP = 4
REPEAT 90 [
  MOVE STEP
  TURN 91
  LET STEP = STEP + 2
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

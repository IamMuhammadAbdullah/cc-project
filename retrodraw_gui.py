import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import turtle
import sys

from retrodraw.lexer import Lexer, LexerError
from retrodraw.parser import Parser, ParserError
from retrodraw.semantic import SemanticAnalyzer, SemanticError
from retrodraw.optimizer import Optimizer
from retrodraw.interpreter import Interpreter

class RetroDrawGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RetroDraw IDE - DSL Compiler Project")
        self.root.geometry("1000x600")

        # Layout styling
        self.root.configure(bg="#2D2D2D")

        # Left Frame: Editor and Output Console
        self.left_frame = tk.Frame(root, width=400, bg="#2D2D2D")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        
        # Editor
        lbl1 = tk.Label(self.left_frame, text="Code Editor (.logo)", font=("Consolas", 12, "bold"), bg="#2D2D2D", fg="white")
        lbl1.pack(pady=5)
        self.editor = ScrolledText(self.left_frame, height=20, width=50, font=("Consolas", 12), bg="#1E1E1E", fg="#D4D4D4", insertbackground="white")
        self.editor.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # Buttons
        self.btn_frame = tk.Frame(self.left_frame, bg="#2D2D2D")
        self.btn_frame.pack(pady=5)
        self.run_btn = tk.Button(self.btn_frame, text="► Run Code", command=self.run_code, bg="#4CAF50", fg="white", font=("Consolas", 11, "bold"), relief=tk.FLAT, padx=10)
        self.run_btn.pack(side=tk.LEFT, padx=5)

        # Output/Console
        lbl2 = tk.Label(self.left_frame, text="Compiler Output Console", font=("Consolas", 10, "bold"), bg="#2D2D2D", fg="white")
        lbl2.pack(pady=5)
        self.console = ScrolledText(self.left_frame, height=10, width=50, bg="#000000", fg="#00FF00", font=("Consolas", 10))
        self.console.pack(padx=10, pady=5, fill=tk.BOTH, expand=False)

        # Right Frame: Turtle Canvas
        self.right_frame = tk.Frame(root, width=600, bg="#2D2D2D")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        lbl3 = tk.Label(self.right_frame, text="RetroDraw Live Canvas", font=("Consolas", 12, "bold"), bg="#2D2D2D", fg="white")
        lbl3.pack(pady=5)
        
        self.canvas = tk.Canvas(self.right_frame, width=600, height=500, bg="white", highlightthickness=0)
        self.canvas.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # Setup RawTurtle
        self.turtle_screen = turtle.TurtleScreen(self.canvas)
        self.t = turtle.RawTurtle(self.turtle_screen)
        self.t.speed(0)
        
        # Initial editor code
        initial_code = '''COLOR #FF0055
REPEAT 36 [
  MOVE 100
  TURN 170
]'''
        self.editor.insert(tk.END, initial_code)
        self.print_console("Welcome to RetroDraw Compiler System.")

    def print_console(self, text):
        self.console.insert(tk.END, "> " + text + "\n")
        self.console.see(tk.END)

    def run_code(self):
        self.console.delete(1.0, tk.END)
        code = self.editor.get(1.0, tk.END).strip()
        if not code:
            self.print_console("Error: Empty code.")
            return

        self.t.reset()
        self.t.speed(0)

        try:
            self.print_console("Phase 1: Lexical Analysis...")
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            
            self.print_console("Phase 2: Syntax Analysis (Parser)...")
            parser = Parser(tokens)
            ast = parser.parse()
            
            self.print_console("Phase 3: Semantic Analysis...")
            analyzer = SemanticAnalyzer()
            analyzer.analyze(ast)

            self.print_console("Phase 4: Optimization (Constant Folding)...")
            optimizer = Optimizer()
            ast_opt = optimizer.fold(ast)
            
            self.print_console("Phase 5: Code Generation / Execution...")
            interpreter = Interpreter(self.t)
            interpreter.execute(ast_opt)

            self.print_console("SUCCESS! Graphic Rendered.")
            
        except LexerError as e:
            self.print_console(f"LEXER ERROR: {e}")
        except ParserError as e:
            self.print_console(f"PARSER ERROR: {e}")
        except SemanticError as e:
            self.print_console(f"SEMANTIC ERROR: {e}")
        except Exception as e:
            self.print_console(f"RUNTIME ERROR: {str(e)}")

        self.turtle_screen.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = RetroDrawGUI(root)
    root.mainloop()

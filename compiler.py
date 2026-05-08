import argparse
import sys

from retrodraw.lexer import Lexer, LexerError
from retrodraw.parser import Parser, ParserError
from retrodraw.semantic import SemanticAnalyzer, SemanticError
from retrodraw.optimizer import Optimizer


def compile_source(code: str, debug: bool = False):
    lexer = Lexer(code)
    tokens = lexer.tokenize()

    if debug:
        print("=== TOKENS ===")
        for tok in tokens:
            print(f"{tok.type:10} {str(tok.value):12} line={tok.line} col={tok.column}")

    parser = Parser(tokens)
    ast = parser.parse()

    if debug:
        print("\n=== AST ===")
        print(ast)

    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)

    optimizer = Optimizer()
    optimized_ast = optimizer.fold(ast)

    if debug:
        print("\n=== OPTIMIZED AST ===")
        print(optimized_ast)
        print("\n=== SYMBOL TABLE ===")
        print(analyzer.symbol_table)
        print("=== TURTLE STATE ===")
        print(analyzer.turtle_state)

    return optimized_ast


def setup_cli():
    parser = argparse.ArgumentParser(
        description="SensiPath/RetroDraw compiler: lexes, parses, validates, and optimizes .logo programs."
    )
    parser.add_argument("input_file", help="Input .logo source file")
    parser.add_argument("--debug", action="store_true", help="Print tokens, AST, and semantic tables")
    return parser.parse_args()


def main():
    args = setup_cli()

    try:
        with open(args.input_file, "r", encoding="utf-8") as source:
            compile_source(source.read(), debug=args.debug)
        print(f"[+] Compilation completed successfully: {args.input_file}")
    except FileNotFoundError:
        print(f"Error: Source file '{args.input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except LexerError as exc:
        print(f"Lexical Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except ParserError as exc:
        print(f"Syntax Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except SemanticError as exc:
        print(f"Semantic Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

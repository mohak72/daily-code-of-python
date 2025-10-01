"""Daily calculator snippet for 2025-10-01

Features:
- Safe expression evaluator for arithmetic and selected math functions
- Calculator class with common operations
- CLI demo mode (default)
- Optional simple Tkinter GUI when run with --gui

Usage:
    python daily_2025-10-01_calculator.py        # runs CLI demo
    python daily_2025-10-01_calculator.py --gui  # opens a simple GUI
"""

from __future__ import annotations

import ast
import math
import operator as op
import sys
from dataclasses import dataclass
from typing import Any, Dict

try:
    import tkinter as tk
    from tkinter import ttk
except Exception:  # pragma: no cover - GUI optional
    tk = None


# Allowed operators mapping for safe eval
ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}

# Allowed names from math
ALLOWED_NAMES: Dict[str, Any] = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
# Add some builtins
ALLOWED_NAMES.update({"abs": abs, "round": round, "min": min, "max": max})


def safe_eval(expr: str) -> float:
    """Safely evaluate a numeric expression using AST.

    Supports arithmetic operators and functions listed in ALLOWED_NAMES.
    Raises ValueError on invalid expressions.
    """

    def _eval(node: ast.AST) -> Any:
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Num):  # type: ignore[attr-defined]
            return node.n
        if isinstance(node, ast.Constant):  # Py3.8+
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Unsupported constant")
        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type in ALLOWED_OPERATORS:
                return ALLOWED_OPERATORS[op_type](left, right)
            raise ValueError("Unsupported binary operator")
        if isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type in ALLOWED_OPERATORS:
                return ALLOWED_OPERATORS[op_type](operand)
            raise ValueError("Unsupported unary operator")
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Only simple function calls allowed")
            func_name = node.func.id
            if func_name not in ALLOWED_NAMES:
                raise ValueError(f"Function {func_name} is not allowed")
            func = ALLOWED_NAMES[func_name]
            args = [_eval(a) for a in node.args]
            return func(*args)
        if isinstance(node, ast.Name):
            if node.id in ALLOWED_NAMES:
                return ALLOWED_NAMES[node.id]
            raise ValueError(f"Name {node.id} is not allowed")
        if isinstance(node, ast.Tuple):
            return tuple(_eval(e) for e in node.elts)
        raise ValueError(f"Unsupported expression: {ast.dump(node)}")

    try:
        parsed = ast.parse(expr, mode="eval")
        return float(_eval(parsed))
    except Exception as exc:
        raise ValueError(f"Invalid expression: {exc}") from exc


@dataclass
class Calculator:
    """Small calculator with convenience methods wrapping safe_eval."""

    def calculate(self, expr: str) -> float:
        return safe_eval(expr)

    def add(self, a: float, b: float) -> float:
        return a + b

    def sub(self, a: float, b: float) -> float:
        return a - b

    def mul(self, a: float, b: float) -> float:
        return a * b

    def div(self, a: float, b: float) -> float:
        if b == 0:
            raise ZeroDivisionError("division by zero")
        return a / b

    def pow(self, a: float, b: float) -> float:
        return a ** b

    def sqrt(self, a: float) -> float:
        return math.sqrt(a)

    def factorial(self, n: int) -> int:
        return math.factorial(n)


def run_cli_demo():
    calc = Calculator()
    samples = [
        "2 + 3 * 4",
        "(1 + 2) ** 3",
        "sqrt(16)",
        "factorial(5)",
        "sin(pi/2)",
        "1 / 3",
    ]
    print("Calculator demo - safe evaluator")
    for s in samples:
        try:
            res = calc.calculate(s)
        except Exception as e:
            res = f"error: {e}"
        print(f"{s} = {res}")

    print("\nInteractive mode: type 'quit' to exit")
    while True:
        try:
            expr = input('expr> ').strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not expr:
            continue
        if expr.lower() in ("quit", "exit"):
            break
        try:
            print(calc.calculate(expr))
        except Exception as e:
            print("Error:", e)


# --- Simple Tkinter GUI (optional) ---
def launch_tkinter():
    if tk is None:
        print("Tkinter not available. Install tkinter or run without --gui.")
        return

    calc = Calculator()
    root = tk.Tk()
    root.title("Daily Calculator - 2025-10-01")

    frm = ttk.Frame(root, padding=10)
    frm.grid()

    expr_var = tk.StringVar()
    result_var = tk.StringVar(value="Result will show here")

    ttk.Label(frm, text="Expression:").grid(column=0, row=0, sticky="w")
    expr_entry = ttk.Entry(frm, width=40, textvariable=expr_var)
    expr_entry.grid(column=0, row=1, columnspan=2, sticky="we")

    def on_eval(_=None):
        e = expr_var.get().strip()
        if not e:
            return
        try:
            res = calc.calculate(e)
            result_var.set(str(res))
        except Exception as exc:
            result_var.set(f"Error: {exc}")

    eval_btn = ttk.Button(frm, text="Evaluate", command=on_eval)
    eval_btn.grid(column=0, row=2, sticky="w")

    ttk.Label(frm, textvariable=result_var, foreground="blue").grid(column=0, row=3, columnspan=2, sticky="w")

    expr_entry.bind('<Return>', on_eval)
    expr_entry.focus()

    root.mainloop()


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    if "--gui" in argv:
        launch_tkinter()
        return 0
    # default: run CLI demo
    run_cli_demo()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

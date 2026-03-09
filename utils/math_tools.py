"""Symbolic math tools using SymPy for the Solver Agent."""
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import re


def safe_solve(equation_str: str, variable: str = "x") -> dict:
    """Solve a single-variable equation symbolically."""
    try:
        var = sp.Symbol(variable)
        # Try to parse as equation (with =)
        if "=" in equation_str:
            lhs, rhs = equation_str.split("=", 1)
            expr = parse_expr(lhs.strip(), local_dict={variable: var}) - parse_expr(rhs.strip(), local_dict={variable: var})
        else:
            expr = parse_expr(equation_str.strip(), local_dict={variable: var})
        solutions = sp.solve(expr, var)
        return {"success": True, "solutions": [str(s) for s in solutions], "simplified": str(sp.simplify(expr))}
    except Exception as e:
        return {"success": False, "error": str(e)}


def safe_differentiate(expr_str: str, variable: str = "x") -> dict:
    """Differentiate an expression symbolically."""
    try:
        var = sp.Symbol(variable)
        expr = parse_expr(expr_str.strip(), local_dict={variable: var},
                          transformations=standard_transformations + (implicit_multiplication_application,))
        derivative = sp.diff(expr, var)
        simplified = sp.simplify(derivative)
        return {"success": True, "derivative": str(simplified), "latex": sp.latex(simplified)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def safe_integrate(expr_str: str, variable: str = "x", limits: tuple = None) -> dict:
    """Integrate an expression symbolically (definite or indefinite)."""
    try:
        var = sp.Symbol(variable)
        expr = parse_expr(expr_str.strip(), local_dict={variable: var},
                          transformations=standard_transformations + (implicit_multiplication_application,))
        if limits:
            result = sp.integrate(expr, (var, limits[0], limits[1]))
        else:
            result = sp.integrate(expr, var)
        simplified = sp.simplify(result)
        return {"success": True, "integral": str(simplified), "latex": sp.latex(simplified)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def safe_limit(expr_str: str, variable: str = "x", point: str = "0", direction: str = "+") -> dict:
    """Compute limit of expression."""
    try:
        var = sp.Symbol(variable)
        expr = parse_expr(expr_str.strip(), local_dict={variable: var},
                          transformations=standard_transformations + (implicit_multiplication_application,))
        pt = parse_expr(point)
        result = sp.limit(expr, var, pt, direction)
        return {"success": True, "limit": str(result), "latex": sp.latex(result)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def safe_evaluate(expr_str: str, substitutions: dict = None) -> dict:
    """Evaluate a numeric expression."""
    try:
        substitutions = substitutions or {}
        local_dict = {k: sp.Symbol(k) for k in substitutions}
        expr = parse_expr(expr_str.strip(), local_dict=local_dict,
                          transformations=standard_transformations + (implicit_multiplication_application,))
        if substitutions:
            expr = expr.subs([(sp.Symbol(k), v) for k, v in substitutions.items()])
        result = float(expr.evalf())
        return {"success": True, "value": result, "exact": str(sp.simplify(expr))}
    except Exception as e:
        return {"success": False, "error": str(e)}


def compute_with_tool(tool_name: str, params: dict) -> dict:
    """Dispatcher for math tool calls from agents."""
    tools = {
        "solve": lambda p: safe_solve(p.get("equation", ""), p.get("variable", "x")),
        "differentiate": lambda p: safe_differentiate(p.get("expression", ""), p.get("variable", "x")),
        "integrate": lambda p: safe_integrate(p.get("expression", ""), p.get("variable", "x"),
                                               p.get("limits", None)),
        "limit": lambda p: safe_limit(p.get("expression", ""), p.get("variable", "x"),
                                      p.get("point", "0"), p.get("direction", "+")),
        "evaluate": lambda p: safe_evaluate(p.get("expression", ""), p.get("substitutions", {})),
    }
    if tool_name not in tools:
        return {"success": False, "error": f"Unknown tool: {tool_name}"}
    return tools[tool_name](params)

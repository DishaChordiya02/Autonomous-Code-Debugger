import ast

def analyze_code(source_code):
    """
    Parses the given Python code and detects potential issues
    using Abstract Syntax Tree (AST).
    """
    tree = ast.parse(source_code)  # Convert code into AST
    issues = []

    for node in ast.walk(tree):  # Walk through the AST nodes
        if isinstance(node, ast.FunctionDef) and len(node.body) > 50:
            issues.append(f"Function '{node.name}' is too long. Consider breaking it down.")
        if isinstance(node, ast.For) and not any(isinstance(n, ast.If) for n in ast.walk(node)):
            issues.append("Loop without a conditional check detected.")

    return issues

# Testing with a sample Python script
code_sample = """
def long_function():
    for i in range(100):
        print(i)
"""

print(analyze_code(code_sample))
    
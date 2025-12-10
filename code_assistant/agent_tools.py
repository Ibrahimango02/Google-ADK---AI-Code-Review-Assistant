import ast  # For parsing Python code

def analyze_code_structure(code: str) -> dict:
    """Analyzes the structure of Python code and returns insights.
    
    Args:
        code (str): The Python code to analyze as a string.
    
    Returns:
        dict: Analysis results including functions, classes, complexity metrics.
              Contains 'status' ('success' or 'error') and relevant data.
    """
    print(f"--- Tool: analyze_code_structure called ---")
    
    try:
        tree = ast.parse(code)
        
        analysis = {
            "status": "success",
            "functions": [],
            "classes": [],
            "imports": [],
            "lines_of_code": len(code.split('\n')),
            "issues": []
        }
        
        # Extract functions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    "name": node.name,
                    "args": len(node.args.args),
                    "line_number": node.lineno,
                    "has_docstring": ast.get_docstring(node) is not None
                }
                analysis["functions"].append(func_info)
                
                # Check for issues
                if not func_info["has_docstring"]:
                    analysis["issues"].append(
                        f"Function '{node.name}' at line {node.lineno} missing docstring"
                    )
                if func_info["args"] > 5:
                    analysis["issues"].append(
                        f"Function '{node.name}' has {func_info['args']} parameters (>5 suggests complexity)"
                    )
            
            elif isinstance(node, ast.ClassDef):
                class_info = {
                    "name": node.name,
                    "line_number": node.lineno,
                    "methods": len([n for n in node.body if isinstance(n, ast.FunctionDef)]),
                    "has_docstring": ast.get_docstring(node) is not None
                }
                analysis["classes"].append(class_info)
                
                if not class_info["has_docstring"]:
                    analysis["issues"].append(
                        f"Class '{node.name}' at line {node.lineno} missing docstring"
                    )
            
            elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        analysis["imports"].append(alias.name)
                else:
                    analysis["imports"].append(node.module)
        
        return analysis
        
    except SyntaxError as e:
        return {
            "status": "error",
            "error_message": f"Syntax error in code: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error analyzing code: {str(e)}"
        }

# # Test the tool
# test_code = """
# def calculate_sum(a, b):
#     return a + b
#
# class Calculator:
#     def add(self, x, y):
#         return x + y
# """
#
# print(analyze_code_structure(test_code))

def check_security_issues(code: str) -> dict:
    """Checks code for common security vulnerabilities.
    
    Args:
        code (str): Python code to check for security issues.
    
    Returns:
        dict: Security analysis results with potential vulnerabilities.
    """
    print(f"--- Tool: check_security_issues called ---")
    
    security_issues = []
    lines = code.split('\n')
    
    # Common security patterns to check
    dangerous_patterns = {
        'eval(': 'Dangerous use of eval() - can execute arbitrary code',
        'exec(': 'Dangerous use of exec() - can execute arbitrary code',
        'pickle.loads': 'Unsafe deserialization with pickle - can execute code',
        '__import__': 'Dynamic imports can be security risk',
        'os.system': 'Direct system calls - prefer subprocess with shell=False',
        'shell=True': 'Shell injection risk - avoid shell=True in subprocess',
        'sql': 'Potential SQL injection - use parameterized queries',
        'password': 'Hardcoded password detected - use environment variables',
        'api_key': 'Hardcoded API key detected - use environment variables',
        'SECRET': 'Hardcoded secret detected - use environment variables'
    }
    
    for i, line in enumerate(lines, 1):
        line_lower = line.lower()
        for pattern, message in dangerous_patterns.items():
            if pattern in line_lower:
                security_issues.append({
                    "line": i,
                    "pattern": pattern,
                    "message": message,
                    "severity": "HIGH" if pattern in ['eval(', 'exec(', 'pickle.loads'] else "MEDIUM",
                    "code_snippet": line.strip()
                })
    
    return {
        "status": "success",
        "issues_found": len(security_issues),
        "security_issues": security_issues,
        "safe": len(security_issues) == 0
    }

# Example usage of check_security_issues:
# test_security_code = """
# import os
# password = "admin123"
# os.system("rm -rf /")
# result = eval(user_input)
# """
#
# print(check_security_issues(test_security_code))


def check_performance_issues(code: str) -> dict:

    """Analyzes code for performance anti-patterns.
    
    Args:
        code (str): Python code to analyze for performance.
    
    Returns:
        dict: Performance analysis with recommendations.
    """
    print(f"--- Tool: check_performance_issues called ---")
    
    performance_issues = []
    lines = code.split('\n')
    
    # Performance anti-patterns
    patterns = {
        'for i in range(len(': 'Use enumerate() instead of range(len())',
        '.append(': 'Consider list comprehension if building list in loop',
        'global ': 'Global variables can hurt performance and readability',
        '+ str(': 'String concatenation in loop - use join() or f-strings',
        'try:': 'Empty except blocks hide errors (if found)'
    }
    
    in_loop = False
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        
        # Track if we're in a loop
        if stripped.startswith(('for ', 'while ')):
            in_loop = True
        elif stripped and not stripped.startswith(' ') and in_loop:
            in_loop = False
        
        for pattern, message in patterns.items():
            if pattern in stripped:
                if pattern == '.append(' and in_loop:
                    performance_issues.append({
                        "line": i,
                        "message": message,
                        "severity": "LOW",
                        "code_snippet": stripped
                    })
                elif pattern != '.append(':
                    performance_issues.append({
                        "line": i,
                        "message": message,
                        "severity": "MEDIUM",
                        "code_snippet": stripped
                    })
    
    return {
        "status": "success",
        "issues_found": len(performance_issues),
        "performance_issues": performance_issues,
        "optimized": len(performance_issues) == 0
    }


def check_documentation(code: str) -> dict:
    """Reviews code documentation quality.
    
    Args:
        code (str): Python code to check documentation.
    
    Returns:
        dict: Documentation quality analysis.
    """
    print(f"--- Tool: check_documentation called ---")
    
    try:
        tree = ast.parse(code)
        doc_issues = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                docstring = ast.get_docstring(node)
                name = node.name
                node_type = "Function" if isinstance(node, ast.FunctionDef) else "Class"
                
                if not docstring:
                    doc_issues.append({
                        "line": node.lineno,
                        "element": name,
                        "type": node_type,
                        "issue": "Missing docstring",
                        "severity": "HIGH"
                    })
                elif len(docstring) < 20:
                    doc_issues.append({
                        "line": node.lineno,
                        "element": name,
                        "type": node_type,
                        "issue": "Docstring too brief (< 20 chars)",
                        "severity": "MEDIUM"
                    })
                elif isinstance(node, ast.FunctionDef):
                    # Check if docstring mentions parameters
                    has_params = len(node.args.args) > 0
                    mentions_params = 'Args:' in docstring or 'Parameters:' in docstring
                    
                    if has_params and not mentions_params:
                        doc_issues.append({
                            "line": node.lineno,
                            "element": name,
                            "type": node_type,
                            "issue": "Docstring doesn't document parameters",
                            "severity": "MEDIUM"
                        })
                    
                    # Check for return documentation
                    has_return = any(isinstance(n, ast.Return) for n in ast.walk(node) if n != node)
                    mentions_return = 'Returns:' in docstring or 'Return:' in docstring
                    
                    if has_return and not mentions_return:
                        doc_issues.append({
                            "line": node.lineno,
                            "element": name,
                            "type": node_type,
                            "issue": "Docstring doesn't document return value",
                            "severity": "LOW"
                        })
        
        return {
            "status": "success",
            "issues_found": len(doc_issues),
            "documentation_issues": doc_issues,
            "well_documented": len(doc_issues) == 0
        }
    
    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e)
        }
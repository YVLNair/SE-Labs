# Lab 5: Static Code Analysis — Issues Report

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Unsafe `eval()` | Security | 12 | May execute arbitrary Python code from the configured formula. | Replace with safe formula evaluation. |
| Bare exception | Security/Quality | 37 | `except: pass` hides errors. | Catch specific exceptions and handle them explicitly. |
| Mutable default argument | Bug | 14 | `logs=[]` reuses the same list across calls. | Use `None` and initialize a fresh list. |
| Unsafe file handling | Quality | 29, 36 | Files are opened without context managers or explicit encoding. | Use `with open()` and UTF-8 encoding. |
| Unused imports | Style | 2–3 | `math` and `sys` are unused. | Remove unused imports. |
| Missing docstrings | Maintainability | Multiple | Module and functions lack documentation. | Add module and function docstrings. |
| Incorrect function naming | Style | 40 | `printShortlist()` violates snake_case. | Rename to `print_shortlist()`. |
| Boolean comparison | Style | 43 | Compares a Boolean directly with `True`. | Use `if results[r]["eligible"]:`. |
| Missing blank lines | Style | Multiple | Function definitions violate PEP 8 spacing. | Add the required blank lines. |
| Missing final newline | Style | 59 | File does not end with a newline. | Add a newline at the end of the file. |
| Unused function arguments | Quality | 11–12 | `gpa` and `credits` are not used in the original `eval()` implementation. | Use the arguments in a safe score calculation. |
| Built-in name shadowing | Quality | 11, 16 | `credits` shadows a Python built-in. | Rename it to a clearer name such as `extracurricular_credits`. |
| Global state mutation | Maintainability | 25, 34 | Functions modify global variables. | Reduce global mutation where practical. |

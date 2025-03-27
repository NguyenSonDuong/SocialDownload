import os
import ast

def get_imports(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=file_path)
    imports = {node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.Import)}
    imports |= {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}
    return imports

all_imports = set()
for root, _, files in os.walk("."):
    for file in files:
        if file.endswith(".py"):
            all_imports |= get_imports(os.path.join(root, file))

print("Các thư viện đang sử dụng:")
print("\n".join(sorted(all_imports)))

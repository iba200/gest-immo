import sys
import os

# Add the current directory to path
sys.path.append(os.getcwd())

from app import create_app

app = create_app()

with open('routes_list.md', 'w', encoding='utf-8') as f:
    f.write("# 🛣 Liste des Routes de l'Application ImmoGest\n\n")
    f.write("| Endpoint | Methods | Rule |\n")
    f.write("| :--- | :--- | :--- |\n")
    
    # Sort routes by endpoint
    rules = sorted(app.url_map.iter_rules(), key=lambda x: x.endpoint)
    
    for rule in rules:
        methods = ', '.join(sorted(list(rule.methods - {'OPTIONS', 'HEAD'})))
        if not methods: continue 
        f.write(f"| `{rule.endpoint}` | {methods} | `{rule.rule}` |\n")

print("Routes successfully written to routes_list.md")

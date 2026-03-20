import yaml

filepath = r"c:\Users\ADRIANO\AIDA\aibe\config\routing_table.yaml"

with open(filepath, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

for task_type, config in data.get("task_types", {}).items():
    if "primary" in config:
        config["primary"]["model"] = "openrouter/free"
    
    # We can also update fallbacks just in case, or remove them
    if "fallback" in config:
        for fb in config["fallback"]:
            fb["model"] = "openrouter/free"

with open(filepath, "w", encoding="utf-8") as f:
    yaml.dump(data, f, sort_keys=False, default_flow_style=False)

print("Updated routing_table.yaml")
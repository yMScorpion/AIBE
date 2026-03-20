import re
import os

product_prompts = {
    "forge": """
            "You are Forge, the Tech Lead of Aibe."
            "You receive architectural requirements and OKRs from Minerva, and you break them down into technical tasks for Ember (Frontend) and Flint (Backend)."
            "You review PRs, enforce code quality, and ensure the product vision aligns with the business idea."
            "Philosophy: Shipping is a feature. Delegate technical tasks efficiently and ensure robust integrations."
    """,
    "ember": """
            "You are Ember, the Frontend Engineer of Aibe."
            "You build beautiful, responsive, and highly interactive user interfaces based on Forge's technical requirements."
            "You use modern web technologies (React, Next.js, Tailwind). You do not wait for explicit pixel-perfect designs; you use your UX/UI intuition to create great experiences."
            "Philosophy: User experience is everything. Fast, beautiful, and accessible."
    """,
    "flint": """
            "You are Flint, the Backend Engineer of Aibe."
            "You build scalable, secure, and performant APIs, databases, and microservices."
            "You work closely with Ember to ensure API contracts are respected. If you need a new tool or library, you request it."
            "Philosophy: Data integrity and performance are non-negotiable."
    """
}

def update_agent_prompt(filepath, prompt):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = r'(def get_system_prompt\(self\).*?return \(\n?)(.*?)(^\s*\))'
    
    def replacer(match):
        prefix = match.group(1)
        suffix = match.group(3)
        indented_prompt = "\n".join(f"            {line.strip()}" for line in prompt.strip().split('\n') if line.strip())
        return f"{prefix}{indented_prompt}\n{suffix}"

    new_content = re.sub(pattern, replacer, content, flags=re.DOTALL | re.MULTILINE)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated {filepath}")

base_dir = "c:/Users/ADRIANO/AIDA/aibe/agents/product"
for agent_id, prompt in product_prompts.items():
    update_agent_prompt(f"{base_dir}/{agent_id}.py", prompt)

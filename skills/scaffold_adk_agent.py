import sys
import os
from pathlib import Path

TEMPLATE = """from google.adk import {agent_class}

def create_{agent_snake}_agent(model_name: str = "gemini-2.5-flash") -> {agent_class}:
    \"\"\"
    Creates the {agent_name} agent.
    \"\"\"
    return {agent_class}(
        name="{agent_snake}",
        model=model_name,
        instruction=\"\"\"
        TODO: Add instruction for {agent_name}.
        \"\"\",
        description="TODO: Add description."
    )
"""

def main():
    if len(sys.argv) < 2:
        print("Usage: python scaffold_adk_agent.py <AgentName> [AgentType]")
        print("Example: python scaffold_adk_agent.py Research LlmAgent")
        sys.exit(1)

    agent_name = sys.argv[1]
    agent_type = sys.argv[2] if len(sys.argv) > 2 else "Agent"
    
    agent_snake = agent_name.lower().replace(" ", "_")
    file_name = f"{agent_snake}_agent.py"
    
    base_path = Path(__file__).parent.parent / "infrastructure" / "adk" / "agents"
    base_path.mkdir(parents=True, exist_ok=True)
    
    file_path = base_path / file_name
    
    if file_path.exists():
        print(f"Error: Agent file {file_name} already exists.")
        sys.exit(1)
        
    content = TEMPLATE.format(
        agent_class=agent_type,
        agent_snake=agent_snake,
        agent_name=agent_name
    )
    
    with open(file_path, "w") as f:
        f.write(content)
        
    print(f"Successfully created ADK agent scaffold at: {file_path}")
    print("Don't forget to register it in the factory!")

if __name__ == "__main__":
    main()

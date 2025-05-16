import os
import re
import sys
import yaml
from crewai import Agent, Task, Crew

# === CONFIG ENV POUR OLLAMA ===
os.environ["OPENAI_API_KEY"] = "ollama"

# === UTILS ===

def strip_think_block(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

def save_outputs(task, label):
    try:
        full = task.output.final_output
    except AttributeError:
        full = str(task.output)
    clean = strip_think_block(full)

    with open(f"{label}.txt", "w", encoding="utf-8") as f:
        f.write(clean)
    with open(f"{label}_debug.txt", "w", encoding="utf-8") as f:
        f.write(full)

def load_yaml(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# === CHARGEMENT DES CONFIGS YAML ===

agents_config = load_yaml("agents.yaml")["agents"]
tasks_config = load_yaml("tasks.yaml")["tasks"]

# === CRÉATION DES AGENTS ===

agent_objects = {}

for key, cfg in agents_config.items():
    agent_objects[key] = Agent(
        role=cfg["role"],
        goal=cfg["goal"],
        backstory=cfg["backstory"],
        verbose=True,
        allow_delegation=False,
        llm="ollama/deepseek-r1:1.5b"
    )

# === CRÉATION DES TÂCHES (sans contexte dans un 1er temps) ===

task_objects = {}

for key, cfg in tasks_config.items():
    task_objects[key] = Task(
        description=cfg["description"],
        expected_output=cfg["expected_output"],
        agent=agent_objects[key]
    )

# === AJOUT DES CONTEXTES (une fois toutes les tâches créées) ===

for key, cfg in tasks_config.items():
    if "context" in cfg and cfg["context"]:
        task_objects[key].context = [task_objects[ctx] for ctx in cfg["context"]]

# === PHASE 1 & PHASE 2 ===

def run_phase1():
    print("\n--- PHASE 1 : OSINT + Phishing ---\n")
    crew = Crew(
        agents=[agent_objects["osint"], agent_objects["phishing"]],
        tasks=[task_objects["osint"], task_objects["phishing"]],
        verbose=True
    )
    result = crew.kickoff()
    save_outputs(task_objects["osint"], "osint")
    save_outputs(task_objects["phishing"], "phishing")
    return result

def run_phase2():
    print("\n--- PHASE 2 : Malware + Exfiltration ---\n")
    crew = Crew(
        agents=[agent_objects["malware"], agent_objects["exfiltration"]],
        tasks=[task_objects["malware"], task_objects["exfiltration"]],
        verbose=True
    )
    result = crew.kickoff()
    save_outputs(task_objects["malware"], "malware")
    save_outputs(task_objects["exfiltration"], "exfiltration")
    return result

# === CLI ===

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : python crew_attack_simulation.py [phase1|phase2]")
    elif sys.argv[1] == "phase1":
        print(run_phase1())
    elif sys.argv[1] == "phase2":
        print(run_phase2())
    else:
        print("Argument inconnu. Utilise 'phase1' ou 'phase2'.")

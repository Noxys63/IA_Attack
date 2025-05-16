# 🧪 Simulation d'attaque avec CrewAI + n8n

Ce projet simule une attaque en deux phases, déclenchée depuis n8n.

---

## ▶️ Comment utiliser

### 1. Lancer l'API Python

Dans le terminal, à la racine du projet :

```bash
uvicorn crew_api:app --reload --port 8000
```

L’API propose 2 routes :

- `POST http://localhost:8000/run/phase1` → Phase OSINT + Phishing
- `POST http://localhost:8000/run/phase2` → Phase Malware + Exfiltration

---

### 2. Depuis n8n

Importer le fichier `crewai_simulation_post_webhooks.json` dans n8n.

#### Pour lancer la simulation :
```bash
curl -X POST http://localhost:5678/webhook/start
```

#### Pour simuler un clic sur l'email :
```bash
curl -X POST http://localhost:5678/webhook/clic-email
```

---

## 📂 Fichiers générés

Les fichiers `.txt` produits sont :

- `osint.txt` → Rapport OSINT
- `phishing.txt` → Email de phishing
- `malware.txt` → Description du malware
- `exfiltration.txt` → Stratégie d’exfiltration

Chaque fichier existe aussi en version `_debug.txt` avec les détails internes du raisonnement de l’agent.

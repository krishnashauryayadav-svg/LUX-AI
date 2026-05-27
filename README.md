# ⚡ AUTOCLONE: Self-Healing Local AI Code Architect 🤖💻🛠️

[![Python](https://shields.io)](https://python.org)
[![Ollama](https://shields.io)](https://ollama.com)
[![Agentic](https://shields.io)](https://github.com)
[![Privacy](https://shields.io)](https://github.com)

> **"Code. Execute. Fail. Fix. Deliver."**  
An autonomous, 100% offline agentic software engineering pipeline that takes raw prompts, synthesizes executable source code via local LLMs, tests it inside isolated virtual environments, and auto-corrects runtime stack traces iteratively until a flawless production-ready bundle is delivered.

---

## 💎 The Engineering Masterstroke: Autonomous Self-Correction Loop
Aapka project simple code generation se bhaut aage hai. Yeh ek **Self-Healing Closed Feedback Loop** par chalta hai, jahan manual debugging ki koi zaroorat nahi padti:

```text
 ┌──────────────┐      ┌────────────────┐      ┌─────────────────┐
 │ User Prompt  ├─────►│  Local LLM     ├─────►│ Code Generation │
 └──────────────┘      │ (Friday Model) │      └────────┬────────┘
                       └───────▲────────┘               │
                               │                        ▼
                       ┌───────┴────────┐      ┌─────────────────┐
                       │  Ollama Feed   │      │ Isolated Venv   │
                       │  Error Stack   │◄─────┤ Execution Test  │
                       └────────────────┘      └────────┬────────┘
                                                        │ (If Success)
                                                        ▼
                                               ┌─────────────────┐
                                               │ Export Artifact │
                                               │ (Code + Regs)   │
                                               └─────────────────┘
```

---

## 🛠️ Deep-Dive Architecture & Core Systems

### 1. 🧠 Autonomous Prompt Synthesis & Generation Engine
- Raw engineering prompts ko accept karke unhe structured coding blueprints me parse karta hai.
- Interface handles system orchestration using local **Ollama API endpoints** to query lightweight, quantized models under resource constraints.

### 2. 🧪 Isolated Virtual Sandbox Sandbox (Venv Executor)
- Host dependencies ko contaminate hone se bachane ke liye programmatically ek dynamic, clean **Python Virtual Environment (`venv`)** spin up karta hai.
- Dynamic parsing engine automatic background me scripts me se required library imports detect karta hai aur unhe runtime test container ke andar `pip install` karta hai.

### 3. 🩺 Self-Healing & Error Remediation Layer (The Debugger Agent)
- Agar code execution ke waqt runtime errors (`Traceback`, `SyntaxError`, `ImportError`) aate hain, toh host sub-process pipelines un output logs ko directly capture karti hain.
- Yeh error payload reverse-route hokar wapas local model ke paas bheja jata hai ek optimized refinement prompt ke sath: *"Bhai, code crash ho gaya. Yeh raha error stack, isko repair karke optimized variant wapas do."*
- Yeh loop tab tak chalta hai jab tak code successfully zero-exit code ke sath execute na ho jaye.

### 4. 📦 Production Deployment Packager
- Once the pipeline verifies a 100% clean test execution, standard IO utilities take over.
- System automatically ek custom timestamped **output workspace folder** create karta hai.
- Bundles the absolute source code files alongside an auto-generated, strictly pinned **`requirements.txt`** deployment file.

---

## ⚙️ Pipeline Specifications

- **Execution Domain:** Local CPU Runtime Shell Sub-processes.
- **Sandboxing Utility:** Native Python `subprocess` + `venv` modules.
- **Self-Healing Depth:** Programmed with a strict **10-Iteration Maximum Loop Constraint** to aggressively resolve deep runtime exceptions while preventing endless API deadlock loops.
- **Cross-Platform Readiness:** Developed using standard cross-platform wrappers (`os.path`, `sys.executable`), allowing native execution parameters to adapt dynamically across generic OS terminals without strict architectural dependencies.


---

## 📜 Chronicles of Battle: Mitigating "Error Maharaj" 🛡️

1. **The Ghost Dependency Deadlock (`ModuleNotFoundError`)**  
   *Root Cause:* Generative models outputting custom imports that were missing inside the isolated sandbox container.  
   *Mitigation:* Injected an active subprocess installation step to dynamically pip-install requirements directly before checking interpreter outputs.

2. **The Terminal Stutter (`Subprocess Process Freeze`)**  
   *Root Cause:* Running generated infinite loops or heavy blocking scripts without explicit process timeout configurations.  
   *Mitigation:* Hardened the execution thread layers with a forced `timeout=30` exception handler to forcefully kill stalled scripts.

3. **The Workspace Overwrite Collision**  
   *Root Cause:* Sequential script runs cleaning up previous code directories due to identical absolute folder nomenclature structures.  
   *Mitigation:* Scaled up output folders with atomic alphanumeric naming tokens to store unique coding sessions permanently.

---
*Architected, engineered, and fine-tuned by Krishna Shaurya Yadav. Automating software development lifecycle workflows natively on local edge constraints.*

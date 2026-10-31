GhostOperator AI 🤖

An autonomous, local-first system engineering agent that translates natural language intentions into safe, structured multi-step computer workflows using Meta's open weights—operating completely independent of cloud APIs or active payment infrastructure.

🚀 The Core Innovation (Anti-Cliché Strategy)
GhostOperator AI was designed to completely avoid the standard chatbot and basic retrieval (RAG) wrapper paradigms. Instead of an uninspired chat window, it introduces an **Agentic System Engine** that evaluates, handles, and isolates programmatic actions natively via a four-stage loop:
1. Deep Workspace Context Parsing: Natively scans directory metadata boundaries to feed structural environment limits to the planner model.
2. Structured JSON Orchestration: Forces local execution models to generate deterministic multi-step recipes rather than unpredictable shell strings.
3. Dual-Layer Security Auditing: Uses a secondary programmatic schema and an internal AI audit checker that dynamically screens plans for boundary traps before execution.
4. Isolated Sandboxed Execution: Safe Python-level file manipulations locked strictly within the project folder.

 🛠️ Technical Stack
- Core LLM Engine: Meta Llama 3.2 (3B) Open Weights running completely offline.
- Inference Wrapper: Local Ollama API Client Framework utilizing structured JSON formats (`/api/chat`).
- Language Layer:Python 3.x (Native File System Isolation & Subprocess-free File Operations).

 📁 Repository Map
- main.py: Master controller agent shell interface loop.
- planner.py: Structural communication hook connecting to local Llama inference paths.
- executor.py: Safe tool registry containing sandboxed workspace logic and safety auditors.
- context_engine.py: Isolated metadata extractor tracking active workspace file layouts.

 🎬 Quickstart & Local Test Verification
1. Install [Ollama](https://ollama.com) and pull the free open-weights model:
   ```bash
   ollama run llama3.2
   ```
2. Run the master control driver script:
   ```bash
   python main.py
   ```
3. Input target instructions:
   > *"Find the latest csv file, extract all rows containing ERROR, and save it to error_report.txt"*

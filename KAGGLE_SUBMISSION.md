FlowScore AI — Kaggle AI Agents Capstone Submission

Overview
--------
This repository demonstrates an ADK multi-agent system that computes a deterministic Flow Score for users with thin credit histories. It includes:

- ADK Workflow agent orchestration (app/agent.py)
- A local MCP server with mock data and tools (app/mcp_server.py)
- Deterministic Flow Score utility (app/flow_score.py)
- Streamlit demo dashboard (app/streamlit_app.py)
- Integration and unit tests

How to run (local demo)
-----------------------
1. Install dependencies (recommended to use the project's uv/agents-cli flow):
   - pip install -r requirements.txt  # or use agents-cli install
   - pip install streamlit

2. Run the MCP mock server (optional for demo because functions are importable):
   - uv run python -m app.mcp_server

3. Launch demo dashboard:
   - streamlit run app/streamlit_app.py

Submission Notes
----------------
- The Flow Score calculator is deterministic and auditable (see app/flow_score.py).
- All MCP tools are registered in app/mcp_server.py and can be replaced with real integrations.
- The ADK workflow demonstrates agent-to-agent calls using McpToolset and AgentTool.

Files included in the submission
- README.md
- app/ (agent code, mcp_server, flow_score, streamlit app)
- tests/ (unit and integration)
- ARCHITECTURE.md (design description)
- demo.bat (Windows demo script)

Evaluation checklist (Kaggle)
- Reproducible: deterministic score function and sample data included.
- Documented: README + this document + architecture diagram.
- Runnable: streamlit dashboard and unit tests included.

Contact
-------
For questions about the submission reach out to the project maintainer listed in pyproject.toml.

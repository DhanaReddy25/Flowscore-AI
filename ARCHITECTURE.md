FlowScore AI — Architecture Overview

High-level components

1. ADK Multi-Agent Workflow (app/agent.py)
   - Workflow defines nodes: security_checkpoint -> financial_orchestrator -> process_report
   - Specialized LlmAgents: income_analyzer, behavior_risk_analyst
   - Uses McpToolset to call out to an MCP server for external data retrieval

2. MCP Server (app/mcp_server.py)
   - FastMCP based server exposing tools to fetch transaction history, income streams, credit checks
   - Includes deterministic compute_flow_score tool for transparent scoring

3. Deterministic Scoring (app/flow_score.py)
   - Standalone, auditable algorithm for mapping transaction and credit data to a 300-850 score

4. Demo & UI
   - Streamlit demo (app/streamlit_app.py) to show the score, sample transactions, and recommendations

5. Observability & Logging
   - AgentRuntime scaffolding logs to Cloud Logging when configured (see app/agent_runtime_app.py)

Security features
- PII scrubbing and prompt-injection detection in the security_checkpoint node
- Audit logs collected in the workflow state
- MCP tool health-check with optional environment-based token guard

Deployment
- agents-cli / agents runtime can deploy the App to Agent Runtime (see README)
- MCP server is a local Python module (app.mcp_server) and can be run via uv or containerized

Diagram
- See architecture.png(simple representation) or the textual diagram below.

Textual diagram

[User] --> ADK Workflow (security_checkpoint)
    --> (if ok) financial_orchestrator (calls AgentTools -> McpToolset)
        --> MCP Server (fetch_transaction_history, fetch_income_sources, check_credit_repayments)
        --> compute_flow_score (deterministic utility)
    --> process_report -> final user-facing summary


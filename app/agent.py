# ruff: noqa
import datetime
import json
import re
from typing import List, Dict, Any, Optional

from google.adk.agents import LlmAgent
from google.adk.apps import App
from google.adk.models import Gemini
from google.adk.workflow import START, Edge, node, Workflow
from google.adk.tools import AgentTool, McpToolset, request_input
from google.adk import Context
from google.adk.events.event import Event
from google.adk.events.event_actions import EventActions
from google.adk.events.request_input import RequestInput
from mcp import StdioServerParameters
from pydantic import BaseModel, Field

from config import config

# Initialize local MCP Toolset
mcp_toolset = McpToolset(
    connection_params=StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "app.mcp_server"],
    )
)

# 1. State Schema
class FlowScoreState(BaseModel):
    user_query: str = ""
    consent_given: bool = False
    security_audit_log: List[Dict[str, Any]] = Field(default_factory=list)
    income_analysis: str = ""
    risk_analysis: str = ""
    flow_score: int = 0
    recommendations: List[str] = Field(default_factory=list)
    suitable_opportunities: List[str] = Field(default_factory=list)
    final_summary: str = ""

# 2. Specialized Sub-Agents (sharing the MCP Toolset)
income_analyzer = LlmAgent(
    name="income_analyzer",
    model=Gemini(model=config.model),
    instruction="""You are a specialized alternative income analyst.
Use the tools in your toolset to fetch transaction history and income sources.
Identify all active income streams (gig work, freelancing, micro-business, rent, etc.).
Calculate:
1. Income consistency (e.g., monthly deposits, frequency).
2. Income growth or stability trends.
Provide a clear analysis of income consistency, average monthly earnings, and an overall income stability assessment.""",
    tools=[mcp_toolset],
)

behavior_risk_analyst = LlmAgent(
    name="behavior_risk_analyst",
    model=Gemini(model=config.model),
    instruction="""You are a financial risk analyst.
Use the tools in your toolset to fetch transaction history and check credit repayments.
Identify spending risks such as:
1. Volatile spending relative to income.
2. Direct risk signals (e.g., high debt repayments, recurring overdrafts, payment failures).
Calculate a risk level (Low, Medium, High) and provide a behavior-based risk assessment summary.""",
    tools=[mcp_toolset],
)

# 3. Security Checkpoint (Function Node)
@node
async def security_checkpoint(ctx: Context, node_input: str):
    if not ctx.state.security_audit_log:
        ctx.state.security_audit_log = []

    # Prompt Injection Check
    injection_keywords = ["ignore previous instructions", "system prompt", "jailbreak", "override security", "bypass rules"]
    is_injection = any(kw in node_input.lower() for kw in injection_keywords)
    if is_injection:
        audit_log = {
            "timestamp": datetime.datetime.now().isoformat(),
            "event": "prompt_injection_detected",
            "severity": "CRITICAL",
            "details": f"Flagged input: {node_input}"
        }
        ctx.state.security_audit_log.append(audit_log)
        return Event(
            output="Security check failed: Prompt injection detected.",
            actions=EventActions(route="SECURITY_EVENT")
        )

    # PII Scrubbing
    pan_pattern = r'[A-Z]{5}[0-9]{4}[A-Z]{1}'
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    phone_pattern = r'\+?[0-9]{2,4}[ -]?[0-9]{10}'
    
    scrubbed_input = node_input
    scrubbed_input = re.sub(pan_pattern, "[REDACTED_PAN]", scrubbed_input)
    scrubbed_input = re.sub(email_pattern, "[REDACTED_EMAIL]", scrubbed_input)
    scrubbed_input = re.sub(phone_pattern, "[REDACTED_PHONE]", scrubbed_input)

    # Domain-Specific Rule: Consent check
    consent_given = ctx.state.consent_given or False
    if not consent_given:
        # Check if user confirms consent in response to interrupt
        interrupt_id = "consent_interrupt"
        if ctx.resume_inputs and interrupt_id in ctx.resume_inputs:
            user_response = ctx.resume_inputs[interrupt_id]
            if any(word in user_response.lower() for word in ["consent", "agree", "yes", "i confirm", "authorize"]):
                ctx.state.consent_given = True
                consent_given = True
                audit_log = {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "event": "consent_acquired",
                    "severity": "INFO",
                    "details": "User granted consent via manual input."
                }
                ctx.state.security_audit_log.append(audit_log)
            else:
                audit_log = {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "event": "consent_denied",
                    "severity": "CRITICAL",
                    "details": f"User denied consent: {user_response}"
                }
                ctx.state.security_audit_log.append(audit_log)
                return Event(
                    output="Consent denied. Financial analysis aborted.",
                    actions=EventActions(route="SECURITY_EVENT")
                )
        else:
            # Check if query itself has consent
            query_has_consent = any(word in scrubbed_input.lower() for word in ["consent", "authorize", "agree", "allow", "i confirm"])
            if query_has_consent:
                ctx.state.consent_given = True
                consent_given = True
            else:
                audit_log = {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "event": "consent_missing",
                    "severity": "WARNING",
                    "details": "Consent missing in query. Prompting user."
                }
                ctx.state.security_audit_log.append(audit_log)
                return RequestInput(
                    interrupt_id=interrupt_id,
                    message="To generate your Flow Score, FlowScore AI requires your consent to analyze your cash-flow and transaction history. Please reply 'I consent' to proceed.",
                    response_schema={"type": "string"}
                )

    # Audit log entry for success
    audit_log = {
        "timestamp": datetime.datetime.now().isoformat(),
        "event": "security_check_passed",
        "severity": "INFO",
        "details": "PII scrubbed and consent verified."
    }
    ctx.state.security_audit_log.append(audit_log)
    ctx.state.user_query = scrubbed_input
    return Event(output=scrubbed_input)

# 4. Security Incident Response Node
@node
async def security_incident_response(ctx: Context, node_input: str):
    return f"ACCESS DENIED: A security event was triggered. Details: {node_input}"

# 5. Financial Orchestrator Agent
income_analyzer_tool = AgentTool(agent=income_analyzer)
behavior_risk_analyst_tool = AgentTool(agent=behavior_risk_analyst)

financial_orchestrator = LlmAgent(
    name="financial_orchestrator",
    model=Gemini(model=config.model),
    instruction="""You are FlowScore AI's lead financial inclusion orchestrator.
Your goal is to evaluate creditworthiness for users without traditional credit profiles.
You have access to specialized tools:
- `income_analyzer` (AgentTool): Call it to get a deep-dive analysis of user income streams.
- `behavior_risk_analyst` (AgentTool): Call it to get a risk analysis of user spending.
- `request_input` (LongRunningFunctionTool): Call it to request clarification or additional information from the user if their transaction details are ambiguous or missing.

Once you have gathered the income and risk analyses:
1. Compute a 'Flow Score' (integer between 300 and 850) based on income stability and spending risk.
2. Create key recommendations to improve their cash-flow.
3. Recommend suitable opportunities (micro-loans, savings plans, etc.).
4. Return a structured JSON response matching this schema:
{
  "income_analysis": "Summary of income streams and stability.",
  "risk_analysis": "Summary of spending patterns and risks.",
  "flow_score": 720,
  "recommendations": ["Recommendation 1", "Recommendation 2"],
  "suitable_opportunities": ["Opportunity 1", "Opportunity 2"],
  "summary": "General overview of the user's financial profile."
}

Do NOT wrap the JSON in conversational filler. Output ONLY the JSON block.""",
    tools=[income_analyzer_tool, behavior_risk_analyst_tool, request_input],
)

# 6. Report Processor Node
@node
async def process_report(ctx: Context, node_input: str):
    try:
        # Clean markdown wrappers if present
        text = node_input.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        
        report_data = json.loads(text)
        ctx.state.income_analysis = report_data.get("income_analysis", "No income analysis provided.")
        ctx.state.risk_analysis = report_data.get("risk_analysis", "No risk analysis provided.")
        ctx.state.flow_score = int(report_data.get("flow_score", 0))
        ctx.state.recommendations = list(report_data.get("recommendations", []))
        ctx.state.suitable_opportunities = list(report_data.get("suitable_opportunities", []))
        ctx.state.final_summary = report_data.get("summary", "No summary provided.")
    except Exception as e:
        # Graceful fallback if JSON parsing fails
        ctx.state.final_summary = node_input
        ctx.state.flow_score = 500  # neutral default
        ctx.state.recommendations = ["Provide more structured transaction data to get custom suggestions."]
        ctx.state.suitable_opportunities = ["Basic savings account"]
        
    return f"""📊 FlowScore AI Assessment Report
======================================
Flow Score: {ctx.state.flow_score}/850
Summary: {ctx.state.final_summary}

💡 Recommendations:
{chr(10).join('- ' + r for r in ctx.state.recommendations)}

💼 Suitable Schemes & Opportunities:
{chr(10).join('- ' + o for o in ctx.state.suitable_opportunities)}"""

# 7. Workflow Graph Setup
edges = [
    Edge(from_node=START, to_node=security_checkpoint),
    Edge(from_node=security_checkpoint, to_node=financial_orchestrator),  # Default route goes to orchestrator
    Edge(from_node=security_checkpoint, to_node=security_incident_response, route="SECURITY_EVENT"),
    Edge(from_node=financial_orchestrator, to_node=process_report),  # Default route
]

flowscore_workflow = Workflow(
    name="flowscore_workflow",
    edges=edges,
    state_schema=FlowScoreState,
)
root_agent = flowscore_workflow
app = App(
    root_agent=root_agent,
    name="app",
)

# FlowScore AI – Architecture Overview

## Overview

FlowScore AI is an AI-powered alternative credit scoring platform designed for gig workers, freelancers, and underserved individuals who may lack traditional credit histories. The system evaluates financial behavior using transaction history, income consistency, spending patterns, and repayment records to generate a transparent cash-flow-based credit score and risk assessment.

---

## System Components

### 1. ADK Multi-Agent Workflow (`app/agent.py`)

The core intelligence layer is built using Google ADK's multi-agent architecture.

**Workflow Nodes**

* Security Checkpoint
* Financial Orchestrator
* Report Processing

**Specialized Agents**

* Income Analyzer Agent
* Behavior Risk Analyst Agent

**Responsibilities**

* Coordinate financial analysis
* Evaluate user cash-flow behavior
* Generate risk insights and recommendations
* Manage tool interactions through MCP

---

### 2. MCP Server (`app/mcp_server.py`)

The Model Context Protocol (MCP) server acts as the data access layer.

**Available Tools**

* `fetch_transaction_history()`
* `fetch_income_sources()`
* `check_credit_repayments()`
* `compute_flow_score_tool()`

**Responsibilities**

* Provide financial data to agents
* Simulate banking and transaction records
* Support transparent score calculation

---

### 3. Flow Score Engine (`app/flow_score.py`)

The deterministic scoring engine converts financial activity into a credit score.

**Inputs**

* Transaction history
* Income sources
* Repayment behavior

**Output**

* Flow Score (300–850)

**Purpose**

* Provide an explainable alternative to traditional credit scoring systems
* Enable transparent and auditable financial assessments

---

### 4. Streamlit Dashboard (`app/streamlit_app.py`)

The user interface demonstrates the platform capabilities.

**Features**

* Display transaction history
* Show income and repayment data
* Generate Flow Score
* Provide financial recommendations

**Output**

* Credit score visualization
* Risk assessment summary
* User-friendly insights

---

### 5. Observability and Logging

The platform includes monitoring support through Agent Runtime infrastructure.

**Capabilities**

* Audit logging
* Agent activity tracking
* Cloud Logging integration
* Telemetry support

---

## Security Features

### Security Checkpoint Agent

The system performs security validation before processing user data.

**Security Controls**

* Prompt injection detection
* Sensitive information filtering
* Input validation
* Audit trail generation

### MCP Protection

* Tool health checks
* Environment-based access controls
* Secure data flow between agents and tools

---

## System Workflow

1. User submits financial information.
2. Security Checkpoint validates the request.
3. Financial Orchestrator coordinates analysis.
4. MCP Server retrieves transaction and repayment data.
5. Flow Score Engine calculates a cash-flow-based score.
6. Risk assessment and recommendations are generated.
7. Results are displayed through the Streamlit dashboard.

---

## Architecture Diagram

See `architecture.png` for the visual representation of the system architecture.

---

## Data Flow

```text
User
 │
 ▼
Security Checkpoint Agent
 │
 ▼
Financial Orchestrator
 │
 ├── Income Analyzer Agent
 ├── Behavior Risk Analyst Agent
 │
 ▼
MCP Server
 │
 ├── Transaction History
 ├── Income Sources
 └── Credit Repayments
 │
 ▼
Flow Score Engine
 │
 ▼
Risk Assessment & Recommendations
 │
 ▼
Streamlit Dashboard
```

---

## Future Enhancements

* Real bank statement integration
* UPI transaction ingestion
* Loan eligibility recommendations
* Explainable AI financial reports
* Fraud detection capabilities
* Financial literacy assistant

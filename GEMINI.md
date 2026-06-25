# FlowScore AI – Development Guide

## Project Overview

FlowScore AI is a financial inclusion and alternative credit scoring system built using Google ADK, MCP (Model Context Protocol), and Streamlit.

The project analyzes:

* Transaction history
* Income sources
* Credit repayment behavior

and generates a transparent Flow Score (300–850) that can help evaluate financial reliability for users with limited traditional credit history.

---

## Architecture

### Core Components

#### 1. ADK Multi-Agent Workflow

Location: `app/agent.py`

Agents:

* Security Checkpoint Agent
* Financial Orchestrator Agent
* Income Analyzer Agent
* Behavior Risk Analyst Agent

Responsibilities:

* Validate requests
* Detect prompt injection attempts
* Coordinate financial analysis
* Generate user recommendations

#### 2. MCP Server

Location: `app/mcp_server.py`

Tools:

* fetch_transaction_history
* fetch_income_sources
* check_credit_repayments
* compute_flow_score_tool

Responsibilities:

* Provide financial data
* Expose scoring functionality
* Simulate external financial services

#### 3. Flow Score Engine

Location: `app/flow_score.py`

Responsibilities:

* Deterministic score calculation
* Transparent and auditable logic
* Score range: 300–850

Factors:

* Income stability
* Spending behavior
* Credit repayment history
* Financial consistency

#### 4. Streamlit Dashboard

Location: `app/streamlit_app.py`

Features:

* User input interface
* Transaction visualization
* Flow Score display
* Financial recommendations

---

## Local Development

Install dependencies:

```bash
agents-cli install
```

Run Streamlit demo:

```bash
streamlit run app/streamlit_app.py
```

Run tests:

```bash
pytest tests
```

Launch ADK playground:

```bash
agents-cli playground
```

---

## Security Features

* Prompt injection detection
* PII protection
* Audit logging
* Tool access controls

---

## Future Improvements

* Real bank API integrations
* Advanced ML-based scoring
* Fraud detection module
* Personalized financial recommendations
* Real-time analytics dashboard

---

## Kaggle Gen AI Intensive Course Submission

Project: FlowScore AI

Theme:
Financial Inclusion through AI

Technologies Used:

* Google ADK
* Gemini
* MCP
* Python
* Streamlit

Goal:
Provide alternative credit scoring for underserved individuals using transparent AI-assisted financial analysis.
 409): Use `terraform import` instead of retrying creation.

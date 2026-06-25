# FlowScore AI: AI-Powered Alternative Credit Scoring

## Subtitle
*Enabling fair financial inclusion for gig workers and freelancers through AI agent-driven cash-flow analysis.*

---

## Problem Statement

**The Challenge:** Over 1.7 billion individuals globally—including gig workers, freelancers, and self-employed professionals—lack access to formal credit because they don't have traditional credit histories. Banks reject loan applications despite proven, consistent cash-flow, simply because these individuals don't fit conventional credit scoring models.

**Why It Matters:** 
- Underserved populations cannot invest in growth or weather financial emergencies
- Gig economy workers represent $1.1 trillion annually but remain systematically underbanked
- Economic potential is wasted due to outdated, historical evaluation metrics

**The Opportunity:** What if we evaluated creditworthiness based on *actual financial behavior*—transaction patterns, income consistency, spending discipline—rather than historical credit records?

---

## Solution Overview

### What is FlowScore AI?

FlowScore AI is an **AI agent-powered alternative credit scoring system** that evaluates financial creditworthiness through cash-flow analysis instead of credit history.

**How It Works:**
1. User submits transaction history and income data
2. Specialized AI agents autonomously analyze income stability and financial behavior
3. A deterministic scoring engine calculates a FlowScore (300–850 scale)
4. Intelligent recommendations guide lending decisions
5. Results displayed through an intuitive Streamlit dashboard

**User Benefits:**
- Fair evaluation based on actual financial behavior
- Real-time scoring without manual underwriting delays
- Transparent logic—users understand their score
- Actionable recommendations for financial improvement

---

## Why AI Agents?

Traditional applications follow fixed logic paths. AI agents provide critical advantages for alternative credit scoring:

**Autonomous Reasoning:** Agents don't execute predetermined scripts. They analyze income patterns, spending behavior, and risk signals dynamically—adapting logic based on data characteristics rather than hardcoded rules.

**Multi-Step Orchestration:** Specialized sub-agents (income analyzer, risk analyst) handle distinct domains autonomously, coordinating results without explicit code paths. This modularity enables scaling and adaptation.

**Tool Integration at Scale:** MCP (Model Context Protocol) enables agents to discover and invoke tools independently—fetching transaction data, computing scores, and generating recommendations without manual orchestration.

**Security & Audit Trails:** Autonomous validation agents check for malicious input before financial data is processed. Every decision leaves an audit trail, critical for regulatory compliance in lending.

**Adaptability:** Adding new lending criteria doesn't require redeployment—agents adjust through updated instructions. Future enhancements (financial literacy coaching, loan negotiation) emerge naturally.

**In essence:** Agents transform FlowScore AI from a calculator into an intelligent financial assistant that reasons, validates, and acts—essential for fair, scalable alternative credit systems.

---

## Project Architecture

```
User Input (via Streamlit)
        ↓
┌─────────────────────────────────┐
│   AI Agent Workflow (ADK)       │
│ • Security Checkpoint           │
│ • Income Analyzer Agent         │
│ • Risk Analyst Agent            │
│ • Orchestrator                  │
└────────────┬────────────────────┘
             ↓
    ┌────────────────────┐
    │  MCP Server        │
    │ (Tool Abstraction) │
    └────────┬───────────┘
             ↓
    ┌────────────────────────────────┐
    │  Financial Data Tools          │
    │ • fetch_transaction_history()  │
    │ • fetch_income_sources()       │
    │ • check_credit_repayments()    │
    │ • compute_flow_score_tool()    │
    └────────────┬───────────────────┘
                 ↓
    ┌────────────────────────────────┐
    │  Flow Score Engine             │
    │  (Deterministic Algorithm)     │
    └────────────┬───────────────────┘
                 ↓
    Dashboard Output & Recommendations
```

**Component Details:**

- **Streamlit Interface:** User dashboard for querying scores and viewing results
- **AI Agent Workflow:** Security validation, multi-agent analysis, orchestration
- **MCP Server:** Standardized tool access for financial data
- **Flow Score Engine:** Transparent, auditable scoring algorithm (300–850)
- **Data Layer:** Transaction history, income sources, repayment records

---

## Technical Implementation

### Technology Stack
- **Language:** Python 3.x
- **AI Framework:** Google Agents Development Kit (ADK)
- **LLM:** Gemini 2.5 Flash
- **MCP Protocol:** Model Context Protocol for tool standardization
- **Web Framework:** Streamlit for rapid dashboard development
- **Development Tool:** Antigravity for streamlined project creation and iteration

### Key Technologies Explained

**Google ADK:** Provides `LlmAgent` for autonomous reasoning, `Workflow` for orchestration, and state management via Pydantic. Agents bind to `McpToolset` for tool discovery.

**MCP Server:** Exposes financial data tools (`fetch_transaction_history`, `fetch_income_sources`, `check_credit_repayments`, `compute_flow_score_tool`). FastMCP implementation enables stdio-based communication with agents.

**Deterministic Scoring:** Non-LLM algorithm ensuring reproducibility for regulatory compliance. Factors:
- Income consistency (0–200 points)
- Income scale (0–200 points)  
- Spending volatility penalty (0–300 points)
- Credit behavior bonus (0–100 points)
- Base: 300; Maximum: 850

---

## Key Features

1. **AI-Powered Multi-Agent Analysis**
   - Specialized agents autonomously analyze income stability and financial behavior
   - Agents coordinate without explicit orchestration code

2. **Automated Financial Data Processing**
   - MCP-driven automation: agents fetch, parse, and extract insights from transaction data
   - Scalable to multiple data sources (UPI, banking APIs, fintech platforms)

3. **Real-Time Scoring & Recommendations**
   - Sub-second flow score computation
   - Instant lending recommendations tailored to risk profile

4. **Security-First Architecture**
   - Security checkpoint detects and blocks malicious inputs
   - Comprehensive audit logging of all financial data access

5. **Transparent, Explainable Scoring**
   - Deterministic algorithm ensures reproducibility
   - Users understand score composition and factors

6. **Interactive Web Dashboard**
   - Real-time query interface
   - Transaction and income breakdowns
   - Responsive design for accessibility

---

## Development Journey

### Kaggle AI Agents: Intensive Vibe Coding Capstone

FlowScore AI was developed during **Kaggle's 5-Day AI Agents Intensive Vibe Coding course**, a comprehensive exploration of autonomous agent design and deployment.

**Learning Progression:**
- **Days 1–2:** Built foundational understanding of Google ADK architecture, agents, tools, workflows, and state management. Implemented first autonomous income analysis agent.
- **Days 3–4:** Implemented MCP Protocol for standardized tool access. Created MCP server with financial data tools. Added security checkpoint agent for prompt injection detection.
- **Day 5:** Integrated Streamlit dashboard, deployed to production-ready architecture, optimized costs, and conducted evaluation runs to validate agent behavior.

**Key Insights:**
- Agents excel at complex financial reasoning, adapting to unique user profiles
- MCP standardization eliminates integration boilerplate and enables scalability
- Autonomous validation agents catch security issues traditional applications miss

---

## Demo Explanation

**Workflow: Evaluating a Freelancer**

1. **Input:** User enters freelancer ID in Streamlit dashboard
2. **Security:** Agent validates input (checks for injection patterns)
3. **Data Collection:** Income Analyzer autonomously fetches transaction history and income sources
4. **Analysis:** Risk Analyst identifies spending patterns and repayment behavior
5. **Scoring:** Flow Score Engine computes result based on extracted metrics
6. **Output:** Dashboard displays score, income stability, risk profile, and lending recommendations

**Example Result:**
```
Flow Score: 625/850
Income Consistency: ✅ Stable (₹49,000/month avg)
Risk Profile: ✅ Low
Recommendation: Eligible for ₹150K micro-business loan at 9%
```

---

## Challenges Faced & Solutions

| Challenge | Solution |
|-----------|----------|
| **Deterministic scoring vs. LLM variability** | Separated concerns: agents handle reasoning; deterministic algorithm computes final score |
| **Financial data privacy & security** | Security checkpoint agent validates inputs; audit logging enabled; PII redaction configurable |
| **Multi-agent coordination complexity** | Used ADK Workflow abstraction with Pydantic state schema for type-safe transitions |
| **Real vs. mock financial data** | Built MCP abstraction layer—MVP uses mock data; production ready for live APIs |
| **Agent evaluation & validation** | Created evaluation datasets using ADK eval framework to validate determinism and accuracy |

---

## Future Improvements

**Near-Term (3–6 months):**
- Real financial data integration (UPI APIs, bank OpenBanking)
- Advanced risk scoring (seasonality detection, macroeconomic factors)
- Personalized loan recommendation engine

**Medium-Term (6–12 months):**
- Explainable AI reports with scoring breakdowns
- Financial literacy assistant agent
- Multi-currency and geo-expansion

**Long-Term (1+ year):**
- Marketplace for agent-negotiated lending
- Predictive default prevention
- Open-source alternative credit framework

---

## Conclusion

FlowScore AI demonstrates that **AI agents can democratize financial inclusion by evaluating creditworthiness based on behavioral cash-flow analysis rather than historical records.** 

The project showcases:
- **Agent-powered reasoning** for complex financial decisions
- **MCP standardization** enabling scalable data integration
- **Transparent, deterministic** scoring building user trust
- **Real-world impact** potential for millions of underserved workers

By shifting from "Do you have a credit history?" to "What does your cash-flow tell us?"—FlowScore AI opens credit access to the world's 1.7 billion unbanked individuals, enabling economic growth and financial resilience.

---

**Repository:** https://github.com/DhanaReddy25/Flowscore-AI  
**Technologies:** Google ADK, Gemini AI, MCP Protocol, Streamlit, Python  
**Author:** Dhana Laxmi | B.Tech CSE (AIML) | Neil Gogte Institute of Technology  
**Course:** Kaggle AI Agents: Intensive Vibe Coding Capstone Project
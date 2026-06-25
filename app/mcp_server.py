import os
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("FlowScore-AI-Server")

@mcp.tool()
def fetch_transaction_history(user_id: str) -> str:
    """Fetch transaction history for a user to analyze spending and cash-flow patterns.
    
    Args:
        user_id: The ID of the user.
    """
    # Mock data showing cash inflows (deposits) and outflows (spending)
    return """Date,Description,Amount,Type,Category
2026-06-01,UPI Deposit (Client Payment),15000,IN,Income
2026-06-02,Grocery Store,-1200,OUT,Essentials
2026-06-05,Electricity Bill,-2500,OUT,Utilities
2026-06-10,UPI Deposit (Freelance Project),22000,IN,Income
2026-06-12,Restaurant Spend,-1800,OUT,Leisure
2026-06-15,UPI Deposit (Consulting Fee),12000,IN,Income
2026-06-20,Rent Payment,-12000,OUT,Rent
2026-06-22,Mobile Recharge,-500,OUT,Utilities
2026-06-24,ATM Withdrawal,-2000,OUT,Cash
"""

@mcp.tool()
def fetch_income_sources(user_id: str) -> str:
    """Fetch recurring income sources and payment channels for a user.
    
    Args:
        user_id: The ID of the user.
    """
    # Mock data showing gig/freelance income consistency
    return """Income Stream,Source Channel,Frequency,Average Amount
Client Payment,UPI Deposit,Monthly,15000
Freelance Project,UPI Deposit,Bi-weekly,22000
Consulting Fee,UPI Deposit,Monthly,12000
"""

@mcp.tool()
def check_credit_repayments(user_id: str) -> str:
    """Check user micro-loan repayments or outstanding credit card bills.
    
    Args:
        user_id: The ID of the user.
    """
    # Mock data showing credit behavior
    return """Institution,Loan Type,Due Date,Amount,Repayment Status
Micro-finance Inst,Micro-business Loan,2026-06-10,5000,Paid on time
E-commerce Pay Later,Consumer Credit,2026-06-15,1500,Paid on time
"""

from flow_score import compute_flow_score


@mcp.tool()
def compute_flow_score_tool(transactions_csv: str, income_sources_csv: str = "", credit_csv: str = "") -> int:
    """MCP-accessible deterministic flow score tool.

    Accepts transaction CSV and optional income/credit CSVs and returns an
    integer Flow Score (300-850)."""
    return compute_flow_score(transactions_csv, income_sources_csv, credit_csv)


@mcp.tool()
def health_check(token: str = "") -> str:
    """Simple health check for MCP with optional token guard via MCP_HEALTH_TOKEN env var."""
    expected = os.environ.get("MCP_HEALTH_TOKEN")
    if expected and token != expected:
        return "UNAUTHORIZED"
    return "OK"


if __name__ == "__main__":
    mcp.run()

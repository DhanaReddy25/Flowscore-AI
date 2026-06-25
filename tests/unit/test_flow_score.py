from app.flow_score import compute_flow_score


def test_flow_score_on_mock_transactions():
    sample = """Date,Description,Amount,Type,Category
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
    income_csv = """Income Stream,Source Channel,Frequency,Average Amount
Client Payment,UPI Deposit,Monthly,15000
Freelance Project,UPI Deposit,Bi-weekly,22000
Consulting Fee,UPI Deposit,Monthly,12000
"""
    credit_csv = """Micro-finance Inst,Micro-business Loan,2026-06-10,5000,Paid on time
E-commerce Pay Later,Consumer Credit,2026-06-15,1500,Paid on time
"""

    score = compute_flow_score(sample, income_csv, credit_csv)
    assert isinstance(score, int)
    assert 300 <= score <= 850


def test_flow_score_is_deterministic():
    sample = """Date,Description,Amount,Type,Category
2026-06-01,UPI Deposit,10000,IN,Income
2026-06-02,Grocery,-500,OUT,Essentials
"""
    s1 = compute_flow_score(sample)
    s2 = compute_flow_score(sample)
    assert s1 == s2

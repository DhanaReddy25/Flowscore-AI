"""
Deterministic Flow Score calculator.
Provides a simple, auditable scoring function that maps transaction history
and credit behavior into a reproducible score between 300 and 850.

This module is intentionally deterministic and testable (no random seeds,
no LLM involvement).
"""
from __future__ import annotations

import csv
import math
from typing import Optional


def _parse_transactions(csv_text: str):
    """Parse a lightweight CSV of transactions and return lists of IN and OUT amounts.
    Expects a header like: Date,Description,Amount,Type,Category
    Type is either IN or OUT and Amount is a number (can have +/-).
    """
    reader = csv.DictReader(csv_text.strip().splitlines())
    ins = []
    outs = []
    total_tx = 0
    for row in reader:
        total_tx += 1
        try:
            amt = float(row.get("Amount", 0))
        except Exception:
            # Try to coerce possible formatted numbers
            s = str(row.get("Amount", "0")).replace(",", "")
            try:
                amt = float(s)
            except Exception:
                continue
        t = (row.get("Type") or "").upper()
        if t == "IN" or amt > 0:
            ins.append(abs(amt))
        else:
            outs.append(abs(amt))
    return ins, outs, total_tx


def _stddev(values: list[float]) -> float:
    if not values:
        return 0.0
    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / len(values)
    return math.sqrt(variance)


def compute_flow_score(
    transactions_csv: str,
    income_sources_csv: Optional[str] = None,
    credit_csv: Optional[str] = None,
) -> int:
    """Compute a deterministic Flow Score (300-850) from CSV inputs.

    Inputs are simple CSV strings (the repository provides example mock data
    from the MCP server). This is intentionally simple — meant as a transparent
    baseline scoring function for Kaggle submission and demos.

    Returns an integer score between 300 and 850.
    """
    ins, outs, total_tx = _parse_transactions(transactions_csv or "")

    total_in = sum(ins)
    total_out = sum(outs)

    # Income frequency / consistency
    num_in_tx = len(ins)
    freq_score = 0
    if total_tx > 0:
        freq = num_in_tx / float(max(1, total_tx))  # fraction of IN transactions
        # Map [0.0, 1.0] -> [0, 200]
        freq_score = int(200 * freq)

    # Income scale contribution (normalized)
    income_scale_score = 0
    if total_in > 0:
        # Map income to [0, 200] using a modest scaling factor
        income_scale_score = min(200, int((total_in / 1000.0) * 2))

    # Spending volatility penalty
    avg_in = total_in / max(1, num_in_tx)
    out_std = _stddev(outs)
    volatility = out_std / max(1.0, avg_in)
    volatility_penalty = int(min(300, volatility * 300))

    # Credit behavior bonus (from credit_csv content)
    credit_bonus = 0
    if credit_csv:
        try:
            # simple heuristic: if all lines say 'Paid on time' -> bonus 100
            rows = [r for r in credit_csv.splitlines() if r.strip()]
            if rows and all("Paid on time" in r for r in rows):
                credit_bonus = 100
            else:
                # partial bonus for mixed performance
                credit_bonus = 40
        except Exception:
            credit_bonus = 0

    # Compose score
    base = 400
    score = base + freq_score // 2 + income_scale_score // 1 + credit_bonus - volatility_penalty // 1

    # Clamp to [300, 850]
    score = max(300, min(850, int(score)))
    return score


if __name__ == "__main__":
    # Simple CLI demo
    sample = (
        "Date,Description,Amount,Type,Category\n"
        "2026-06-01,UPI Deposit,15000,IN,Income\n"
        "2026-06-02,Grocery,-1200,OUT,Essentials\n"
    )
    print("Sample Flow Score:", compute_flow_score(sample))

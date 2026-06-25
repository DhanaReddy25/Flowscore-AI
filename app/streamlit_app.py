"""
Streamlit app placed in `app/` for demo purposes (avoids creating new top-level dirs).
Run: streamlit run app/streamlit_app.py
"""
from __future__ import annotations

import streamlit as st
import mcp_server
from  flow_score import compute_flow_score

st.set_page_config(page_title="FlowScore AI Demo", layout="centered")
st.title("FlowScore AI — Demo Dashboard")

st.markdown("This lightweight dashboard demonstrates the deterministic Flow Score calculator and the MCP tools.")

user_id = st.text_input("User ID", "demo-user-1")

if st.button("Fetch and Compute Flow Score"):
    with st.spinner("Fetching transaction history from local MCP mock tool..."):
        tx_csv = mcp_server.fetch_transaction_history(user_id)
        income_csv = mcp_server.fetch_income_sources(user_id)
        credit_csv = mcp_server.check_credit_repayments(user_id)

    st.subheader("Transactions (sample)")
    st.code(tx_csv)

    score = compute_flow_score(tx_csv, income_csv, credit_csv)

    st.metric("Flow Score", f"{score}/850")

    st.subheader("Income Sources (sample)")
    st.code(income_csv)

    st.subheader("Credit & Repayments (sample)")
    st.code(credit_csv)

    if score >= 700:
        st.success("Strong cash-flow profile — user is likely eligible for several opportunities.")
    elif score >= 550:
        st.info("Moderate cash-flow profile — consider targeted micro-loans and savings plans.")
    else:
        st.warning("Low cash-flow score — recommend basic financial literacy and stability programs.")

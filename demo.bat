@echo off
REM Demo script for Windows: starts MCP mock module (if needed) and opens Streamlit demo
echo Starting FlowScore AI demo environment...

REM Optionally start MCP server in background (uncomment to run server separately)
REM uv run python -m app.mcp_server > mcp_server.log 2>&1

echo Launching Streamlit demo (app/streamlit_app.py)
python -m streamlit run app/streamlit_app.py

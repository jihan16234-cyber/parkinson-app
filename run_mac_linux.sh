#!/usr/bin/env bash
cd "$(dirname "$0")"
mkdir -p ~/.streamlit
[ -f ~/.streamlit/credentials.toml ] || printf '[general]\nemail = ""\n' > ~/.streamlit/credentials.toml
python3 -m pip install -r requirements.txt && python3 train.py && python3 -m streamlit run app.py

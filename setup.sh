#!/usr/bin/env bash

# setup backend
virtualenv --python=python3.8 ./.venv
source .venv/bin/activate

pip install -r requirements.txt

python app.py &

# setup frontend
cd frontend && npm install
npm start &

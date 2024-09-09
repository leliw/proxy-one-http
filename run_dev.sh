#!/bin/sh
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload &
cd ../frontend
ng serve -o --proxy-config=src/proxy.conf.json
cd ..
killall uvicorn
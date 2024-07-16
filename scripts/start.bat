@echo off
start cmd /c .venv\Scripts\uvicorn.exe api.main:app <nul

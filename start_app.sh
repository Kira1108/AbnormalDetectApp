conda deactivate
source env/bin/activate
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
uvicorn app.main:app --reload
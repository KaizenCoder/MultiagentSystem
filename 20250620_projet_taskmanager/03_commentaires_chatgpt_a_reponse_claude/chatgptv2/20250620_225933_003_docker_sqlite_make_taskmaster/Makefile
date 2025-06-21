start:
	uvicorn taskmaster_pool_supervisor:app --host 0.0.0.0 --port 8001 --reload

spawn:
	python spawn_worker.py

test:
	python dashboard_console.py && python session_validator.py

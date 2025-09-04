run:
	uvicorn main:app --reload --port 8002

lib:
	pip freeze > requirements.txt


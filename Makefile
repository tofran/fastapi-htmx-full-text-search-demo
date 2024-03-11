dev:
	uvicorn app:app --host "0.0.0.0" --reload

install:
	pip install -r requirements.txt
	wget -O ./static/htmx.min.js "https://github.com/bigskysoftware/htmx/releases/download/v1.9.10/htmx.min.js"

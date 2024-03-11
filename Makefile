dev:
	uvicorn --host "0.0.0.0" --reload text_search_app.app:app

install:
	pip install -r requirements.txt
	wget -O ./static/htmx.min.js "https://github.com/bigskysoftware/htmx/releases/download/v1.9.10/htmx.min.js"
